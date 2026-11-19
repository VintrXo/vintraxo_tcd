import frappe
from frappe.utils import getdate


def execute():
	"""Published pages created before Phase 12 get an owner and a review date from their publish date."""
	from vintraxo_tcd.core import freshness

	# the new setting has no stored value on existing sites: store its default once
	if not frappe.db.exists("Singles", {"doctype": "TCD Settings", "field": "default_review_months"}):
		frappe.db.set_single_value("TCD Settings", "default_review_months", freshness.DEFAULT_MONTHS)

	for name in frappe.get_all(
		"TCD Content",
		filters=[["status", "=", "Published"], ["next_review_date", "is", "not set"]],
		pluck="name",
	):
		doc = frappe.get_doc("TCD Content", name)
		freshness.schedule(doc, getdate(doc.published_on or doc.modified))
		doc.db_set(
			{
				"content_owner": doc.content_owner or doc.owner,
				"last_reviewed_on": doc.last_reviewed_on,
				"next_review_date": doc.next_review_date,
			},
			update_modified=False,
		)
