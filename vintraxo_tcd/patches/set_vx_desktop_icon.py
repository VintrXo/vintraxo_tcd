import frappe


def execute():
	"""Brand the desk icon as VX (existing sites keep the old label otherwise)."""
	if frappe.db.exists("Desktop Icon", "VintraXo TCD"):
		frappe.db.set_value(
			"Desktop Icon",
			"VintraXo TCD",
			{"label": "VX", "logo_url": "/assets/vintraxo_tcd/images/vx-logo.png"},
		)
