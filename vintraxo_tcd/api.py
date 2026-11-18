"""Public whitelisted API. Keep thin: permission check + delegate to services/controllers."""

import frappe

from vintraxo_tcd.core import content as svc_content
from vintraxo_tcd.core import progress
from vintraxo_tcd.core import quiz as svc_quiz
from vintraxo_tcd.core.search import search

# keep in sync with the TCD Settings field defaults
DEFAULT_PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/"
DEFAULT_SQLJS_URL = "https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/"


@frappe.whitelist(methods=["POST"])
def set_content_status(name: str, status: str) -> dict:
	"""Move content through the review workflow (rules enforced in TCD Content.validate)."""
	doc = frappe.get_doc("TCD Content", name)
	doc.check_permission("write")
	doc.status = status
	doc.save()
	return {"name": doc.name, "status": doc.status, "current_version": doc.current_version}


@frappe.whitelist()
def search_content(query: str, space: str | None = None, limit: int = 20) -> list[dict]:
	"""Arabic-normalized, ranked search over content the user can read."""
	return search(query, space=space, limit=limit)


# ---------------------------------------------------------------- P2: learning


def _readable_content(name: str):
	doc = frappe.get_doc("TCD Content", name)
	doc.check_permission("read")
	return doc


def playground_config() -> dict:
	settings = frappe.get_cached_doc("TCD Settings")
	return {
		"enabled": bool(settings.enable_playgrounds),
		"timeout_seconds": settings.playground_timeout_seconds or 5,
		"pyodide_index_url": settings.pyodide_index_url or DEFAULT_PYODIDE_URL,
		"sqljs_base_url": settings.sqljs_base_url or DEFAULT_SQLJS_URL,
	}


@frappe.whitelist()
def get_lesson(name: str, tutorial: str | None = None) -> dict:
	"""Everything a learner page needs for one lesson/article (read-only, no side effects)."""
	doc = _readable_content(name)
	user = frappe.session.user
	playground = playground_config()
	blocks = svc_content.parse_blocks(doc.blocks)
	if not playground["enabled"]:
		blocks = [b for b in blocks if b.get("type") != "playground"]

	quiz = frappe.db.get_value(
		"TCD Quiz", {"content": doc.name, "is_active": 1}, ["name", "title"], as_dict=True
	)
	out = {
		"name": doc.name,
		"title": doc.title,
		"slug": doc.slug,
		"content_type": doc.content_type,
		"language": doc.language,
		"direction": "rtl" if doc.language == "ar" else "ltr",
		"summary": doc.summary,
		"blocks": blocks,
		"space": doc.space,
		"playground": playground,
		"quiz": quiz
		and {"name": quiz.name, "title": quiz.title, "passed": progress.has_passed(user, quiz.name)},
		"progress": frappe.db.get_value("TCD Progress", {"user": user, "content": doc.name}, "status")
		or "Not Started",
	}
	if doc.content_type == "Tutorial":
		out["tutorial"] = progress.tutorial_summary(user, doc.name)
	elif tutorial:
		summary = progress.tutorial_summary(user, _readable_content(tutorial).name)
		ids = [lesson["lesson"] for lesson in summary["lessons"]]
		if doc.name in ids:
			i = ids.index(doc.name)
			out["prev"] = ids[i - 1] if i > 0 else None
			out["next"] = ids[i + 1] if i + 1 < len(ids) else None
	return out


@frappe.whitelist(methods=["POST"])
def track_view(name: str) -> dict:
	doc = _readable_content(name)
	p = progress.track_view(frappe.session.user, doc.name)
	return {"status": p.status, "percent": p.percent}


@frappe.whitelist(methods=["POST"])
def complete_lesson(name: str) -> dict:
	doc = _readable_content(name)
	p = progress.complete(frappe.session.user, doc.name)
	return {"status": p.status, "percent": p.percent}


@frappe.whitelist()
def get_tutorial_progress(name: str) -> dict:
	doc = _readable_content(name)
	return progress.tutorial_summary(frappe.session.user, doc.name)


def _quiz_for_user(name: str):
	"""Learners have no DocPerm on TCD Quiz (it holds the answers); access follows the content."""
	quiz = frappe.get_doc("TCD Quiz", name)
	_readable_content(quiz.content)
	if not quiz.is_active:
		frappe.throw(frappe._("This quiz is not active."))
	return quiz


@frappe.whitelist()
def get_quiz(name: str) -> dict:
	return svc_quiz.learner_payload(_quiz_for_user(name), frappe.session.user)


@frappe.whitelist(methods=["POST"])
def submit_quiz(name: str, answers) -> dict:
	return svc_quiz.grade(_quiz_for_user(name), frappe.session.user, answers)
