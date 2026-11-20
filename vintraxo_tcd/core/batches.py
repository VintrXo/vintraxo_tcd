"""Batches (Phase 23, ADR-0031): mentors, batch feedback and a weekly timetable that generates sessions."""

from datetime import timedelta

import frappe
from frappe import _
from frappe.utils import get_datetime, get_time, getdate

from vintraxo_tcd.core.permissions import is_admin

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MAX_SESSIONS = 300
RATINGS = ("content_rating", "instructor_rating", "overall_rating")


# ---------------------------------------------------------------- mentors


def mentor_batches(user: str) -> list[str]:
	if user == "Guest":
		return []
	return sorted(
		set(
			frappe.get_all(
				"TCD Batch Mentor", filters={"user": user, "parenttype": "TCD Batch"}, pluck="parent"
			)
		)
	)


def batch_members(batch: str) -> list[str]:
	return frappe.get_all(
		"TCD Batch Member", filters={"parent": batch, "parenttype": "TCD Batch"}, pluck="user"
	)


def batches_of_member(user: str) -> list[str]:
	return frappe.get_all(
		"TCD Batch Member", filters={"user": user, "parenttype": "TCD Batch"}, pluck="parent"
	)


def validate_batch(doc):
	seen = set()
	for row in doc.get("mentors") or []:
		if row.user in seen:
			frappe.throw(_("Row {0}: {1} is listed twice.").format(row.idx, frappe.bold(row.user)))
		seen.add(row.user)
	for row in doc.get("timetable") or []:
		if get_time(row.end_time) <= get_time(row.start_time):
			frappe.throw(_("Timetable row {0}: the end time must be after the start time.").format(row.idx))


# ---------------------------------------------------------------- timetable


def generate_sessions(batch_name: str) -> dict:
	"""One TCD Session per timetable row and matching day between the batch dates. Existing sessions of
	the batch at the same start are kept (running it twice creates nothing new)."""
	batch = frappe.get_doc("TCD Batch", batch_name)
	batch.check_permission("write")
	if not batch.course:
		frappe.throw(_("Choose the course of the batch first."))
	if not (batch.start_date and batch.end_date):
		frappe.throw(_("Set the start and end dates of the batch first."))
	if not batch.timetable:
		frappe.throw(_("Add at least one timetable row."))
	title = frappe.db.get_value("TCD Course", batch.course, "title")
	start, end = getdate(batch.start_date), getdate(batch.end_date)
	created = skipped = 0
	day = start
	while day <= end:
		for row in batch.timetable:
			if row.day != DAYS[day.weekday()]:
				continue
			starts_on = get_datetime(f"{day} {row.start_time}")
			if frappe.db.exists(
				"TCD Session", {"batch": batch.name, "course": batch.course, "starts_on": starts_on}
			):
				skipped += 1
				continue
			if created >= MAX_SESSIONS:
				frappe.throw(_("A timetable can create at most {0} sessions.").format(MAX_SESSIONS))
			frappe.get_doc(
				{
					"doctype": "TCD Session",
					"title": row.title or title,
					"course": batch.course,
					"batch": batch.name,
					"status": "Scheduled",
					"session_type": row.session_type or "Classroom",
					"location": row.location,
					"starts_on": starts_on,
					"ends_on": get_datetime(f"{day} {row.end_time}"),
					"instructor": batch.instructor or frappe.session.user,
				}
			).insert()  # normal permissions: course instructors and admins
			created += 1
		day += timedelta(days=1)
	return {"created": created, "skipped": skipped}


# ---------------------------------------------------------------- feedback


def my_batches(user: str) -> list[dict]:
	out = []
	for name in batches_of_member(user):
		b = frappe.db.get_value(
			"TCD Batch", name, ["name", "group_name", "start_date", "end_date", "course"], as_dict=True
		)
		if not b:
			continue
		fb = frappe.db.get_value(
			"TCD Batch Feedback", {"batch": name, "user": user}, [*RATINGS, "comment"], as_dict=True
		)
		b.feedback = fb
		b.course_title = frappe.db.get_value("TCD Course", b.course, "title") if b.course else None
		out.append(b)
	return out


def save_feedback(user: str, batch: str, data: dict) -> dict:
	if user == "Guest" or user not in batch_members(batch):
		raise frappe.PermissionError(_("Only members of the batch can rate it."))
	values = {}
	for f in RATINGS:
		try:
			v = int(data.get(f) or 0)
		except (TypeError, ValueError):
			v = 0
		if not 1 <= v <= 5:
			frappe.throw(_("Choose a rating from 1 to 5 for each question."))
		values[f] = v
	values["comment"] = (data.get("comment") or "").strip()[:2000]
	name = frappe.db.get_value("TCD Batch Feedback", {"batch": batch, "user": user})
	if name:
		frappe.db.set_value("TCD Batch Feedback", name, values)
	else:
		doc = frappe.get_doc({"doctype": "TCD Batch Feedback", "batch": batch, "user": user, **values})
		doc.flags.from_service = True
		doc.insert(ignore_permissions=True)
	return {"saved": True}


def feedback_summary(batch: str) -> dict:
	rows = frappe.get_all("TCD Batch Feedback", filters={"batch": batch}, fields=[*RATINGS, "comment"])
	out = {"responses": len(rows), "members": len(batch_members(batch))}
	for f in RATINGS:
		out[f] = round(sum(r[f] for r in rows) / len(rows), 1) if rows else None
	out["comments"] = [r.comment for r in rows if r.comment][:20]
	return out


def validate_feedback(doc):
	if doc.is_new() and not doc.flags.from_service:
		frappe.throw(_("Batch feedback is sent from My Learning."))


def can_see_summary(user: str, batch: str) -> bool:
	return is_admin(user) or batch in mentor_batches(user)
