from frappe import _

from vintraxo_tcd.core import sessions


def execute(filters=None):
	filters = filters or {}
	rows = sessions.attendance_rows(filters)
	held = sum(r["held"] - r["Excused"] for r in rows)
	attended = sum(r["Present"] + r["Late"] for r in rows)
	summary = [
		{"label": _("Learners"), "value": len({r["user"] for r in rows}), "datatype": "Int"},
		{
			"label": _("Attendance"),
			"value": round(attended * 100 / held, 1) if held else 100,
			"datatype": "Percent",
			"indicator": "Green",
		},
	]
	return columns(), rows, None, None, summary


def columns():
	return [
		{"fieldname": "user", "label": _("User"), "fieldtype": "Link", "options": "User", "width": 200},
		{"fieldname": "full_name", "label": _("Full Name"), "fieldtype": "Data", "width": 160},
		{
			"fieldname": "course",
			"label": _("Course", context="TCD"),
			"fieldtype": "Link",
			"options": "TCD Course",
			"width": 160,
		},
		{"fieldname": "held", "label": _("Sessions held"), "fieldtype": "Int", "width": 110},
		{"fieldname": "Present", "label": _("Present", context="TCD"), "fieldtype": "Int", "width": 80},
		{"fieldname": "Late", "label": _("Late", context="TCD"), "fieldtype": "Int", "width": 80},
		{"fieldname": "Absent", "label": _("Absent", context="TCD"), "fieldtype": "Int", "width": 80},
		{"fieldname": "Excused", "label": _("Excused", context="TCD"), "fieldtype": "Int", "width": 80},
		{"fieldname": "unmarked", "label": _("Not recorded"), "fieldtype": "Int", "width": 100},
		{"fieldname": "attendance", "label": _("Attendance"), "fieldtype": "Percent", "width": 110},
	]
