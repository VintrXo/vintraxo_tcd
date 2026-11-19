import frappe

from vintraxo_tcd.core import portal

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal(allow_guest=True)
	context.is_guest = frappe.session.user == "Guest"
	context.update(portal.path_context(frappe.form_dict.get("space"), frappe.form_dict.get("slug")))
	context.labels_json = portal.json_for_script(context.js_labels)
	context.show_sidebar = False
