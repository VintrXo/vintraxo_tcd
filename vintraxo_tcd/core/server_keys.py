"""Fill every key of a new server from one JSON file (ADR-0034).

    bench --site <site> execute vintraxo_tcd.core.server_keys.apply_keys --kwargs "{'path': '/path/keys.json'}"

The file follows deploy/keys.example.json. Empty values and values that still start with "REPLACE" are
skipped, so the owner can fill only what they have and run it again later. Each section is applied on
its own: one bad key does not stop the others. Secrets are never printed. Runs only from the command
line (bench execute), never over HTTP."""

import json

import frappe
from frappe import _

TRIAL_ACCOUNTS = (
	"learner1@vintraxo.local",
	"learner2@vintraxo.local",
	"learner3@vintraxo.local",
	"author@vintraxo.local",
	"instructor@vintraxo.local",
)


def _filled(value) -> bool:
	if value is None:
		return False
	if isinstance(value, str):
		return bool(value.strip()) and not value.strip().upper().startswith("REPLACE")
	return True


def _clean(section: dict | None) -> dict:
	return {k: v for k, v in (section or {}).items() if _filled(v) and not k.startswith("_")}


def _update_single(doctype: str, values: dict) -> list[str]:
	doc = frappe.get_single(doctype)
	doc.update(values)
	doc.save(ignore_permissions=True)
	return sorted(values)


def _email(v: dict) -> list[str]:
	if not v.get("email_id"):
		return []
	name = v.get("email_account_name") or v["email_id"]
	values = {
		"email_id": v["email_id"],
		"email_account_name": name,
		"enable_outgoing": 1,
		"default_outgoing": 1,
		"smtp_server": v.get("smtp_server"),
		"smtp_port": v.get("smtp_port") or 587,
		"use_tls": int(v.get("use_tls", 1)),
		"use_ssl_for_outgoing": int(v.get("use_ssl", 0)),
		"password": v.get("password"),
	}
	if v.get("login_id"):
		values.update({"login_id_is_different": 1, "login_id": v["login_id"]})
	values = {k: val for k, val in values.items() if _filled(val)}
	if frappe.db.exists("Email Account", name):
		doc = frappe.get_doc("Email Account", name)
		doc.update(values)
		doc.save(ignore_permissions=True)
	else:
		frappe.get_doc({"doctype": "Email Account", **values}).insert(ignore_permissions=True)
	return sorted(k for k in values if k != "password") + (["password"] if "password" in values else [])


def _ai(v: dict) -> list[str]:
	if not v.get("api_key"):
		return []
	values = {"enabled": 1, "api_key": v["api_key"]}
	for key in ("provider", "model", "monthly_budget", "daily_requests_per_user"):
		if key in v:
			values[key] = v[key]
	return _update_single("TCD AI Settings", values)


def _runner(v: dict) -> list[str]:
	if not v.get("url"):
		return []
	values = {"runner_enabled": 1, "runner_url": v["url"]}
	if v.get("token"):
		values["runner_token"] = v["token"]
	return _update_single("TCD Settings", values)


def _zoom(v: dict) -> list[str]:
	needed = ("account_id", "client_id", "client_secret")
	if not all(v.get(k) for k in needed):
		return []
	return _update_single(
		"TCD Settings",
		{
			"meeting_provider": "Zoom",
			"zoom_account_id": v["account_id"],
			"zoom_client_id": v["client_id"],
			"zoom_client_secret": v["client_secret"],
		},
	)


def _google_meet(v: dict) -> list[str]:
	if not v.get("google_calendar"):
		return []
	if not frappe.db.exists("Google Calendar", v["google_calendar"]):
		frappe.throw(
			_("Google Calendar {0} does not exist. Connect it from the Desk first.").format(
				v["google_calendar"]
			)
		)
	return _update_single(
		"TCD Settings", {"meeting_provider": "Google Meet", "google_calendar": v["google_calendar"]}
	)


