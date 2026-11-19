import frappe
from frappe import _

from vintraxo_tcd import api
from vintraxo_tcd.core import portal

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	try:
		context.policy = api.get_policy(frappe.form_dict.get("code"))
	except frappe.DoesNotExistError:
		raise frappe.PageDoesNotExistError from None
	doc = frappe.get_doc("TCD Governance Document", context.policy["code"])
	from vintraxo_tcd.core.connect import _item

	context.linked = [
		i
		for i in (
			_item("TCD Content", r.content) if r.target_type == "Content" else _item("TCD Course", r.course)
			for r in doc.links
		)
		if i
	]
	context.title = context.policy["title"]
	context.parents = [
		{"route": "/learn", "title": _("Learning")},
		{"route": "/learn/policies", "title": _("Policies and procedures")},
	]
	context.labels_json = portal.json_for_script(portal.js_labels())
	context.show_sidebar = False
