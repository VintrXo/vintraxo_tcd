"""Training sessions and attendance (Phase 12, ADR-0020): classroom or online sessions of a course
(optionally one batch), invitations, attendance taken by the instructor, learner views and a report."""

from urllib.parse import urlparse

import frappe
from frappe import _
from frappe.utils import add_days, get_datetime, now_datetime

from vintraxo_tcd.core.permissions import _in, instructed, is_admin

ATTENDED = ("Present", "Late")


# ---------------------------------------------------------------- permissions


def can_manage(doc, user: str) -> bool:
	"""Admins, or an instructor of the session's course (or the session's own instructor)."""
	if is_admin(user):
		return True
	if "TCD Instructor" not in frappe.get_roles(user):
		return False
	return bool(doc.course and doc.course in instructed(user, "TCD Course")) or doc.get("instructor") == user


def session_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if ptype in (None, "read", "report", "print") and "TCD Content Reviewer" in frappe.get_roles(user):
		return True
	if doc.is_new() and not doc.course:
		return True
	return can_manage(doc, user)


def session_query(user=None, doctype=None):
	user = user or frappe.session.user
	if is_admin(user) or "TCD Content Reviewer" in frappe.get_roles(user):
		return ""
	parts = [f"`tabTCD Session`.instructor = {frappe.db.escape(user)}"]
	courses = instructed(user, "TCD Course")
	if courses:
		parts.append(_in("`tabTCD Session`.course", courses))
	return "(" + " or ".join(parts) + ")"


# ---------------------------------------------------------------- validation


def invited(doc) -> list[str]:
	"""Learners invited to the session: the batch members (when set) who are enrolled, else every
	active enrollment of the course."""
	enrolled = set(
		frappe.get_all(
			"TCD Enrollment",
			filters={"course": doc.course, "status": ("in", ["Active", "Pending Approval", "Completed"])},
			pluck="user",
		)
	)
	if doc.batch:
		members = set(frappe.get_all("TCD Batch Member", filters={"parent": doc.batch}, pluck="user"))
		enrolled &= members
	return sorted(enrolled)


def validate(doc):
	if get_datetime(doc.ends_on) <= get_datetime(doc.starts_on):
		frappe.throw(_("The session must end after it starts."))
	if doc.session_type == "Online":
		url = (doc.meeting_url or "").strip()
		if url and urlparse(url).scheme not in ("http", "https"):
			frappe.throw(_("The meeting link must be an http(s) URL."))
		doc.meeting_url = url
		doc.location = None
	else:
		doc.meeting_url = None
	doc.instructor = doc.instructor or frappe.session.user
	seen = set()
	marked = False
	allowed = set(invited(doc))
	for row in doc.attendance:
		if row.user in seen:
			frappe.throw(_("{0} is listed twice.").format(frappe.bold(row.user)))
		seen.add(row.user)
		if row.user not in allowed:
			frappe.throw(_("{0} is not enrolled in this course or batch.").format(frappe.bold(row.user)))
		marked = marked or bool(row.status)
	if marked and get_datetime(doc.starts_on) > now_datetime():
		frappe.throw(_("Attendance can be taken once the session starts."))
	if marked and doc.status == "Cancelled":
		frappe.throw(_("A cancelled session has no attendance."))


def on_update(doc):
	from vintraxo_tcd.core import notify

	before = doc.get_doc_before_save()
	when = frappe.utils.format_datetime(doc.starts_on, "dd-MM-yyyy HH:mm")
	if not before and doc.status == "Scheduled":
		notify._send(
			invited(doc), _("New session: {0} on {1}").format(doc.title, when), doc.doctype, doc.name
		)
	elif before and before.status != "Cancelled" and doc.status == "Cancelled":
		notify._send(
			invited(doc), _("Session cancelled: {0} on {1}").format(doc.title, when), doc.doctype, doc.name
		)
	elif (
		before and doc.status == "Scheduled" and get_datetime(before.starts_on) != get_datetime(doc.starts_on)
	):
		notify._send(
			invited(doc), _("Session moved: {0} is now on {1}").format(doc.title, when), doc.doctype, doc.name
		)


