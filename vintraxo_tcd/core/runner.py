"""Code runner client (PLAN Phase 10, ADR-0019, docs/PHASE10_ISOLATION_DESIGN.md).

Frappe never executes learner code. It sends the code to a separate, isolated runner service
(Judge0 compatible API) and receives the output. Every run is logged in TCD Code Run.
Grading re-runs the code on the runner, so the output reported by the learner's device is ignored."""

import base64
import hashlib
from urllib.parse import urlparse

import frappe
import requests
from frappe import _
from frappe.utils import add_to_date, flt, now_datetime

SETTINGS = "TCD Settings"
LOG = "TCD Code Run"
BROWSER_LANGUAGES = {"python", "javascript", "sql", "html"}
MAX_CODE_BYTES = 64 * 1024
MAX_OUTPUT_CHARS = 64 * 1024
# Judge0 CE language ids (verify against your runner with "Test Runner": GET /languages)
DEFAULT_LANGUAGES = [
	("python", "Python 3", 71),
	("javascript", "JavaScript (Node.js)", 63),
	("java", "Java", 62),
	("cpp", "C++", 54),
	("c", "C", 50),
	("go", "Go", 60),
	("csharp", "C#", 51),
	("bash", "Bash", 46),
]
# Judge0 status ids -> our status
STATUS = {3: "Finished", 4: "Finished", 5: "Time Limit", 6: "Compilation Error"}
STATUS.update(dict.fromkeys(range(7, 13), "Runtime Error"))


class RunnerError(frappe.ValidationError):
	pass


def settings():
	return frappe.get_cached_doc(SETTINGS)


def languages(s=None) -> dict:
	"""Configured runner languages {language: runner_language_id}, or {} when the runner is off."""
	s = s or settings()
	if not s.get("runner_enabled"):
		return {}
	return {r.language.strip().lower(): int(r.runner_language_id) for r in s.get("runner_languages") or []}


def server_only(language: str | None) -> bool:
	return bool(language) and language not in BROWSER_LANGUAGES


def grades_on_server(item) -> bool:
	"""A Code question is graded on the runner when the runner supports its language and either the
	question asks for it or the language cannot run in the browser."""
	if item.get("type") != "Code":
		return False
	if item.get("test_cases"):
		return item.get("code_language") in languages()
	language = item.get("code_language")
	if language not in languages():
		return False
	return bool(item.get("grade_on_server")) or server_only(language)


def validate_settings(doc):
	if not doc.get("runner_enabled"):
		return
	url = (doc.runner_url or "").strip().rstrip("/")
	parsed = urlparse(url)
	if parsed.scheme not in ("http", "https") or not parsed.hostname:
		frappe.throw(_("The runner URL must be an http(s) URL."))
	doc.runner_url = url
	doc.runner_cpu_seconds = min(max(flt(doc.runner_cpu_seconds) or 5, 1), 15)
	doc.runner_wall_seconds = min(max(flt(doc.runner_wall_seconds) or 10, doc.runner_cpu_seconds), 30)
	doc.runner_memory_mb = min(max(int(doc.runner_memory_mb or 256), 32), 1024)
	doc.runner_runs_per_minute = max(int(doc.runner_runs_per_minute or 10), 1)
	if not doc.runner_languages:
		for language, label, lid in DEFAULT_LANGUAGES:
			doc.append("runner_languages", {"language": language, "label": label, "runner_language_id": lid})
	seen = set()
	for row in doc.runner_languages:
		row.language = (row.language or "").strip().lower()
		if row.language in seen:
			frappe.throw(_("Language {0} is listed twice.").format(row.language))
		seen.add(row.language)


# ---------------------------------------------------------------- HTTP


def _b64(text: str) -> str:
	return base64.b64encode((text or "").encode()).decode()


def _unb64(value) -> str:
	if not value:
		return ""
	try:
		return base64.b64decode(value).decode(errors="replace")
	except ValueError:
		return ""


def _headers(s) -> dict:
	headers = {"Content-Type": "application/json", "Accept": "application/json"}
	token = s.get_password("runner_token", raise_exception=False) if s.get("runner_token") else None
	if token:
		headers["X-Auth-Token"] = token
	return headers


def _post(s, payload: dict) -> dict:
	try:
		response = requests.post(
			f"{s.runner_url}/submissions?base64_encoded=true&wait=true",
			json=payload,
			headers=_headers(s),
			timeout=flt(s.runner_wall_seconds) + 20,
			allow_redirects=False,
		)
	except requests.RequestException as e:
		raise RunnerError(_("Cannot reach the code runner.")) from e
	if response.status_code >= 400:
		raise RunnerError(_("The code runner returned an error ({0}).").format(response.status_code))
	try:
		return response.json()
	except ValueError as e:
		raise RunnerError(_("The code runner sent an unreadable answer.")) from e


# ---------------------------------------------------------------- run


