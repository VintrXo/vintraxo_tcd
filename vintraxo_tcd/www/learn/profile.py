import frappe
from frappe import _

from vintraxo_tcd.core import careers, portal

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	user = frappe.form_dict.get("user") or frappe.session.user
	try:
		context.data = careers.view(user, frappe.session.user)
	except frappe.DoesNotExistError:
		raise frappe.PageDoesNotExistError from None
	if context.data.get("own"):
		context.countries = frappe.get_all("Country", pluck="name", order_by="name asc")
	context.labels_json = portal.json_for_script(portal.js_labels())
	context.title = context.data["full_name"]
	context.parents = [{"route": "/learn", "title": _("Learning")}]
	context.show_sidebar = False
