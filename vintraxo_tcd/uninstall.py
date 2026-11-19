import frappe

from vintraxo_tcd.install import LEARN_URL


def before_uninstall():
	"""Remove what the app added outside its own DocTypes (the website navbar item)."""
	settings = frappe.get_single("Website Settings")
	kept = [row for row in settings.top_bar_items if row.url != LEARN_URL]
	if len(kept) != len(settings.top_bar_items):
		settings.set("top_bar_items", kept)
		settings.save(ignore_permissions=True)
