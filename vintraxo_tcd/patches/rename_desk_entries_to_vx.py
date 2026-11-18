import frappe


def execute():
	"""Desk looks up an icon's sidebar by the icon label, so icon and sidebar must both be "VX"."""
	for doctype in ("Workspace Sidebar", "Desktop Icon"):
		if frappe.db.exists(doctype, "VintraXo TCD") and not frappe.db.exists(doctype, "VX"):
			frappe.rename_doc(doctype, "VintraXo TCD", "VX", force=True)
	if frappe.db.exists("Workspace Sidebar", "VX"):
		frappe.db.set_value("Workspace Sidebar", "VX", "title", "VX")
	if frappe.db.exists("Desktop Icon", "VX"):
		frappe.db.set_value(
			"Desktop Icon",
			"VX",
			{"label": "VX", "link_to": "VX", "logo_url": "/assets/vintraxo_tcd/images/vx-logo.png"},
		)