def run(
	language: str, code: str, user: str, purpose: str = "Practice", stdin: str = "", reference=None
) -> dict:
	"""Run code on the runner and log it. Returns {status, output, error, time_ms, memory_kb}."""
	s = settings()
	langs = languages(s)
	if not langs:
		frappe.throw(_("The code runner is turned off."), RunnerError)
	language = (language or "").strip().lower()
	if language not in langs:
		frappe.throw(_("The code runner does not support {0}.").format(language), RunnerError)
	code = code or ""
	if len(code.encode()) > MAX_CODE_BYTES:
		frappe.throw(_("The code is too long (maximum 64 KB)."), RunnerError)
	if purpose == "Practice":
		recent = frappe.db.count(
			LOG,
			{
				"user": user,
				"purpose": "Practice",
				"creation": (">=", add_to_date(now_datetime(), seconds=-60)),
			},
		)
		if recent >= int(s.runner_runs_per_minute or 10):
			frappe.throw(_("Too many runs. Wait a minute and try again."), RunnerError)

	payload = {
		"source_code": _b64(code),
		"language_id": langs[language],
		"stdin": _b64(stdin),
		"cpu_time_limit": flt(s.runner_cpu_seconds) or 5,
		"wall_time_limit": flt(s.runner_wall_seconds) or 10,
		"memory_limit": int(s.runner_memory_mb or 256) * 1024,
		"max_file_size": 1024,
		"enable_network": False,
	}
	log = {
		"language": language,
		"purpose": purpose,
		"user": user,
		"code_hash": hashlib.sha256(code.encode()).hexdigest(),
	}
	if reference:
		log.update(reference_doctype=reference[0], reference_name=reference[1])
	try:
		data = _post(s, payload)
	except RunnerError as e:
		_log({**log, "status": "Error", "error": str(e)})
		frappe.db.commit()  # keep the failed attempt in the log even though the request fails
		frappe.throw(str(e), RunnerError)

	status = STATUS.get(int((data.get("status") or {}).get("id") or 0), "Error")
	output = _unb64(data.get("stdout"))[:MAX_OUTPUT_CHARS]
	error = (_unb64(data.get("compile_output")) or _unb64(data.get("stderr")) or data.get("message") or "")[
		:4000
	]
	if status == "Error" and not error:
		error = (data.get("status") or {}).get("description") or ""
	result = {
		"status": status,
		"output": output,
		"error": error,
		"time_ms": round(flt(data.get("time")) * 1000, 1),
		"memory_kb": int(data.get("memory") or 0),
	}
	_log({**log, **result})
	return result


def _log(values: dict):
	frappe.get_doc({"doctype": LOG, **values}).insert(ignore_permissions=True)


def grade_output(item, code: str, user: str, reference=None) -> str | None:
	"""Output of the learner's code run on the runner (setup code first), or None when the runner
	could not run it (the answer then goes to manual review instead of being marked wrong)."""
	source = ((item.get("setup_code") or "") + "\n" + (code or "")).strip("\n")
	try:
		result = run(item["code_language"], source, user, purpose="Grading", reference=reference)
	except RunnerError:
		return None
	if result["status"] == "Error":
		return None
	return result["output"] if result["status"] == "Finished" else ""


def grade_cases(item, code: str, user: str, reference=None) -> list[bool] | None:
	"""Run the learner's code once per test case (its input on stdin); None when the runner failed."""
	from vintraxo_tcd.core.assessment import _norm_output

	source = ((item.get("setup_code") or "") + "\n" + (code or "")).strip("\n")
	out = []
	for case in item.get("test_cases") or []:
		try:
			result = run(
				item["code_language"],
				source,
				user,
				purpose="Grading",
				stdin=case["input"],
				reference=reference,
			)
		except RunnerError:
			return None
		if result["status"] == "Error":
			return None
		out.append(
			result["status"] == "Finished"
			and _norm_output(result["output"]) == _norm_output(case["expected_output"])
		)
	return out


def test_connection() -> dict:
	"""Ask the runner for its version and languages; report configured ids that it does not know."""
	s = settings()
	if not s.get("runner_enabled"):
		frappe.throw(_("The code runner is turned off."), RunnerError)
	try:
		about = requests.get(f"{s.runner_url}/about", headers=_headers(s), timeout=10, allow_redirects=False)
		langs = requests.get(
			f"{s.runner_url}/languages", headers=_headers(s), timeout=10, allow_redirects=False
		)
		about.raise_for_status()
		langs.raise_for_status()
		available = {int(x["id"]): x.get("name") for x in langs.json()}
	except (requests.RequestException, ValueError, KeyError, TypeError) as e:
		frappe.log_error(title="TCD code runner test failed")
		frappe.throw(_("Cannot reach the code runner: {0}").format(type(e).__name__), RunnerError)
	unknown = [f"{lang} ({lid})" for lang, lid in languages(s).items() if lid not in available]
	return {"version": (about.json() or {}).get("version"), "unknown": unknown, "available": len(available)}
