import frappe

from vintraxo_tcd.core import portal

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal(allow_guest=True)
	context.is_guest = frappe.session.user == "Guest"
	context.update(portal.space_context(frappe.form_dict.get("space")))
	context.show_sidebar = False
