"""Certification evaluations (Phase 19, ADR-0027).

A course with "Requires Evaluation" does not issue its certificate when the learner completes it. The
learner books a slot with an evaluator (weekly availability, minus holidays and booked sessions); the
evaluator records Passed / Failed / No Show. Passed issues the certificate; otherwise the learner books
again. Bookings and results go through this module only (DocType fields are read-only)."""

from datetime import timedelta

import frappe
from frappe import _
from frappe.utils import add_days, get_datetime, get_time, getdate, now_datetime, nowdate

from vintraxo_tcd.core.permissions import is_admin

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
WINDOW_DAYS = 14
MAX_SLOTS = 80
RESULTS = ("Passed", "Failed", "No Show")


def required(course: str) -> bool:
	values = frappe.db.get_value("TCD Course", course, ["issue_certificate", "requires_evaluation"])
	return bool(values and values[0] and values[1])


def evaluators_for(course: str) -> list[str]:
	"""Users who evaluate this course: the course list, else its instructors who are evaluators."""
	doc = frappe.get_doc("TCD Course", course)
	users = [frappe.db.get_value("TCD Evaluator", r.evaluator, "user") for r in doc.get("evaluators") or []]
	if not users:
		users = [r.user for r in doc.get("instructors") or [] if frappe.db.exists("TCD Evaluator", r.user)]
	active = set(frappe.get_all("TCD Evaluator", filters={"is_active": 1}, pluck="user"))
	return [u for u in dict.fromkeys(users) if u and u in active]


# ---------------------------------------------------------------- eligibility


def _enrollment_status(user: str, course: str) -> str | None:
	return frappe.db.get_value("TCD Enrollment", {"user": user, "course": course}, "status")


def _has_certificate(user: str, course: str) -> bool:
	return bool(frappe.db.exists("TCD Certificate", {"user": user, "course": course, "status": "Active"}))


def scheduled(user: str, course: str) -> dict | None:
	name = frappe.db.get_value("TCD Evaluation", {"user": user, "course": course, "status": "Scheduled"})
	return _public(frappe.get_doc("TCD Evaluation", name)) if name else None


def state(user: str, course: str) -> dict | None:
	"""What the course page shows about the evaluation, or None when the course needs none."""
	if user == "Guest" or not required(course):
		return None
	last = frappe.get_all(
		"TCD Evaluation",
		filters={"user": user, "course": course, "status": ("in", RESULTS)},
		fields=["name"],
		order_by="creation desc",
		limit=1,
	)
	out = {
		"completed": _enrollment_status(user, course) == "Completed",
		"certified": _has_certificate(user, course),
		"scheduled": scheduled(user, course),
		"last": _public(frappe.get_doc("TCD Evaluation", last[0].name)) if last else None,
	}
	out["can_book"] = out["completed"] and not out["certified"] and not out["scheduled"]
	out["slots"] = available_slots(course) if out["can_book"] else []
	return out


def _public(doc) -> dict:
	return {
		"name": doc.name,
		"status": doc.status,
		"date": str(doc.date),
		"start_time": _hhmm(_minutes(doc.start_time)),
		"end_time": _hhmm(_minutes(doc.end_time)),
		"evaluator": doc.evaluator,
		"evaluator_name": frappe.db.get_value("User", doc.evaluator, "full_name") or doc.evaluator,
		"meeting_url": doc.meeting_url,
		"score": doc.score,
		"feedback": doc.feedback,
	}


# ---------------------------------------------------------------- slots


def _minutes(t) -> int:
	t = get_time(t)
	return t.hour * 60 + t.minute


def _hhmm(m: int) -> str:
	return f"{m // 60:02d}:{m % 60:02d}"


