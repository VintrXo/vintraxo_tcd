import frappe

from vintraxo_tcd.core import portal

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal(allow_guest=True)
	context.is_guest = frappe.session.user == "Guest"
	form = frappe.form_dict
	context.update(
		portal.content_context(form.get("space"), form.get("slug"), form.get("tutorial"), form.get("course"))
	)
	context.labels_json = portal.json_for_script(context.js_labels)
	context.playground_json = portal.json_for_script(context.lesson["playground"])
	context.show_sidebar = False
