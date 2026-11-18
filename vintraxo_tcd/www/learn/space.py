import frappe

from vintraxo_tcd.core import portal

no_cache = 1


def get_context(context):
	portal.require_portal()
	context.update(portal.space_context(frappe.form_dict.get("space")))
	context.show_sidebar = False
