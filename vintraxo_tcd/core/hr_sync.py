"""Record completed courses in HRMS (Phase 13, ADR-0021). Guarded: does nothing without HRMS.

For each completed course enrollment of an active Employee: a Training Program per course (reused),
a submitted Training Event (the employee, Completed / Present) and a submitted Training Result with the
score. Runs in the background after commit; a failure is logged and never blocks the completion."""

import frappe
from frappe.utils import add_to_date, escape_html, get_datetime, now_datetime

from vintraxo_tcd.core.training import employee_profile, hr_available

LOCATION = "VintraXo TCD (online)"


def available() -> bool:
	return hr_available() and bool(frappe.db.exists("DocType", "Training Event"))


def enabled() -> bool:
	return bool(frappe.db.get_single_value("TCD Settings", "sync_training_to_hr"))


def on_completed(enrollment):
	if not enrollment.course or enrollment.get("hr_training_event") or not enabled() or not available():
		return
	frappe.enqueue(
		"vintraxo_tcd.core.hr_sync.record",
		queue="long",
		enrollment=enrollment.name,
		enqueue_after_commit=True,
	)


# ---------------------------------------------------------------- record builders (pure, tested)


def program_name(course) -> str:
	return f"TCD: {course.title}"[:140]


def program_values(course, company: str) -> dict:
	return {
		"doctype": "Training Program",
		"training_program": program_name(course),
		"company": company,
		"description": escape_html(course.get("summary") or course.title),
		"status": "Completed",
	}


def event_values(enrollment, course, employee) -> dict:
	start = get_datetime(enrollment.enrolled_on or enrollment.completed_on or now_datetime())
	end = get_datetime(enrollment.completed_on or now_datetime())
	if end <= start:
		end = add_to_date(start, minutes=1)
	return {
		"doctype": "Training Event",
		"event_name": f"{enrollment.name} · {course.title} · {employee.name}"[:140],
		"training_program": program_name(course),
		"event_status": "Completed",
		"type": "Theory",
		"company": employee.company,
		"course": course.title[:140],
		"location": LOCATION,
		"start_time": start,
		"end_time": end,
		"has_certificate": int(bool(course.get("issue_certificate"))),
		"introduction": escape_html(course.get("summary") or course.title),
		"employees": [
			{
				"employee": employee.name,
				"status": "Completed",
				"attendance": "Present",
				"is_mandatory": int(bool(enrollment.get("mandatory"))),
			}
		],
	}


def result_values(event_name: str, enrollment, employee) -> dict:
	score = enrollment.get("score")
	return {
		"doctype": "Training Result",
		"training_event": event_name,
		"employees": [
			{
				"employee": employee.name,
				"grade": f"{round(score)}%" if score else "",
				"comments": "Completed in VintraXo TCD",
			}
		],
	}


# ---------------------------------------------------------------- writer


def _insert(values: dict, submit: bool = False):
	doc = frappe.get_doc(values)
	doc.flags.ignore_permissions = True
	doc.insert()
	if submit:
		doc.submit()
	return doc


def record(enrollment: str):
	e = frappe.get_doc("TCD Enrollment", enrollment)
	if e.status != "Completed" or e.get("hr_training_event") or not e.course or not available():
		return None
	employee = employee_profile(e.user)
	if not employee or not employee.get("company"):
		return None
	course = frappe.get_doc("TCD Course", e.course)
	try:
		if not frappe.db.exists("Training Program", program_name(course)):
			_insert(program_values(course, employee.company))
		event = _insert(event_values(e, course, employee), submit=True)
		_insert(result_values(event.name, e, employee), submit=True)
	except Exception:
		frappe.log_error(title=f"TCD: could not record {enrollment} in HRMS")
		return None
	e.db_set("hr_training_event", event.name, update_modified=False)
	return event.name
