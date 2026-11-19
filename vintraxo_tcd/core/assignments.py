"""Assignments: submission rules, grading, completion (PLAN Phase 1)."""

import os

import frappe
from frappe import _
from frappe.utils import flt, get_datetime, now_datetime

from vintraxo_tcd.core import courses, media, progress


def validate_assignment(doc):
	if flt(doc.max_score) <= 0:
		frappe.throw(_("Max score must be greater than zero."))
	if not 0 <= flt(doc.pass_score) <= flt(doc.max_score):
		frappe.throw(_("Pass score must be between 0 and the max score."))
	if doc.course and doc.content not in {i["content"] for i in courses.course_items(doc.course)}:
		frappe.throw(_("The lesson is not part of the selected course."))


def _submission_course(assignment, user: str) -> str | None:
	if assignment.course:
		return assignment.course
	candidates = courses.courses_with_content(assignment.content)
	for course in candidates:
		if frappe.db.exists(
			"TCD Enrollment", {"user": user, "course": course, "status": ("!=", "Withdrawn")}
		):
			return course
	return candidates[0] if candidates else None


def _check_extension(assignment, file_url: str):
	allowed = {
		e.strip().lower().lstrip(".") for e in (assignment.allowed_extensions or "").split(",") if e.strip()
	}
	if allowed:
		ext = os.path.splitext(file_url)[1].lower().lstrip(".")
		if ext not in allowed:
			frappe.throw(_("File type .{0} is not allowed for this assignment.").format(ext))


def submit(assignment, user: str, answer_text: str | None = None, attachment: str | None = None):
	if not assignment.is_active:
		frappe.throw(_("This assignment is not active."))
	answer_text = (answer_text or "").strip()
	attachment = (attachment or "").strip()
	kind = assignment.submission_type
	if kind in ("Text", "Text and File") and not answer_text:
		frappe.throw(_("Write your answer."))
	if kind in ("File", "Text and File") and not attachment:
		frappe.throw(_("Attach a file."))
	if kind == "Text":
		attachment = ""
	if kind == "File":
		answer_text = ""
	if attachment:
		media.validate_file_url(attachment, owner=user)
		_check_extension(assignment, attachment)
	if len(answer_text) > 50000:
		frappe.throw(_("The answer is too long."))

	name = frappe.db.get_value("TCD Assignment Submission", {"assignment": assignment.name, "user": user})
	if name:
		doc = frappe.get_doc("TCD Assignment Submission", name)
		if doc.status == "Graded":
			frappe.throw(_("This submission is already graded."))
	else:
		doc = frappe.new_doc("TCD Assignment Submission")
		doc.update({"assignment": assignment.name, "user": user, "content": assignment.content})
	doc.update(
		{
			"course": _submission_course(assignment, user),
			"answer_text": answer_text,
			"attachment": attachment or None,
			"status": "Submitted",
			"submitted_on": now_datetime(),
			"is_late": int(bool(assignment.due_date) and now_datetime() > get_datetime(assignment.due_date)),
		}
	)
	doc.flags.from_api = True
	doc.save(ignore_permissions=True)
	from vintraxo_tcd.core import notify

	notify.assignment_submitted(doc)
	return doc


def grade(submission, score, feedback: str | None, action: str = "Graded"):
	if action not in ("Graded", "Returned"):
		frappe.throw(_("Invalid grading action."))
	assignment = frappe.get_doc("TCD Assignment", submission.assignment)
	submission.feedback = (feedback or "").strip() or None
	submission.status = action
	if action == "Graded":
		score = flt(score)
		if not 0 <= score <= flt(assignment.max_score):
			frappe.throw(_("Score must be between 0 and {0}.").format(assignment.max_score))
		submission.score = score
		submission.passed = int(score >= flt(assignment.pass_score))
		submission.graded_by = frappe.session.user
		submission.graded_on = now_datetime()
	elif not submission.feedback:
		frappe.throw(_("Tell the learner what to change before returning the submission."))
	submission.flags.from_api = True
	submission.save(ignore_permissions=True)
	if action == "Graded" and submission.passed and assignment.required_to_complete:
		progress.complete(submission.user, submission.content, from_quiz=True)
	courses.on_content_changed(submission.user, submission.content)
	return submission