def available_slots(course: str, days: int = WINDOW_DAYS) -> list[dict]:
	"""Free slots from tomorrow for `days` days, over every evaluator of the course."""
	length = int(frappe.db.get_value("TCD Course", course, "evaluation_minutes") or 30)
	length = min(max(length, 10), 240)
	start_day = getdate(add_days(nowdate(), 1))
	out = []
	for user in evaluators_for(course):
		ev = frappe.get_doc("TCD Evaluator", user)
		off_from = getdate(ev.unavailable_from) if ev.unavailable_from else None
		off_to = getdate(ev.unavailable_to) if ev.unavailable_to else off_from
		booked = {}
		for b in frappe.get_all(
			"TCD Evaluation",
			filters={"evaluator": user, "status": "Scheduled", "date": (">=", start_day)},
			fields=["date", "start_time", "end_time"],
		):
			booked.setdefault(getdate(b.date), []).append((_minutes(b.start_time), _minutes(b.end_time)))
		name = frappe.db.get_value("User", user, "full_name") or user
		for offset in range(days):
			day = start_day + timedelta(days=offset)
			if off_from and off_from <= day <= (off_to or off_from):
				continue
			for row in ev.schedule:
				if row.day != DAYS[day.weekday()]:
					continue
				m, end = _minutes(row.start_time), _minutes(row.end_time)
				while m + length <= end:
					if not any(m < b_end and b_start < m + length for b_start, b_end in booked.get(day, [])):
						out.append(
							{
								"evaluator": user,
								"evaluator_name": name,
								"date": str(day),
								"start_time": _hhmm(m),
								"end_time": _hhmm(m + length),
							}
						)
					m += length
	out.sort(key=lambda s: (s["date"], s["start_time"], s["evaluator_name"]))
	return out[:MAX_SLOTS]


# ---------------------------------------------------------------- learner actions


def book(user: str, course: str, evaluator: str, date: str, start_time: str) -> str:
	if user == "Guest":
		raise frappe.PermissionError
	frappe.has_permission("TCD Course", "read", course, throw=True)
	st = state(user, course)
	if not st or not st["can_book"]:
		frappe.throw(_("You cannot book an evaluation for this course now."))
	slot = next(
		(
			s
			for s in st["slots"]
			if s["evaluator"] == evaluator
			and s["date"] == str(getdate(date))
			and s["start_time"] == start_time[:5]
		),
		None,
	)
	if not slot:
		frappe.throw(_("This time is no longer available. Choose another one."))
	doc = frappe.get_doc(
		{
			"doctype": "TCD Evaluation",
			"course": course,
			"user": user,
			"full_name": frappe.db.get_value("User", user, "full_name") or user,
			"evaluator": evaluator,
			"status": "Scheduled",
			"date": slot["date"],
			"start_time": slot["start_time"],
			"end_time": slot["end_time"],
		}
	)
	doc.flags.from_service = True
	doc.insert(ignore_permissions=True)
	_notify(
		evaluator,
		_("{0} booked a certification evaluation for {1} on {2} at {3}").format(
			doc.full_name,
			frappe.db.get_value("TCD Course", course, "title"),
			slot["date"],
			slot["start_time"],
		),
		doc.name,
	)
	return doc.name


def cancel(user: str, name: str) -> dict:
	doc = frappe.get_doc("TCD Evaluation", name)
	if doc.user != user and not is_admin(user):
		raise frappe.PermissionError
	if doc.status != "Scheduled":
		frappe.throw(_("Only a scheduled evaluation can be cancelled."))
	if get_datetime(f"{doc.date} {doc.start_time}") <= now_datetime():
		frappe.throw(_("The evaluation has already started."))
	doc.flags.from_service = True
	doc.db_set("status", "Cancelled")
	_notify(doc.evaluator, _("{0} cancelled the evaluation on {1}").format(doc.full_name, doc.date), doc.name)
	return {"status": "Cancelled"}


# ---------------------------------------------------------------- evaluator actions


def can_evaluate(doc, user: str) -> bool:
	return is_admin(user) or doc.evaluator == user


