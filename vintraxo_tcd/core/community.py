"""Certified learners and platform statistics (Phase 25, ADR-0033).

Privacy: a certificate holder is listed only when their learner profile is visible to colleagues (the learner
opted in). The page needs a login. Statistics are counts only."""

import frappe

from vintraxo_tcd.core.permissions import readable_list

MAX_ROWS = 300


def stats() -> dict:
	courses = readable_list("TCD Course", filters={"status": "Published"}, pluck="name")
	return {
		"courses": len(courses),
		"paths": len(readable_list("TCD Learning Path", filters={"status": "Published"}, pluck="name")),
		"pages": frappe.db.count("TCD Content", {"status": "Published"}),
		"learners": len(
			set(
				frappe.get_all(
					"Has Role", filters={"role": "TCD Learner", "parenttype": "User"}, pluck="parent"
				)
			)
			& set(frappe.get_all("User", filters={"enabled": 1}, pluck="name"))
		),
		"completions": frappe.db.count("TCD Enrollment", {"status": "Completed"}),
		"certificates": frappe.db.count("TCD Certificate", {"status": "Active"}),
	}


def certified(course: str | None = None) -> list[dict]:
	public = set(frappe.get_all("TCD Learner Profile", filters={"public_profile": 1}, pluck="user"))
	if not public:
		return []
	filters = {"status": "Active", "user": ("in", list(public))}
	if course:
		filters["course"] = course
	rows = frappe.get_all(
		"TCD Certificate",
		filters=filters,
		fields=["user", "full_name", "title", "issued_on", "verification_code", "course", "learning_path"],
		order_by="issued_on desc",
		limit=MAX_ROWS,
	)
	return rows


def course_options() -> list[dict]:
	names = frappe.get_all(
		"TCD Certificate",
		filters={"status": "Active", "course": ("is", "set")},
		pluck="course",
		distinct=True,
	)
	return [{"name": n, "title": frappe.db.get_value("TCD Course", n, "title")} for n in names if n]
