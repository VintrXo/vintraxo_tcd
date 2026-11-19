from frappe import _

from vintraxo_tcd.core import freshness


def execute(filters=None):
	filters = filters or {}
	rows = freshness.rows(filters)
	overdue = sum(1 for r in rows if r["days_overdue"])
	summary = [
		{"label": _("Published pages"), "value": len(rows), "datatype": "Int"},
		{
			"label": _("Past review date"),
			"value": overdue,
			"datatype": "Int",
			"indicator": "Red" if overdue else "Green",
		},
	]
	return columns(), rows, None, None, summary


def columns():
	return [
		{
			"fieldname": "name",
			"label": _("Page"),
			"fieldtype": "Link",
			"options": "TCD Content",
			"width": 120,
		},
		{"fieldname": "title", "label": _("Title"), "fieldtype": "Data", "width": 220},
		{
			"fieldname": "space",
			"label": _("Space"),
			"fieldtype": "Link",
			"options": "TCD Space",
			"width": 140,
		},
		{
			"fieldname": "content_owner",
			"label": _("Content Owner"),
			"fieldtype": "Link",
			"options": "User",
			"width": 180,
		},
		{"fieldname": "last_reviewed_on", "label": _("Last Reviewed On"), "fieldtype": "Date", "width": 120},
		{"fieldname": "next_review_date", "label": _("Next Review Date"), "fieldtype": "Date", "width": 120},
		{"fieldname": "days_overdue", "label": _("Days Overdue"), "fieldtype": "Int", "width": 110},
	]
