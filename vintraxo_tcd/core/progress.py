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


def required_assignment(content: str) -> str | None:
	return frappe.db.get_value(
		"TCD Assignment", {"content": content, "is_active": 1, "required_to_complete": 1}, "name"
	)


def has_passed_assignment(user: str, assignment: str) -> bool:
	return bool(
		frappe.db.exists(
			"TCD Assignment Submission",
			{"assignment": assignment, "user": user, "status": "Graded", "passed": 1},
		)
	)


def completion_blockers(user: str, content: str) -> list[str]:
	"""Assessment requirements that keep a lesson from being completed."""
	missing = []
	quiz = required_quiz(content)
	if quiz and not has_passed(user, quiz):
		missing.append(_("Pass the quiz to complete this lesson."))
	assignment = required_assignment(content)
	if assignment and not has_passed_assignment(user, assignment):
		missing.append(_("Pass the assignment to complete this lesson."))
	min_video = frappe.db.get_value("TCD Content", content, "min_video_percent") or 0
	if min_video and video_count(content):
		watched = (
			frappe.db.get_value("TCD Progress", {"user": user, "content": content}, "video_percent") or 0
		)
		if watched < min_video:
			missing.append(_("Watch at least {0}% of the videos first.").format(int(min_video)))
	from vintraxo_tcd.core.connect import unmet_prerequisites

	unmet = unmet_prerequisites(user, content)
	if unmet:
		missing.append(_("Complete the prerequisites first: {0}").format(", ".join(unmet)))
	return missing


def complete(user: str, content: str, from_quiz: bool = False):
	"""Mark content completed and roll up into tutorials and courses.

	`from_quiz` means the call comes from an assessment result (quiz grading or assignment grading):
	unmet requirements then simply leave the lesson open instead of raising.
	"""
	content_type = frappe.db.get_value("TCD Content", content, "content_type")
	if content_type == "Tutorial":
		frappe.throw(_("Tutorials complete automatically when their lessons are completed."))
	missing = completion_blockers(user, content)
	if missing:
		if from_quiz:
			return None
		frappe.throw(" ".join(missing))

	from vintraxo_tcd.core import courses

	opens = courses.drip_lock(user, content)
	if opens:
		if from_quiz:
			return None
		frappe.throw(_("This lesson opens on {0}.").format(frappe.utils.formatdate(opens)))
	blockers = courses.sequence_blockers(user, content)
	if blockers:
		if from_quiz:
			return None  # quiz result is kept; completion waits for the earlier items
		frappe.throw(_("Complete these items first: {0}").format(", ".join(blockers)))

	doc = _upsert(user, content, status="Completed", percent=100, last_viewed_on=now_datetime())
	if not doc.completed_on:
		doc.db_set("completed_on", now_datetime(), update_modified=False)

	for tutorial in tutorials_for_lesson(content):
		refresh_tutorial(user, tutorial)
	courses.on_content_changed(user, content)
	from vintraxo_tcd.core import badges, content_languages

	content_languages.mirror_completion(user, content)  # Phase 31: counts in the other languages too
	badges.check(user, "Lessons Completed")
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


# ---------------------------------------------------------------- video watching (Phase 14)


def video_count(content: str) -> int:
	from vintraxo_tcd.core.content import parse_blocks

	blocks = parse_blocks(frappe.db.get_value("TCD Content", content, "blocks"))
	return sum(1 for b in blocks if b.get("type") == "video")


def record_video(user: str, content: str, index: int, watched: float, duration: float) -> dict:
	"""Store the seconds a learner really watched of one video block (kept as the maximum reported).
	Reported by the learner's browser: a nudge, not proof."""
	import json

	total = video_count(content)
	index = int(index)
	if not 0 <= index < total:
		frappe.throw(_("Unknown video."))
	duration = max(float(duration or 0), 0.0)
	watched = min(max(float(watched or 0), 0.0), duration)
	if not duration:
		return {"video_percent": 0}
	doc = get_progress(user, content) or track_view(user, content)
	data = json.loads(doc.get("video_watch") or "{}")
	prev = data.get(str(index)) or [0, duration]
	data[str(index)] = [max(prev[0], round(watched, 1)), round(duration, 1)]
	parts = [min(w / d, 1.0) if d else 0 for w, d in (data.get(str(i), [0, 0]) for i in range(total))]
	percent = round(sum(parts) * 100 / total, 1)
	doc.db_set({"video_watch": json.dumps(data), "video_percent": percent}, update_modified=False)
	return {"video_percent": percent}