def load_learners(name: str) -> int:
	"""Add the invited learners that are not listed yet (existing marks are kept)."""
	doc = frappe.get_doc("TCD Session", name)
	doc.check_permission("write")
	listed = {r.user for r in doc.attendance}
	added = 0
	for user in invited(doc):
		if user not in listed:
			doc.append("attendance", {"user": user})
			added += 1
	if added:
		doc.save()
	return added


# ---------------------------------------------------------------- learner views


def _row(s, user: str, enrolled: bool) -> dict:
	mark = frappe.db.get_value("TCD Session Attendance", {"parent": s.name, "user": user}, "status")
	return {
		"name": s.name,
		"title": s.title,
		"course": s.course,
		"starts_on": s.starts_on,
		"ends_on": s.ends_on,
		"session_type": s.session_type,
		"status": s.status,
		"location": s.location,
		# the meeting link is only for invited learners
		"meeting_url": s.meeting_url if enrolled else None,
		"attendance": mark,
	}


def for_course(course: str, user: str) -> dict:
	"""Upcoming sessions and the user's past attendance in one course (only for invited learners)."""
	out = {"upcoming": [], "past": []}
	if user == "Guest":
		return out
	now = now_datetime()
	for name in frappe.get_all(
		"TCD Session",
		filters={"course": course, "status": ("!=", "Cancelled")},
		order_by="starts_on asc",
		pluck="name",
	):
		s = frappe.get_doc("TCD Session", name)
		if user not in invited(s):
			continue
		row = _row(s, user, True)
		(out["upcoming"] if get_datetime(s.ends_on) >= now else out["past"]).append(row)
	return out


def upcoming_for(user: str, days: int = 14) -> list[dict]:
	courses = frappe.get_all(
		"TCD Enrollment",
		filters={"user": user, "course": ("is", "set"), "status": ("in", ["Active", "Pending Approval"])},
		pluck="course",
	)
	if not courses:
		return []
	now = now_datetime()
	out = []
	for name in frappe.get_all(
		"TCD Session",
		filters=[
			["course", "in", courses],
			["status", "=", "Scheduled"],
			["ends_on", ">=", now],
			["starts_on", "<=", add_days(now, days)],
		],
		order_by="starts_on asc",
		pluck="name",
	):
		s = frappe.get_doc("TCD Session", name)
		if user in invited(s):
			row = _row(s, user, True)
			row["course_title"] = frappe.db.get_value("TCD Course", s.course, "title")
			out.append(row)
	return out


# ---------------------------------------------------------------- report


def attendance_rows(filters) -> list[dict]:
	"""Per learner and course: sessions held so far and how many were attended. Runs as the user."""
	conditions = [["status", "!=", "Cancelled"], ["starts_on", "<=", now_datetime()]]
	for key in ("course", "batch"):
		if filters.get(key):
			conditions.append([key, "=", filters[key]])
	stats = {}
	for s in frappe.get_list(
		"TCD Session", filters=conditions, fields=["name", "course"], limit_page_length=0
	):
		doc = frappe.get_doc("TCD Session", s.name)
		marks = {r.user: r.status for r in doc.attendance}
		for user in invited(doc):
			row = stats.setdefault(
				(user, s.course),
				{
					"user": user,
					"course": s.course,
					"held": 0,
					"Present": 0,
					"Late": 0,
					"Absent": 0,
					"Excused": 0,
					"unmarked": 0,
				},
			)
			row["held"] += 1
			status = marks.get(user)
			row[status if status else "unmarked"] += 1
	rows = []
	for row in stats.values():
		counted = row["held"] - row["Excused"]
		attended = row["Present"] + row["Late"]
		row["attendance"] = round(attended * 100 / counted, 1) if counted else 100.0
		row["full_name"] = frappe.db.get_value("User", row["user"], "full_name")
		rows.append(row)
	rows.sort(key=lambda r: (r["course"], r["attendance"], r["user"]))
	return rows
