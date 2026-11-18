"""Public whitelisted API. Keep thin: permission check + delegate to services/controllers."""

import frappe

from vintraxo_tcd.core import content as svc_content
from vintraxo_tcd.core import courses, progress
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


# ---------------------------------------------------------------- Phase 1: courses & enrollment


def _readable(doctype: str, name: str):
	doc = frappe.get_doc(doctype, name)
	doc.check_permission("read")
	return doc


@frappe.whitelist()
def get_course(name: str) -> dict:
	"""Course outline with the learner's state (completed / locked per item, chapter percent)."""
	course = _readable("TCD Course", name)
	user = frappe.session.user
	state = courses.course_status(user, course.name)
	visible = []
	for ch in state["chapters"]:
		items = []
		for item in ch["items"]:
			content = frappe.get_doc("TCD Content", item["content"])
			if not frappe.has_permission("TCD Content", "read", content):
				continue
			items.append(
				{**item, "title": content.title, "slug": content.slug, "content_type": content.content_type}
			)
		visible.append({**ch, "items": items})
	enrollment = frappe.db.get_value(
		"TCD Enrollment",
		{"user": user, "course": course.name},
		["name", "status", "percent", "score"],
		as_dict=True,
	)
	return {
		"name": course.name,
		"title": course.title,
		"slug": course.slug,
		"space": course.space,
		"summary": course.summary,
		"completion_rule": course.completion_rule,
		"minimum_score": course.minimum_score,
		"self_enrollment": bool(course.self_enrollment),
		"chapters": visible,
		"percent": state["percent"],
		"score": state["score"],
		"enrollment": enrollment,
	}


@frappe.whitelist()
def get_learning_path(name: str) -> dict:
	path = _readable("TCD Learning Path", name)
	user = frappe.session.user
	state = courses.path_status(user, path.name)
	items = []
	for c in state["courses"]:
		course = frappe.get_doc("TCD Course", c["course"])
		if not frappe.has_permission("TCD Course", "read", course):
			continue
		items.append({**c, "title": course.title, "slug": course.slug})
	enrollment = frappe.db.get_value(
		"TCD Enrollment",
		{"user": user, "learning_path": path.name},
		["name", "status", "percent"],
		as_dict=True,
	)
	return {
		"name": path.name,
		"title": path.title,
		"slug": path.slug,
		"space": path.space,
		"summary": path.summary,
		"completion_rule": path.completion_rule,
		"self_enrollment": bool(path.self_enrollment),
		"courses": items,
		"percent": state["percent"],
		"enrollment": enrollment,
	}


@frappe.whitelist(methods=["POST"])
def enroll(enrollment_for: str, name: str) -> dict:
	"""Self-enrollment of the current user."""
	if enrollment_for not in courses.OFFERINGS:
		frappe.throw(frappe._("Invalid enrollment type."))
	doctype = courses.OFFERINGS[enrollment_for][0]
	doc = _readable(doctype, name)
	if not doc.self_enrollment:
		frappe.throw(
			frappe._("Self enrollment is not allowed here. Ask your instructor."), frappe.PermissionError
		)
	e = courses.enroll(frappe.session.user, enrollment_for, doc.name)
	return {"name": e.name, "status": e.status, "percent": e.percent}


@frappe.whitelist(methods=["POST"])
def enroll_group(student_group: str, enrollment_for: str, name: str, due_date: str | None = None) -> dict:
	"""Staff: enroll every member of a student group."""
	if not frappe.has_permission("TCD Enrollment", "create"):
		frappe.throw(frappe._("Not permitted"), frappe.PermissionError)
	group = _readable("TCD Student Group", student_group)
	doctype = courses.OFFERINGS[enrollment_for][0]
	target = _readable(doctype, name)
	enrolled, skipped = [], []
	for row in group.members:
		frappe.db.savepoint("tcd_enroll_member")
		try:
			courses.enroll(row.user, enrollment_for, target.name, group.name, due_date)
			enrolled.append(row.user)
		except frappe.ValidationError as e:
			frappe.db.rollback(save_point="tcd_enroll_member")
			frappe.clear_last_message()
			skipped.append({"user": row.user, "reason": frappe.utils.strip_html(str(e))})
	return {"enrolled": enrolled, "skipped": skipped}


@frappe.whitelist(methods=["POST"])
def approve_enrollment(name: str) -> dict:
	doc = frappe.get_doc("TCD Enrollment", name)
	doc.check_permission("write")
	roles = set(frappe.get_roles())
	if not roles & {"TCD Instructor", "TCD Administrator", "System Manager"}:
		frappe.throw(frappe._("Only an instructor can approve completion."), frappe.PermissionError)
	doc = courses.approve(doc.name)
	return {"name": doc.name, "status": doc.status}
