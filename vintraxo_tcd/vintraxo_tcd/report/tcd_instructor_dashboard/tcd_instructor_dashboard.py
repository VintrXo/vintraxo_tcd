"""Per-course numbers for the courses the current user instructs (admins: all courses)."""

import frappe
from frappe import _

from vintraxo_tcd.core.dashboards import instructor_dashboard


def execute(filters=None):
	data = instructor_dashboard(frappe.session.user)
	rows = data["courses"]
	return columns(), rows, None, chart(rows), summary(data)


def columns():
	return [
		{
			"fieldname": "course",
			"label": _("Course", context="TCD"),
			"fieldtype": "Link",
			"options": "TCD Course",
			"width": 220,
		},
		{"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 90},
		{"fieldname": "completion_rule", "label": _("Completion Rule"), "fieldtype": "Data", "width": 140},
		{"fieldname": "enrolled", "label": _("Enrolled"), "fieldtype": "Int", "width": 90},
		{"fieldname": "active", "label": _("Active", context="TCD"), "fieldtype": "Int", "width": 80},
		{
			"fieldname": "pending_approval",
			"label": _("Pending Approval", context="TCD"),
			"fieldtype": "Int",
			"width": 130,
		},
		{"fieldname": "completed", "label": _("Completed", context="TCD"), "fieldtype": "Int", "width": 90},
		{"fieldname": "completion_rate", "label": _("Completion Rate"), "fieldtype": "Percent", "width": 120},
		{"fieldname": "to_grade", "label": _("To Grade"), "fieldtype": "Int", "width": 90},
		{"fieldname": "average_score", "label": _("Average Score"), "fieldtype": "Percent", "width": 120},
		{"fieldname": "rating", "label": _("Rating"), "fieldtype": "Float", "precision": 1, "width": 80},
		{"fieldname": "ratings", "label": _("Ratings"), "fieldtype": "Int", "width": 80},
	]


def chart(rows):
	if not rows:
		return None
	return {
		"data": {
			"labels": [r["title"] for r in rows],
			"datasets": [{"name": _("Completion Rate"), "values": [r["completion_rate"] for r in rows]}],
		},
		"type": "bar",
		"height": 220,
	}


def summary(data):
	rows = data["courses"]
	return [
		{"label": _("Courses"), "value": len(rows), "datatype": "Int"},
		{
			"label": _("Enrolled"),
			"value": sum(r["enrolled"] for r in rows),
			"datatype": "Int",
			"indicator": "Blue",
		},
		{
			"label": _("Pending Approval", context="TCD"),
			"value": len(data["pending_approvals"]),
			"datatype": "Int",
			"indicator": "Orange",
		},
		{"label": _("To Grade"), "value": len(data["to_grade"]), "datatype": "Int", "indicator": "Orange"},
	]
