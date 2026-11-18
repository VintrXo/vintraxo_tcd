"""Learner progress: one TCD Progress row per (user, content)."""

import frappe
from frappe import _
from frappe.utils import flt, now_datetime

from vintraxo_tcd.core.content import tutorials_for_lesson
from vintraxo_tcd.core.permissions import can_access_content


def get_progress(user: str, content: str):
	name = frappe.db.get_value("TCD Progress", {"user": user, "content": content})
	return frappe.get_doc("TCD Progress", name) if name else None


def _upsert(user: str, content: str, **values):
	doc = get_progress(user, content)
	if not doc:
		doc = frappe.get_doc(
			{"doctype": "TCD Progress", "user": user, "content": content, "started_on": now_datetime()}
		)
	if doc.status == "Completed" and values.get("status") == "In Progress":
		values.pop("status")  # never downgrade
		values.pop("percent", None)
	doc.update(values)
	doc.flags.ignore_permissions = True
	doc.save()
	return doc


def track_view(user: str, content: str):
	doc = get_progress(user, content)
	if doc:
		doc.db_set("last_viewed_on", now_datetime(), update_modified=False)
		return doc
	return _upsert(user, content, status="In Progress", percent=0, last_viewed_on=now_datetime())


def required_quiz(content: str) -> str | None:
	return frappe.db.get_value(
		"TCD Quiz", {"content": content, "is_active": 1, "required_to_complete": 1}, "name"
	)


def has_passed(user: str, quiz: str) -> bool:
	return bool(frappe.db.exists("TCD Quiz Submission", {"quiz": quiz, "user": user, "passed": 1}))


def complete(user: str, content: str, from_quiz: bool = False):
	"""Mark content completed and roll up into the tutorials that include it."""
	content_type = frappe.db.get_value("TCD Content", content, "content_type")
	if content_type == "Tutorial":
		frappe.throw(_("Tutorials complete automatically when their lessons are completed."))
	if not from_quiz:
		quiz = required_quiz(content)
		if quiz and not has_passed(user, quiz):
			frappe.throw(_("Pass the quiz to complete this lesson."))

	doc = _upsert(user, content, status="Completed", percent=100, last_viewed_on=now_datetime())
	if not doc.completed_on:
		doc.db_set("completed_on", now_datetime(), update_modified=False)

	for tutorial in tutorials_for_lesson(content):
		refresh_tutorial(user, tutorial)
	return doc


def tutorial_summary(user: str, tutorial: str) -> dict:
	"""Lessons the user can see, with their completion state."""
	tut = frappe.get_doc("TCD Content", tutorial)
	lessons = []
	for row in tut.lessons:
		lesson = frappe.get_doc("TCD Content", row.lesson)
		if not can_access_content(lesson, user):
			continue
		status = frappe.db.get_value("TCD Progress", {"user": user, "content": row.lesson}, "status")
		lessons.append(
			{
				"lesson": row.lesson,
				"title": lesson.title,
				"slug": lesson.slug,
				"is_optional": bool(row.is_optional),
				"status": status or "Not Started",
			}
		)
	required = [lesson for lesson in lessons if not lesson["is_optional"]]
	done = [lesson for lesson in required if lesson["status"] == "Completed"]
	percent = flt(len(done) * 100 / len(required), 1) if required else 0
	return {
		"tutorial": tutorial,
		"lessons": lessons,
		"required": len(required),
		"completed": len(done),
		"percent": percent,
		"is_complete": bool(required) and len(done) == len(required),
	}


def refresh_tutorial(user: str, tutorial: str):
	summary = tutorial_summary(user, tutorial)
	if not summary["completed"] and not get_progress(user, tutorial):
		return None
	status = "Completed" if summary["is_complete"] else "In Progress"
	doc = _upsert(user, tutorial, status=status, percent=summary["percent"])
	if status == "Completed" and not doc.completed_on:
		doc.db_set("completed_on", now_datetime(), update_modified=False)
	return doc
