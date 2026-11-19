"""Competency gap: required skill levels of a profile vs each user's current level (admins)."""

from frappe import _

from vintraxo_tcd.core.credentials import gap_rows


def execute(filters=None):
	filters = filters or {}
	if not filters.get("profile"):
		return columns(), [], _("Select a competency profile."), None, []
	rows = gap_rows(filters["profile"], filters.get("user"))
	if filters.get("only_gaps"):
		rows = [r for r in rows if r["gap"]]
	return columns(), rows, None, None, summary(rows)


def columns():
	return [
		{"fieldname": "user", "label": _("User"), "fieldtype": "Link", "options": "User", "width": 200},
		{"fieldname": "full_name", "label": _("Full Name"), "fieldtype": "Data", "width": 160},
		{
			"fieldname": "skill",
			"label": _("Skill"),
			"fieldtype": "Link",
			"options": "TCD Skill",
			"width": 180,
		},
		{"fieldname": "required_level", "label": _("Required Level"), "fieldtype": "Int", "width": 120},
		{"fieldname": "current_level", "label": _("Current Level"), "fieldtype": "Int", "width": 120},
		{"fieldname": "gap", "label": _("Gap"), "fieldtype": "Int", "width": 70},
		{"fieldname": "suggested", "label": _("Suggested Courses"), "fieldtype": "Data", "width": 280},
	]


def summary(rows):
	users = {r["user"] for r in rows}
	ready = {u for u in users if not any(r["gap"] for r in rows if r["user"] == u)}
	return [
		{"label": _("Users"), "value": len(users), "datatype": "Int"},
		{"label": _("Fully Competent"), "value": len(ready), "datatype": "Int", "indicator": "Green"},
		{
			"label": _("Open Gaps"),
			"value": sum(1 for r in rows if r["gap"]),
			"datatype": "Int",
			"indicator": "Orange",
		},
	]
