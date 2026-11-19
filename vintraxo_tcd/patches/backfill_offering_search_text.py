import frappe

from vintraxo_tcd.core.connect import course_search_text


def execute():
	"""ADR-0011: fill search_text for existing courses and learning paths."""
	for doctype in ("TCD Course", "TCD Learning Path"):
		if not frappe.db.has_column(doctype, "search_text"):
			continue
		for name in frappe.get_all(doctype, pluck="name"):
			doc = frappe.get_doc(doctype, name)
			doc.db_set("search_text", course_search_text(doc), update_modified=False)
