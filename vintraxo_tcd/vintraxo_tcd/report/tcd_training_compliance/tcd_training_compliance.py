from frappe import _

from vintraxo_tcd.core import training


def execute(filters=None):
	filters = filters or {}
	rows = training.compliance_rows(filters)
	return columns(), rows, None, None, summary(rows)


def columns():
	cols = [
		{"fieldname": "user", "label": _("User"), "fieldtype": "Link", "options": "User", "width": 200},
		{"fieldname": "full_name", "label": _("Full Name"), "fieldtype": "Data", "width": 160},
	]
	if training.hr_available():
		cols += [
			{
				"fieldname": "employee",
				"label": _("Employee"),
				"fieldtype": "Link",
				"options": "Employee",
				"width": 120,
			},
			{"fieldname": "department", "label": _("Department"), "fieldtype": "Data", "width": 140},
			{"fieldname": "designation", "label": _("Designation"), "fieldtype": "Data", "width": 140},
		]
	return [
		*cols,
		{"fieldname": "assigned", "label": _("Mandatory"), "fieldtype": "Int", "width": 100},
		{"fieldname": "completed", "label": _("Completed", context="TCD"), "fieldtype": "Int", "width": 100},
		{"fieldname": "overdue", "label": _("Overdue"), "fieldtype": "Int", "width": 90},
		{"fieldname": "compliance", "label": _("Compliance"), "fieldtype": "Percent", "width": 110},
	]


def summary(rows):
	assigned = sum(r["assigned"] for r in rows)
	done = sum(r["completed"] for r in rows)
	return [
		{"label": _("Learners"), "value": len(rows), "datatype": "Int"},
		{
			"label": _("Compliance"),
			"value": round(done * 100 / assigned, 1) if assigned else 100,
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