def _payment(v: dict) -> list[str]:
	if not v.get("gateway"):
		return []
	if frappe.db.exists("DocType", "Payment Gateway") and not frappe.db.exists(
		"Payment Gateway", v["gateway"]
	):
		frappe.throw(_("Payment Gateway {0} does not exist.").format(v["gateway"]))
	return _update_single("TCD Settings", {"payment_gateway": v["gateway"]})


def _github(spaces: dict) -> list[str]:
	done = []
	for space, v in spaces.items():
		v = _clean(v)
		if not (v.get("repo") and v.get("token")):
			continue
		doc = frappe.get_doc("TCD Space", space)
		doc.update({"github_repo": v["repo"], "github_token": v["token"]})
		if v.get("branch"):
			doc.github_branch = v["branch"]
		doc.save(ignore_permissions=True)
		done.append(space)
	return done


def _documents(docs: list) -> list[str]:
	"""Keys kept by other apps (payment gateway settings, Google Settings…): {"doctype", "name"?, fields}."""
	done = []
	for d in docs or []:
		values = _clean({k: v for k, v in d.items() if k not in ("doctype", "name")})
		if not (d.get("doctype") and any(isinstance(v, str) for v in values.values())):
			continue  # only switches/numbers filled in: nothing real to save yet
		meta = frappe.get_meta(d["doctype"])
		if meta.issingle:
			doc = frappe.get_single(d["doctype"])
		elif d.get("name") and frappe.db.exists(d["doctype"], d["name"]):
			doc = frappe.get_doc(d["doctype"], d["name"])
		else:
			doc = frappe.new_doc(d["doctype"])
			if d.get("name"):
				doc.name = d["name"]
		doc.update(values)
		doc.save(ignore_permissions=True)
		done.append(f"{d['doctype']} {doc.name}")
	return done


def _trial_accounts(action) -> list[str]:
	if action != "disable":
		return []
	done = []
	for user in TRIAL_ACCOUNTS:
		if frappe.db.get_value("User", user, "enabled"):
			frappe.db.set_value("User", user, "enabled", 0)
			done.append(user)
	return done


SECTIONS = (
	("email", _email),
	("ai", _ai),
	("runner", _runner),
	("zoom", _zoom),
	("google_meet", _google_meet),
	("payment", _payment),
	("github", None),
	("documents", None),
	("trial_accounts", None),
)


def apply(data: dict) -> dict:
	"""Returns {section: {"status": "set"|"skipped"|"failed", "keys": [...], "error": str}}."""
	report = {}
	for section, fn in SECTIONS:
		raw = data.get(section)
		frappe.db.savepoint("tcd_keys")
		try:
			if section == "github":
				keys = _github({k: v for k, v in (raw or {}).items() if not k.startswith("_")})
			elif section == "documents":
				keys = _documents(raw)
			elif section == "trial_accounts":
				keys = _trial_accounts(raw)
			else:
				keys = fn(_clean(raw))
			if keys:
				frappe.db.commit()
			report[section] = {"status": "set" if keys else "skipped", "keys": keys}
		except Exception as e:
			frappe.db.rollback(save_point="tcd_keys")  # undo this section only
			frappe.clear_messages()
			report[section] = {"status": "failed", "keys": [], "error": str(e)[:300]}
	return report


def apply_keys(path: str):
	if getattr(frappe.local, "request", None):  # command line only
		raise frappe.PermissionError
	with open(path, encoding="utf-8") as f:
		data = json.load(f)
	frappe.set_user("Administrator")
	report = apply(data)
	for section, r in report.items():
		line = f"[{r['status'].upper():7}] {section}"
		if r["keys"]:
			line += ": " + ", ".join(r["keys"])
		if r.get("error"):
			line += f"  ->  {r['error']}"
		print(line)
	from vintraxo_tcd.core import ops

	print()
	ops.print_readiness()
	return report
