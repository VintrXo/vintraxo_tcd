from frappe import _

from vintraxo_tcd.core import analytics


def execute(filters=None):
	filters = filters or {}
	rows = analytics.course_rows(filters)
	return columns(), rows, None, None, summary(rows)


def columns():
	return [
		{
			"fieldname": "course",
			"label": _("Course"),
			"fieldtype": "Link",
			"options": "TCD Course",
			"width": 220,
		},
		{"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 90},
		{
			"fieldname": "space",
			"label": _("Space"),
			"fieldtype": "Link",
			"options": "TCD Space",
			"width": 140,
		},
		{"fieldname": "enrolled", "label": _("Enrolled"), "fieldtype": "Int", "width": 90},
		{"fieldname": "completed", "label": _("Completed"), "fieldtype": "Int", "width": 90},
		{"fieldname": "completion_rate", "label": _("Completion Rate"), "fieldtype": "Percent", "width": 120},
		{"fieldname": "overdue", "label": _("Overdue"), "fieldtype": "Int", "width": 90},
		{
			"fieldname": "avg_days_to_complete",
			"label": _("Average Days to Complete"),
			"fieldtype": "Float",
			"width": 170,
		},
		{"fieldname": "avg_score", "label": _("Average Score"), "fieldtype": "Percent", "width": 120},
		{"fieldname": "rating", "label": _("Rating"), "fieldtype": "Float", "width": 80},
	]


def summary(rows):
	enrolled = sum(r["enrolled"] for r in rows)
	completed = sum(r["completed"] for r in rows)
	return [
		{"label": _("Courses"), "value": len(rows), "datatype": "Int"},
		{"label": _("Enrolled"), "value": enrolled, "datatype": "Int", "indicator": "Blue"},
		{
			"label": _("Completion Rate"),
			"value": round(completed * 100 / enrolled, 1) if enrolled else 0,
			"datatype": "Percent",
			"indicator": "Green",
		},
		{
			"label": _("Overdue"),
			"value": sum(r["overdue"] for r in rows),
			"datatype": "Int",
			"indicator": "Red",
		},
	]
