from frappe import _

from vintraxo_tcd.core import analytics


def execute(filters=None):
	filters = filters or {}
	rows = analytics.usage_rows(filters)
	return columns(), rows, None, None, summary(rows)


def columns():
	return [
		{
			"fieldname": "content",
			"label": _("Content"),
			"fieldtype": "Link",
			"options": "TCD Content",
			"width": 240,
		},
		{"fieldname": "content_type", "label": _("Type"), "fieldtype": "Data", "width": 100},
		{
			"fieldname": "space",
			"label": _("Space"),
			"fieldtype": "Link",
			"options": "TCD Space",
			"width": 140,
		},
		{"fieldname": "readers", "label": _("Readers"), "fieldtype": "Int", "width": 90},
		{"fieldname": "completed", "label": _("Completed"), "fieldtype": "Int", "width": 90},
		{"fieldname": "feedback", "label": _("Feedback"), "fieldtype": "Int", "width": 90},
		{"fieldname": "helpful_rate", "label": _("Helpful %"), "fieldtype": "Percent", "width": 100},
		{"fieldname": "backlinks", "label": _("Linked From"), "fieldtype": "Int", "width": 100},
	]


def summary(rows):
	return [
		{"label": _("Pages"), "value": len(rows), "datatype": "Int"},
		{
			"label": _("Readers"),
			"value": sum(r["readers"] for r in rows),
			"datatype": "Int",
			"indicator": "Blue",
		},
		{
			"label": _("Never read"),
			"value": sum(1 for r in rows if not r["readers"]),
			"datatype": "Int",
			"indicator": "Orange",
		},
	]
