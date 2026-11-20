"""Public whitelisted API. Keep thin: permission check + delegate to services/controllers."""

import frappe

from vintraxo_tcd.core import assignments as svc_assignments
from vintraxo_tcd.core import connect, courses, progress, wiki
from vintraxo_tcd.core import content as svc_content
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


def runner_languages() -> set:
	from vintraxo_tcd.core import runner

	return set(runner.languages())


def playground_config() -> dict:
	settings = frappe.get_cached_doc("TCD Settings")
	return {
		"enabled": bool(settings.enable_playgrounds),
		"timeout_seconds": settings.playground_timeout_seconds or 5,
		"pyodide_index_url": settings.pyodide_index_url or DEFAULT_PYODIDE_URL,
		"sqljs_base_url": settings.sqljs_base_url or DEFAULT_SQLJS_URL,
		"runner_languages": sorted(runner_languages()),
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
	opens = courses.drip_lock(user, doc.name)
	if opens:  # Phase 20: held back by the course schedule
		out.update({"blocks": [], "quiz": None, "assignment": None, "opens_on": str(opens)})
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
	if courses.drip_lock(frappe.session.user, quiz.content):
		frappe.throw(frappe._("This lesson is not open yet."), frappe.PermissionError)
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


def _intro(url: str | None) -> dict | None:
	if not url:
		return None
	from vintraxo_tcd.core import media

	try:
		provider, embed_url = media.parse_video(url)
	except frappe.ValidationError:
		return None  # a link that is no longer allowed is simply not shown
	return {"provider": provider, "embed_url": embed_url}


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
		{"user": user, "course": course.name, "status": ("!=", "Withdrawn")},
		["name", "status", "percent", "score", "mandatory"],
		as_dict=True,
	)
	return {
		"name": course.name,
		"title": course.title,
		"slug": course.slug,
		"space": course.space,
		"summary": course.summary,
		"cover_image": course.get("cover_image"),
		"paid": bool(course.get("paid")),
		"price": course.get("price"),
		"currency": course.get("currency"),
		"intro": _intro(course.get("intro_video")),
		"completion_rule": course.completion_rule,
		"minimum_score": course.minimum_score,
		"self_enrollment": bool(course.self_enrollment),
		"chapters": visible,
		"percent": state["percent"],
		"score": state["score"],
		"attendance": state.get("attendance"),
		"minimum_attendance": state.get("minimum_attendance"),
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
		{"user": user, "learning_path": path.name, "status": ("!=", "Withdrawn")},
		["name", "status", "percent", "mandatory"],
		as_dict=True,
	)
	return {
		"name": path.name,
		"title": path.title,
		"slug": path.slug,
		"space": path.space,
		"summary": path.summary,
		"cover_image": path.get("cover_image"),
		"paid": bool(path.get("paid")),
		"price": path.get("price"),
		"currency": path.get("currency"),
		"intro": _intro(path.get("intro_video")),
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
	if doc.get("paid"):
		frappe.throw(frappe._("This is a paid course. Use Buy."), frappe.PermissionError)
	if doc.get("coming_soon"):
		frappe.throw(frappe._("This course opens soon. Ask to be notified."), frappe.PermissionError)
	if not doc.self_enrollment:
		frappe.throw(
			frappe._("Self enrollment is not allowed here. Ask your instructor."), frappe.PermissionError
		)
	if doctype == "TCD Course":
		unmet = connect.unmet_course_prerequisites(frappe.session.user, doc.name)
		if unmet:
			frappe.throw(frappe._("Complete these courses first: {0}").format(", ".join(unmet)))
	e = courses.enroll(frappe.session.user, enrollment_for, doc.name)
	return {"name": e.name, "status": e.status, "percent": e.percent}


@frappe.whitelist(methods=["POST"])
def withdraw(enrollment_for: str, name: str) -> dict:
	"""The current user leaves a course or path (not mandatory, not completed)."""
	if enrollment_for not in courses.OFFERINGS:
		frappe.throw(frappe._("Invalid enrollment type."))
	field = courses.OFFERINGS[enrollment_for][1]
	enrollment = frappe.db.get_value(
		"TCD Enrollment", {"user": frappe.session.user, field: name, "status": ("!=", "Withdrawn")}
	)
	if not enrollment:
		raise frappe.DoesNotExistError
	doc = frappe.get_doc("TCD Enrollment", enrollment)
	if doc.mandatory:
		frappe.throw(frappe._("This training is mandatory. Ask your administrator."), frappe.PermissionError)
	if doc.status == "Completed":
		frappe.throw(frappe._("You already completed it."))
	doc.status = "Withdrawn"
	doc.save(ignore_permissions=True)
	return {"status": doc.status}


@frappe.whitelist(methods=["POST"])
def confirm_content_review(name: str) -> dict:
	from vintraxo_tcd.core import freshness

	return freshness.confirm_review(name)


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
	enrolled, skipped, warnings = [], [], []
	for row in group.members:
		frappe.db.savepoint("tcd_enroll_member")
		try:
			courses.enroll(row.user, enrollment_for, target.name, group.name, due_date)
			enrolled.append(row.user)
			if doctype == "TCD Course" and (
				unmet := connect.unmet_course_prerequisites(row.user, target.name)
			):
				warnings.append({"user": row.user, "missing": unmet})
		except frappe.ValidationError as e:
			frappe.db.rollback(save_point="tcd_enroll_member")
			frappe.clear_last_message()
			skipped.append({"user": row.user, "reason": frappe.utils.strip_html(str(e))})
	return {"enrolled": enrolled, "skipped": skipped, "warnings": warnings}


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


# ---------------------------------------------------------------- Phase 2: unified experience


@frappe.whitelist()
def search_all(query: str, types: str | None = None, space: str | None = None, limit: int = 30) -> list:
	"""Unified, permission-filtered search over content, courses and learning paths."""
	wanted = [t for t in (types or "").split(",") if t] or None
	return connect.search_all(query, wanted, space, limit)


@frappe.whitelist()
def get_related(name: str) -> dict:
	doc = _readable_content(name)
	return connect.related_for_content(frappe.session.user, doc.name)


@frappe.whitelist()
def get_recommendations(limit: int = 6) -> list:
	return connect.recommendations(frappe.session.user, int(limit or 6))


# ---------------------------------------------------------------- Phase 3: wiki


@frappe.whitelist()
def compare_versions(old: str, new: str) -> dict:
	"""Diff two versions, or a version and the current content (pass the content name)."""
	for name in (old, new):
		target = frappe.db.get_value("TCD Content Version", name, "content") or name
		_readable_content(target)
	if not frappe.has_permission("TCD Content Version", "read"):
		frappe.throw(frappe._("Not permitted"), frappe.PermissionError)
	return wiki.compare(old, new)


@frappe.whitelist(methods=["POST"])
def restore_version(name: str) -> dict:
	version = frappe.get_doc("TCD Content Version", name)
	version.check_permission("read")
	doc = wiki.restore(version.name)
	return {"name": doc.name, "status": doc.status}


@frappe.whitelist(methods=["POST"])
def content_feedback(name: str, helpful: int, comment: str | None = None) -> dict:
	doc = _readable_content(name)
	wiki.give_feedback(doc.name, frappe.session.user, bool(int(helpful)), comment)
	return wiki.feedback_stats(doc.name)


@frappe.whitelist()
def get_templates(content_type: str | None = None) -> list:
	filters = {"content_type": content_type} if content_type else {}
	return frappe.get_list(
		"TCD Content Template", filters=filters, fields=["name", "content_type", "lesson_type", "description"]
	)


@frappe.whitelist()
def get_template(name: str) -> dict:
	doc = frappe.get_doc("TCD Content Template", name)
	doc.check_permission("read")
	return {"blocks": doc.blocks, "content_type": doc.content_type, "lesson_type": doc.lesson_type}


# ---------------------------------------------------------------- Phase 4: assessments


@frappe.whitelist(methods=["POST"])
def start_quiz(name: str) -> dict:
	"""Open (or resume) a timed / randomized attempt and return its questions."""
	quiz = _quiz_for_user(name)
	svc_quiz.start(quiz, frappe.session.user)
	return svc_quiz.learner_payload(quiz, frappe.session.user)


def _can_review(sub) -> bool:
	from vintraxo_tcd.core.permissions import is_admin

	user = frappe.session.user
	if is_admin(user) or "TCD Content Reviewer" in frappe.get_roles(user):
		return True
	return any(is_instructor_of(user, course) for course in courses.courses_with_content(sub.content))


@frappe.whitelist(methods=["POST"])
def review_quiz_submission(name: str, reviews) -> dict:
	"""Manual grading: reviews = {question_id: {"points": n} | {"rubric": {criterion: n}}, "feedback": "..."}"""
	sub = frappe.get_doc("TCD Quiz Submission", name)
	if not frappe.has_permission("TCD Quiz Submission", "read", sub) or not _can_review(sub):
		frappe.throw(
			frappe._("Only an instructor of this course or a reviewer can grade."), frappe.PermissionError
		)
	return svc_quiz.review(sub, reviews, frappe.session.user)


@frappe.whitelist()
def get_review_items(name: str) -> list:
	"""Pending manual items of a submission with the learner's answers and the rubric."""
	sub = frappe.get_doc("TCD Quiz Submission", name)
	if not frappe.has_permission("TCD Quiz Submission", "read", sub) or not _can_review(sub):
		frappe.throw(frappe._("Not permitted"), frappe.PermissionError)
	import json as _json

	from vintraxo_tcd.core import assessment

	quiz = frappe.get_doc("TCD Quiz", sub.quiz)
	answers = _json.loads(sub.answers or "{}")
	out = []
	for ref in _json.loads(sub.paper or "[]"):
		item = assessment.load_item(ref["key"], ref["source"], quiz)
		if item and assessment.is_manual(item):
			r = assessment.grade_item(item, answers.get(item["key"]))
			out.append(
				{
					"id": item["key"],
					"type": item["type"],
					"question": item["question"],
					"points": item["points"],
					"rubric": item["rubric"],
					"answer": answers.get(item["key"]),
					"auto_hint": r.get("auto_hint"),
					"expected_output": item.get("expected_output"),
				}
			)
	return out


# ---------------------------------------------------------------- Phase 5: skills and certificates


@frappe.whitelist()
def my_credentials() -> dict:
	user = frappe.session.user
	certs = frappe.get_list(
		"TCD Certificate",
		filters={"user": user},
		fields=["name", "title", "status", "issued_on", "expires_on", "verification_code"],
		order_by="issued_on desc",
	)
	skills = frappe.get_list(
		"TCD User Skill",
		filters={"user": user},
		fields=["skill", "level", "source_type", "source_name"],
		order_by="skill asc",
	)
	return {"certificates": certs, "skills": skills}


def _can_manage_certificate(cert) -> bool:
	return is_instructor_of(frappe.session.user, cert.course, cert.learning_path)


@frappe.whitelist(methods=["POST"])
def renew_certificate(name: str) -> dict:
	from vintraxo_tcd.core import credentials

	cert = frappe.get_doc("TCD Certificate", name)
	if not frappe.has_permission("TCD Certificate", "read", cert) or not _can_manage_certificate(cert):
		frappe.throw(
			frappe._("Only an instructor of this course can renew the certificate."), frappe.PermissionError
		)
	new = credentials.renew_certificate(cert.name)
	return {"name": new.name, "expires_on": new.expires_on}


@frappe.whitelist(methods=["POST"])
def revoke_certificate(name: str, reason: str) -> dict:
	from vintraxo_tcd.core import credentials
	from vintraxo_tcd.core.permissions import is_admin

	if not is_admin(frappe.session.user):
		frappe.throw(frappe._("Only an administrator can revoke certificates."), frappe.PermissionError)
	credentials.revoke_certificate(name, reason)
	return {"name": name, "status": "Revoked"}


@frappe.whitelist(allow_guest=True)
def verify_certificate(code: str) -> dict:
	"""Public: minimal certificate facts for a verification code."""
	from vintraxo_tcd.core import credentials

	row = credentials.verify(code)
	if not row:
		frappe.throw(frappe._("Certificate not found."), frappe.DoesNotExistError)
	return {k: row[k] for k in ("full_name", "title", "certificate_for", "issued_on", "expires_on", "status")}


# ---------------------------------------------------------------- Phase 6: governance


def _governance_for_user(code: str):
	from vintraxo_tcd.core import governance

	if not frappe.db.exists("TCD Governance Document", code):
		frappe.throw(frappe._("Document not found."), frappe.DoesNotExistError)
	doc = frappe.get_doc("TCD Governance Document", code)
	if not governance.can_read(doc, frappe.session.user):
		frappe.throw(frappe._("Document not found."), frappe.DoesNotExistError)
	return doc


@frappe.whitelist()
def get_policy(code: str) -> dict:
	"""The latest approved version of a governance document (never the draft being revised)."""
	from vintraxo_tcd.core import governance, wiki

	doc = _governance_for_user(code)
	version = governance.current_version(doc.name)
	if not version:
		frappe.throw(frappe._("This document has no approved version yet."), frappe.DoesNotExistError)
	return {
		"code": doc.name,
		"title": version.title,
		"kind": doc.doc_kind,
		"version": version.version,
		"effective_date": version.effective_date,
		"expiry_date": doc.expiry_date,
		"summary": version.summary,
		"html": wiki.render_markdown(version.body or "", doc.space or ""),
		"attachment": version.attachment,
		"under_revision": doc.status == "Revision",
		"require_acknowledgment": bool(doc.require_acknowledgment),
		"acknowledged": governance.has_acknowledged(frappe.session.user, doc.name, version.version),
	}


@frappe.whitelist(methods=["POST"])
def acknowledge(code: str) -> dict:
	from vintraxo_tcd.core import governance

	doc = _governance_for_user(code)
	ack = governance.acknowledge(doc.name, frappe.session.user)
	return {"version": ack.version, "acknowledged_on": ack.acknowledged_on}


@frappe.whitelist()
def my_policies() -> dict:
	from vintraxo_tcd.core import governance

	docs = governance.documents_for(frappe.session.user)
	return {
		"documents": [
			{
				"code": d.name,
				"title": d.title,
				"kind": d.doc_kind,
				"version": d.version,
				"acknowledged": d.acknowledged,
				"require_acknowledgment": bool(d.require_acknowledgment),
			}
			for d in docs
		]
	}


@frappe.whitelist(methods=["POST"])
def set_governance_status(code: str, status: str) -> dict:
	"""Lifecycle transition. The named approver may activate without write permission on the DocType;
	every other transition needs write permission. Transition rules live in core.governance.validate."""
	doc = frappe.get_doc("TCD Governance Document", code)
	user = frappe.session.user
	is_approver_activation = status == "Active" and doc.status == "Approval" and doc.approver == user
	if not is_approver_activation:
		doc.check_permission("write")
	doc.status = status
	doc.save(ignore_permissions=is_approver_activation)
	return {"name": doc.name, "status": doc.status, "version": doc.version}


# ---------------------------------------------------------------- integrations (Phase 8)


@frappe.whitelist(methods=["POST"])
def test_connector(name: str) -> dict:
	frappe.has_permission("TCD Connector", "write", name, throw=True)
	from vintraxo_tcd.core import integrations

	return integrations.test_connector(name)


@frappe.whitelist(methods=["POST"])
def retry_integration_event(name: str):
	connector = frappe.db.get_value("TCD Integration Event", name, "connector")
	if not connector:
		raise frappe.DoesNotExistError
	frappe.has_permission("TCD Connector", "write", connector, throw=True)
	from vintraxo_tcd.core import integrations

	integrations.retry(name)


@frappe.whitelist(methods=["POST"])
def apply_training_rule(name: str) -> int:
	frappe.has_permission("TCD Training Rule", "write", name, throw=True)
	from vintraxo_tcd.core import training

	return training.apply_rule(name)


# ---------------------------------------------------------------- AI gateway (Phase 9)


@frappe.whitelist()
def ai_status() -> dict:
	from vintraxo_tcd.core import ai

	return {"enabled": ai.can_use(frappe.session.user)}


@frappe.whitelist(methods=["POST"])
def ai_search(query: str, space: str | None = None) -> dict:
	from vintraxo_tcd.core import ai

	return ai.semantic_search(query, frappe.session.user, space)


@frappe.whitelist(methods=["POST"])
def ai_ask(question: str, space: str | None = None) -> dict:
	from vintraxo_tcd.core import ai

	return ai.ask(question, frappe.session.user, space)


@frappe.whitelist(methods=["POST"])
def ai_summarize(content: str) -> dict:
	from vintraxo_tcd.core import ai

	return ai.summarize(content, frappe.session.user)


@frappe.whitelist(methods=["POST"])
def ai_generate_questions(content: str, count: int = 5) -> list:
	from vintraxo_tcd.core import ai

	return ai.generate_questions(content, frappe.session.user, int(count))


@frappe.whitelist(methods=["POST"])
def ai_draft_lesson(space: str, title: str, instructions: str = "", sources=None) -> str:
	from vintraxo_tcd.core import ai

	if isinstance(sources, str):
		sources = frappe.parse_json(sources)
	return ai.draft_lesson(space, title, instructions, frappe.session.user, sources or [])


# ---------------------------------------------------------------- code runner (Phase 10)


@frappe.whitelist(methods=["POST"])
def run_code(language: str, code: str, stdin: str = "") -> dict:
	"""Practice run on the isolated code runner (never on this server)."""
	if frappe.session.user == "Guest":
		raise frappe.PermissionError
	from vintraxo_tcd.core import runner

	return runner.run(language, code, frappe.session.user, purpose="Practice", stdin=stdin)


@frappe.whitelist(methods=["POST"])
def test_runner() -> dict:
	frappe.has_permission("TCD Settings", "write", throw=True)
	from vintraxo_tcd.core import runner

	return runner.test_connection()


# ---------------------------------------------------------------- sessions (Phase 12)


@frappe.whitelist(methods=["POST"])
def load_session_learners(name: str) -> int:
	from vintraxo_tcd.core import sessions

	return sessions.load_learners(name)


@frappe.whitelist()
def course_sessions(course: str) -> dict:
	_readable("TCD Course", course)
	from vintraxo_tcd.core import sessions

	return sessions.for_course(course, frappe.session.user)


# ---------------------------------------------------------------- discussions (Phase 12)


@frappe.whitelist()
def discussion_list(content: str) -> dict:
	from vintraxo_tcd.core import discussions

	return discussions.list_for(content, frappe.session.user)


@frappe.whitelist(methods=["POST"])
def discussion_post(content: str, body: str, thread: str | None = None) -> dict:
	from vintraxo_tcd.core import discussions

	return discussions.post(content, body, frappe.session.user, thread)


@frappe.whitelist(methods=["POST"])
def discussion_accept(name: str):
	from vintraxo_tcd.core import discussions

	discussions.accept(name, frappe.session.user)


@frappe.whitelist(methods=["POST"])
def discussion_hide(name: str, hidden: int = 1):
	from vintraxo_tcd.core import discussions

	discussions.set_hidden(name, hidden, frappe.session.user)


# ---------------------------------------------------------------- manager dashboard (Phase 13)


@frappe.whitelist()
def team_overview(team: str | None = None) -> dict:
	from vintraxo_tcd.core import teams

	return teams.overview(frappe.session.user, team)


# ---------------------------------------------------------------- space export / import (Phase 13)


@frappe.whitelist()
def export_space(space: str):
	"""Download a space as a JSON file (administrators only)."""
	from vintraxo_tcd.core import transfer

	bundle = transfer.export_space(space)
	frappe.response["filename"] = f"tcd-space-{frappe.scrub(space)}-{frappe.utils.nowdate()}.json"
	frappe.response["filecontent"] = frappe.as_json(bundle, indent=1)
	frappe.response["type"] = "download"


@frappe.whitelist(methods=["POST"])
def run_content_import(name: str) -> dict:
	from vintraxo_tcd.core import transfer

	return transfer.run_import(name)


# ---------------------------------------------------------------- video watching (Phase 14)


@frappe.whitelist(methods=["POST"])
def video_progress(content: str, index: int, watched: float, duration: float) -> dict:
	if frappe.session.user == "Guest":
		raise frappe.PermissionError
	_readable_content(content)
	from vintraxo_tcd.core import progress

	return progress.record_video(frappe.session.user, content, index, watched, duration)


# ---------------------------------------------------------------- lesson notes (Phase 14)


@frappe.whitelist(methods=["POST"])
def save_note(content: str, note: str = "") -> dict:
	_readable_content(content)
	from vintraxo_tcd.core import notes

	return notes.save(content, note, frappe.session.user)


# ---------------------------------------------------------------- suggested edits (Phase 14)


@frappe.whitelist(methods=["POST"])
def propose_change(content: str, edits, title: str | None = None, summary: str = "") -> str:
	from vintraxo_tcd.core import change_requests

	return change_requests.propose(content, edits, frappe.session.user, title, summary)


@frappe.whitelist()
def change_request_diff(name: str) -> dict:
	frappe.get_doc("TCD Change Request", name).check_permission("read")
	from vintraxo_tcd.core import change_requests

	return change_requests.diff(name)


@frappe.whitelist(methods=["POST"])
def accept_change_request(name: str, comment: str = "") -> str:
	from vintraxo_tcd.core import change_requests

	return change_requests.accept(name, frappe.session.user, comment)


@frappe.whitelist(methods=["POST"])
def reject_change_request(name: str, comment: str = ""):
	from vintraxo_tcd.core import change_requests

	change_requests.reject(name, frappe.session.user, comment)


# ---------------------------------------------------------------- proctoring (Phase 15)


@frappe.whitelist(methods=["POST"])
def report_quiz_violation(name: str, kind: str) -> dict:
	from vintraxo_tcd.core import quiz as svc_quiz_mod

	return svc_quiz_mod.report_violation(_quiz_for_user(name), frappe.session.user, kind)


# ---------------------------------------------------------------- payments (Phase 16)


@frappe.whitelist()
def price_quote(enrollment_for: str, name: str, coupon: str | None = None) -> dict:
	from vintraxo_tcd.core import courses as _c
	from vintraxo_tcd.core import payments

	_readable(_c.OFFERINGS[enrollment_for][0], name)
	return payments.quote(enrollment_for, name, coupon)


@frappe.whitelist(methods=["POST"])
def checkout(
	enrollment_for: str, name: str, coupon: str | None = None, redirect_to: str | None = None
) -> dict:
	from vintraxo_tcd.core import payments

	safe = redirect_to if (redirect_to or "").startswith("/learn") else "/learn/my"
	return payments.checkout(enrollment_for, name, frappe.session.user, coupon, safe)


# ---------------------------------------------------------------- SCORM (Phase 16)


@frappe.whitelist()
def scorm_data(content: str) -> dict:
	if frappe.session.user == "Guest":
		raise frappe.PermissionError
	_readable_content(content)
	from vintraxo_tcd.core import scorm

	return scorm.get_data(frappe.session.user, content)


@frappe.whitelist(methods=["POST"])
def scorm_commit(content: str, data) -> dict:
	if frappe.session.user == "Guest":
		raise frappe.PermissionError
	doc = _readable_content(content)
	if not doc.get("scorm_launch"):
		frappe.throw(frappe._("This page has no SCORM package."))
	from vintraxo_tcd.core import scorm

	return scorm.commit(frappe.session.user, content, data)


# ---------------------------------------------------------------- GitHub sync (Phase 16)


@frappe.whitelist(methods=["POST"])
def github_push(space: str) -> dict:
	from vintraxo_tcd.core import github_sync

	return github_sync.push(space)


@frappe.whitelist(methods=["POST"])
def github_pull(space: str) -> dict:
	from vintraxo_tcd.core import github_sync

	return github_sync.pull(space)


# ---------------------------------------------------------------- profile and job board (Phase 16)


@frappe.whitelist(methods=["POST"])
def save_profile(data) -> dict:
	from vintraxo_tcd.core import careers

	return careers.save(frappe.session.user, frappe.parse_json(data) if isinstance(data, str) else data)


@frappe.whitelist(methods=["POST"])
def apply_for_job(job: str, cover_note: str = "", resume: str | None = None) -> str:
	from vintraxo_tcd.core import careers

	return careers.apply(job, frappe.session.user, cover_note, resume or None)


# ---------------------------------------------------------------- authoring studio (Phase 18)


@frappe.whitelist(methods=["POST"])
def studio_save_page(data) -> dict:
	from vintraxo_tcd.core import studio

	return studio.save_page(data)


@frappe.whitelist(methods=["POST"])
def studio_save_course(data) -> dict:
	from vintraxo_tcd.core import studio

	return studio.save_course(data)


@frappe.whitelist(methods=["POST"])
def studio_course_status(name: str, status: str) -> dict:
	from vintraxo_tcd.core import studio

	return studio.set_course_status(name, status)


@frappe.whitelist()
def studio_find_pages(query: str = "", space: str | None = None) -> list[dict]:
	from vintraxo_tcd.core import studio

	return studio.find_pages(query, space)


# ---------------------------------------------------------------- certification evaluations (Phase 19)


@frappe.whitelist(methods=["POST"])
def book_evaluation(course: str, evaluator: str, date: str, start_time: str) -> str:
	from vintraxo_tcd.core import evaluations

	return evaluations.book(frappe.session.user, course, evaluator, date, start_time)


@frappe.whitelist(methods=["POST"])
def cancel_evaluation(name: str) -> dict:
	from vintraxo_tcd.core import evaluations

	return evaluations.cancel(frappe.session.user, name)


@frappe.whitelist(methods=["POST"])
def record_evaluation(name: str, result: str, score=None, feedback: str = "") -> dict:
	from vintraxo_tcd.core import evaluations

	return evaluations.record_result(name, frappe.session.user, result, score, feedback)


@frappe.whitelist(methods=["POST"])
def evaluation_meeting(name: str, url: str = "") -> dict:
	from vintraxo_tcd.core import evaluations

	return evaluations.set_meeting_url(name, frappe.session.user, url)


# ---------------------------------------------------------------- coming soon (Phase 20)


@frappe.whitelist(methods=["POST"])
def course_interest(course: str, on: int = 1) -> dict:
	"""Ask (or stop asking) to be notified when a coming-soon course opens."""
	from vintraxo_tcd.core import courses as course_svc

	doc = _readable("TCD Course", course)
	return course_svc.set_interest(frappe.session.user, doc.name, bool(int(on)))
