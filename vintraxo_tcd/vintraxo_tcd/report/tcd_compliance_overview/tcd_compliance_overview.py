from frappe import _

from vintraxo_tcd.core import analytics


def execute(filters=None):
	filters = filters or {}
	rows = analytics.compliance_rows()
	return columns(), rows, None, None, summary(rows)


def columns():
	return [
		{
			"fieldname": "document",
			"label": _("Document"),
			"fieldtype": "Link",
			"options": "TCD Governance Document",
			"width": 200,
		},
		{"fieldname": "title", "label": _("Title"), "fieldtype": "Data", "width": 220},
		{"fieldname": "doc_kind", "label": _("Kind"), "fieldtype": "Data", "width": 90},
		{"fieldname": "version", "label": _("Version"), "fieldtype": "Int", "width": 70},
		{"fieldname": "audience", "label": _("Audience"), "fieldtype": "Int", "width": 90},
		{"fieldname": "acknowledged", "label": _("Acknowledged"), "fieldtype": "Int", "width": 110},
		{"fieldname": "missing", "label": _("Not acknowledged"), "fieldtype": "Int", "width": 130},
		{"fieldname": "compliance", "label": _("Compliance"), "fieldtype": "Percent", "width": 110},
		{"fieldname": "next_review_date", "label": _("Next Review Date"), "fieldtype": "Date", "width": 130},
	]


def summary(rows):
	audience = sum(r["audience"] for r in rows)
	done = sum(r["acknowledged"] for r in rows)
	return [
		{"label": _("Documents"), "value": len(rows), "datatype": "Int"},
		{
			"label": _("Compliance"),
			"value": round(done * 100 / audience, 1) if audience else 100,
			"datatype": "Percent",
			"indicator": "Green",
		},
		{"label": _("Not acknowledged"), "value": audience - done, "datatype": "Int", "indicator": "Red"},
		{
			"label": _("Certificates expiring in 30 days"),
			"value": analytics.expiring_certificates(30),
			"datatype": "Int",
			"indicator": "Orange",
		},
	]
