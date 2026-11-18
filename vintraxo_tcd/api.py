"""Public whitelisted API. Keep thin: permission check + delegate to services/controllers."""

import frappe

from vintraxo_tcd.core import assignments as svc_assignments
from vintraxo_tcd.core import content as svc_content
from vintraxo_tcd.core import courses, progress
from vintraxo_tcd.core import dashboards as svc_dashboards
from vintraxo_tcd.core import quiz as svc_quiz
from vintraxo_tcd.core.permissions import is_instructor_of
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
	assignment_name = frappe.db.get_value("TCD Assignment", {"content": doc.name, "is_active": 1})
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
		"lesson_type": doc.lesson_type,
		"assignment": assignment_name and get_assignment(assignment_name),
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
		"access": course.access,
		"rating": course_rating(course.name),
		"my_feedback": frappe.db.get_value(
			"TCD Course Feedback", {"course": course.name, "user": user}, ["rating", "comment"], as_dict=True
		),
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
def enroll_batch(batch: str, enrollment_for: str, name: str, due_date: str | None = None) -> dict:
	"""Staff: enroll every member of a batch."""
	if not frappe.has_permission("TCD Enrollment", "create"):
		frappe.throw(frappe._("Not permitted"), frappe.PermissionError)
	group = _readable("TCD Batch", batch)
	doctype = courses.OFFERINGS[enrollment_for][0]
	target = _readable(doctype, name)
	field = courses.OFFERINGS[enrollment_for][1]
	if not is_instructor_of(frappe.session.user, **{field if field == "course" else "path": target.name}):
		frappe.throw(
			frappe._("Only an instructor of this course can enroll a batch."), frappe.PermissionError
		)
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
	if not is_instructor_of(frappe.session.user, doc.course, doc.learning_path):
		frappe.throw(
			frappe._("Only an instructor of this course can approve completion."), frappe.PermissionError
		)
	doc = courses.approve(doc.name)
	return {"name": doc.name, "status": doc.status}


# ---------------------------------------------------------------- assignments, feedback, dashboards


@frappe.whitelist()
def get_assignment(name: str) -> dict:
	assignment = _readable("TCD Assignment", name)
	mine = frappe.db.get_value(
		"TCD Assignment Submission",
		{"assignment": assignment.name, "user": frappe.session.user},
		[
			"name",
			"status",
			"score",
			"passed",
			"feedback",
			"answer_text",
			"attachment",
			"submitted_on",
			"is_late",
		],
		as_dict=True,
	)
	return {
		"name": assignment.name,
		"title": assignment.title,
		"instructions": assignment.instructions,
		"submission_type": assignment.submission_type,
		"due_date": assignment.due_date,
		"max_score": assignment.max_score,
		"pass_score": assignment.pass_score,
		"allowed_extensions": assignment.allowed_extensions,
		"submission": mine,
	}


@frappe.whitelist(methods=["POST"])
def submit_assignment(name: str, answer_text: str | None = None, attachment: str | None = None) -> dict:
	assignment = _readable("TCD Assignment", name)
	doc = svc_assignments.submit(assignment, frappe.session.user, answer_text, attachment)
	if doc.attachment:
		# course instructors open the private file through the submission they can read
		file_name = frappe.db.get_value("File", {"file_url": doc.attachment, "owner": doc.user})
		if file_name:
			frappe.db.set_value(
				"File",
				file_name,
				{
					"attached_to_doctype": "TCD Assignment Submission",
					"attached_to_name": doc.name,
					"attached_to_field": "attachment",
				},
			)
	return {"name": doc.name, "status": doc.status, "is_late": doc.is_late}


@frappe.whitelist(methods=["POST"])
def grade_submission(
	name: str, action: str = "Graded", score: float | None = None, feedback: str | None = None
) -> dict:
	doc = frappe.get_doc("TCD Assignment Submission", name)
	doc.check_permission("read")
	if not frappe.has_permission("TCD Assignment Submission", "write", doc) or not is_instructor_of(
		frappe.session.user, doc.course
	):
		frappe.throw(frappe._("Only an instructor of this course can grade."), frappe.PermissionError)
	doc = svc_assignments.grade(doc, score, feedback, action)
	return {"name": doc.name, "status": doc.status, "score": doc.score, "passed": doc.passed}


def course_rating(course: str) -> dict:
	rows = frappe.get_all(
		"TCD Course Feedback", filters={"course": course}, pluck="rating", ignore_permissions=True
	)
	return {"average": round(sum(rows) / len(rows), 1) if rows else None, "count": len(rows)}


@frappe.whitelist(methods=["POST"])
def rate_course(name: str, rating: int, comment: str | None = None) -> dict:
	course = _readable("TCD Course", name)
	user = frappe.session.user
	if not frappe.db.exists(
		"TCD Enrollment", {"user": user, "course": course.name, "status": ("!=", "Withdrawn")}
	):
		frappe.throw(frappe._("Enroll in the course before rating it."), frappe.PermissionError)
	existing = frappe.db.get_value("TCD Course Feedback", {"course": course.name, "user": user})
	doc = (
		frappe.get_doc("TCD Course Feedback", existing) if existing else frappe.new_doc("TCD Course Feedback")
	)
	doc.update(
		{
			"course": course.name,
			"user": user,
			"rating": int(rating),
			"comment": (comment or "").strip()[:2000],
		}
	)
	doc.flags.from_api = True
	doc.save(ignore_permissions=True)
	return {"rating": course_rating(course.name)}


@frappe.whitelist()
def my_learning() -> dict:
	return svc_dashboards.my_learning(frappe.session.user)


@frappe.whitelist()
def instructor_dashboard() -> dict:
	return svc_dashboards.instructor_dashboard(frappe.session.user)
