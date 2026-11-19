"""Who has (not) acknowledged the current version of a governance document."""

from frappe import _
from frappe.utils import flt

from vintraxo_tcd.core.governance import acknowledgment_rows


def execute(filters=None):
	filters = filters or {}
	if not filters.get("document"):
		return columns(), [], _("Select a document."), None, []
	rows = acknowledgment_rows(filters["document"])
	if filters.get("only_missing"):
		rows = [r for r in rows if not r["acknowledged"]]
	return columns(), rows, None, None, summary(acknowledgment_rows(filters["document"]))


def columns():
	return [
		{"fieldname": "user", "label": _("User"), "fieldtype": "Link", "options": "User", "width": 220},
		{"fieldname": "full_name", "label": _("Full Name"), "fieldtype": "Data", "width": 180},
		{"fieldname": "version", "label": _("Version"), "fieldtype": "Int", "width": 80},
		{"fieldname": "acknowledged", "label": _("Acknowledged"), "fieldtype": "Check", "width": 120},
		{
			"fieldname": "acknowledged_on",
			"label": _("Acknowledged On"),
			"fieldtype": "Datetime",
			"width": 170,
		},
	]


def summary(rows):
	done = sum(r["acknowledged"] for r in rows)
	return [
		{"label": _("Audience"), "value": len(rows), "datatype": "Int"},
		{"label": _("Acknowledged"), "value": done, "datatype": "Int", "indicator": "Green"},
		{"label": _("Not acknowledged"), "value": len(rows) - done, "datatype": "Int", "indicator": "Red"},
		{
			"label": _("Compliance"),
			"value": flt(done * 100 / len(rows), 1) if rows else 0,
			"datatype": "Percent",
			"indicator": "Blue",
		},
	]
