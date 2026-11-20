import frappe
from frappe import _

from vintraxo_tcd.core import portal, studio

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	if not studio.can_author():
		raise frappe.PageDoesNotExistError
	context.data = studio.home()
	context.labels_json = portal.json_for_script(portal.js_labels())
	context.title = _("Studio")
	context.parents = [{"route": "/learn", "title": _("Learning")}]
	context.show_sidebar = False
