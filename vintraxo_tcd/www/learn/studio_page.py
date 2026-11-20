import frappe
from frappe import _

from vintraxo_tcd.core import portal, studio

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	if not studio.can_author():
		raise frappe.PageDoesNotExistError
	name = frappe.form_dict.get("name")
	try:
		data = studio.page_data(name)
	except (frappe.PermissionError, frappe.DoesNotExistError):
		raise frappe.PageDoesNotExistError from None
	context.data = data
	context.spaces = studio.spaces_for_authoring()
	context.is_reviewer = studio.is_reviewer()
	context.doc_json = portal.json_for_script(data["doc"])
	context.spec_json = portal.json_for_script(studio.block_spec())
	context.studio_labels_json = portal.json_for_script(studio.labels())
	context.labels_json = portal.json_for_script(portal.js_labels())
	context.title = data["doc"].get("title") or _("New page")
	context.parents = [
		{"route": "/learn", "title": _("Learning")},
		{"route": "/learn/studio", "title": _("Studio")},
	]
	context.show_sidebar = False
