import frappe


def execute():
	"""ADR-0007: TCD Student Group -> TCD Batch (tables only; files are already renamed in the app)."""
	for old, new in (("TCD Student Group Member", "TCD Batch Member"), ("TCD Student Group", "TCD Batch")):
		if frappe.db.exists("DocType", old) and not frappe.db.exists("DocType", new):
			frappe.rename_doc("DocType", old, new, force=True)
