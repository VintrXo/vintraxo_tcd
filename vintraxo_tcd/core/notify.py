"""Data-driven notifications (ADR-0016): recipients computed from courses and policy audiences.
Fixed-recipient events are standard Notification records in vintraxo_tcd/notification/."""

import frappe
from frappe import _
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification

DEDUPE = ["document_type", "document_name", "subject"]


def _send(users, subject: str, doctype: str, name: str, message: str = ""):
	users = sorted({u for u in users if u and u not in ("Guest",)})
	if not users:
		return
	enqueue_create_notification(
		users,
		{
			"type": "Alert",
			"subject": subject,
			"email_content": message or subject,
			"document_type": doctype,
			"document_name": name,
			"from_user": frappe.session.user,
		},
		dedupe_on=DEDUPE,
	)


def course_instructors(course: str | None) -> list[str]:
	if not course:
		return []
	return frappe.get_all(
		"TCD Course Instructor",
		filters={"parenttype": "TCD Course", "parent": course},
		pluck="user",
		ignore_permissions=True,
	)


def _course_title(course):
	return frappe.db.get_value("TCD Course", course, "title") or course


def assignment_submitted(submission):
	title = frappe.db.get_value("TCD Assignment", submission.assignment, "title")
	_send(
		course_instructors(submission.course),
		_("Submission to grade: {0} ({1})").format(title, submission.user),
		"TCD Assignment Submission",
		submission.name,
	)


def enrollment_pending(enrollment):
	if enrollment.course:
		users = course_instructors(enrollment.course)
		title = _course_title(enrollment.course)
	else:
		users = frappe.get_all(
			"TCD Course Instructor",
			filters={"parenttype": "TCD Learning Path", "parent": enrollment.learning_path},
			pluck="user",
			ignore_permissions=True,
		)
		title = frappe.db.get_value("TCD Learning Path", enrollment.learning_path, "title")
	_send(
		users,
		_("Completion waiting for your approval: {0} ({1})").format(title, enrollment.user),
		"TCD Enrollment",
		enrollment.name,
	)


def quiz_pending_review(submission):
	from vintraxo_tcd.core.courses import courses_with_content

	users = set()
	for course in courses_with_content(submission.content):
		users.update(course_instructors(course))
	title = frappe.db.get_value("TCD Quiz", submission.quiz, "title")
	_send(
		users,
		_("Quiz answers to review: {0} ({1})").format(title, submission.user),
		"TCD Quiz Submission",
		submission.name,
	)


def acknowledgment_due(doc):
	from vintraxo_tcd.core.governance import audience_users

	if not doc.require_acknowledgment:
		return
	_send(
		audience_users(doc),
		_("Please read and acknowledge: {0} (version {1})").format(doc.title, doc.version),
		"TCD Governance Document",
		doc.name,
	)