def record_result(
	name: str, user: str, result: str, score=None, feedback: str = "", meeting_url: str | None = None
) -> dict:
	doc = frappe.get_doc("TCD Evaluation", name)
	if not can_evaluate(doc, user):
		raise frappe.PermissionError
	if result not in RESULTS:
		frappe.throw(_("Choose Passed, Failed or No Show."))
	if doc.status != "Scheduled":
		frappe.throw(_("This evaluation already has a result."))
	if get_datetime(f"{doc.date} {doc.start_time}") > now_datetime() and not is_admin(user):
		frappe.throw(_("Record the result after the evaluation starts."))
	values = {
		"status": result,
		"score": max(0.0, min(100.0, float(score))) if score not in (None, "") else None,
		"feedback": (feedback or "").strip()[:2000],
	}
	cert = None
	if result == "Passed":
		from vintraxo_tcd.core import credentials

		cert = credentials.issue_certificate(doc.user, "Course", doc.course)
		values["certificate"] = (
			cert.name
			if cert
			else frappe.db.get_value(
				"TCD Certificate", {"user": doc.user, "course": doc.course, "status": "Active"}
			)
		)
	doc.db_set(values)
	title = frappe.db.get_value("TCD Course", doc.course, "title")
	message = {
		"Passed": _("You passed the evaluation for {0}. Your certificate is ready."),
		"Failed": _("Your evaluation for {0} was not passed. Read the feedback and book again."),
		"No Show": _("You missed the evaluation for {0}. Book a new time."),
	}[result].format(title)
	_notify(doc.user, message, doc.name)
	return {"status": result, "certificate": values.get("certificate")}


def set_meeting_url(name: str, user: str, url: str) -> dict:
	doc = frappe.get_doc("TCD Evaluation", name)
	if not can_evaluate(doc, user):
		raise frappe.PermissionError
	url = (url or "").strip()
	if url and not url.startswith("https://"):
		frappe.throw(_("The meeting link must start with https://"))
	doc.db_set("meeting_url", url or None)
	if url:
		_notify(doc.user, _("Meeting link for your evaluation on {0}: {1}").format(doc.date, url), doc.name)
	return {"meeting_url": url or None}


def for_evaluator(user: str) -> dict:
	"""Upcoming and recent evaluations of an evaluator (or all for admins), for the instructor page."""
	filters = {} if is_admin(user) else {"evaluator": user}
	rows = frappe.get_all(
		"TCD Evaluation",
		filters={**filters, "status": "Scheduled"},
		fields=[
			"name",
			"course",
			"full_name",
			"user",
			"date",
			"start_time",
			"end_time",
			"meeting_url",
			"evaluator",
		],
		order_by="date asc, start_time asc",
		limit=100,
	)
	now = now_datetime()
	for r in rows:
		r.course_title = frappe.db.get_value("TCD Course", r.course, "title")
		r.started = get_datetime(f"{r.date} {r.start_time}") <= now
		r.start_time = _hhmm(_minutes(r.start_time))
		r.end_time = _hhmm(_minutes(r.end_time))
	return {"upcoming": rows, "is_evaluator": bool(frappe.db.exists("TCD Evaluator", user)) or is_admin(user)}


# ---------------------------------------------------------------- permissions and validation


def evaluation_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if is_admin(user):
		return True
	if doc.user == user:
		return ptype in (None, "read", "print")
	return doc.evaluator == user and ptype in (None, "read", "write", "report", "print")


def evaluation_query(user=None, doctype=None):
	user = user or frappe.session.user
	if is_admin(user):
		return ""
	u = frappe.db.escape(user)
	return f"(`tabTCD Evaluation`.user = {u} or `tabTCD Evaluation`.evaluator = {u})"


def validate_evaluation(doc):
	if doc.is_new() and not doc.flags.from_service:
		frappe.throw(_("Evaluations are booked from the course page."))


def validate_evaluator(doc):
	for row in doc.schedule:
		if _minutes(row.end_time) <= _minutes(row.start_time):
			frappe.throw(_("Row {0}: the end time must be after the start time.").format(row.idx))
	if (
		doc.unavailable_from
		and doc.unavailable_to
		and getdate(doc.unavailable_to) < getdate(doc.unavailable_from)
	):
		frappe.throw(_("Unavailable To must be on or after Unavailable From."))


def _notify(user: str, subject: str, name: str):
	from vintraxo_tcd.core import notify

	notify._send([user], subject, "TCD Evaluation", name)
