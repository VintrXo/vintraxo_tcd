import frappe
from frappe import _

from vintraxo_tcd.core import portal
from vintraxo_tcd.core.dashboards import my_learning

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	context.data = my_learning(frappe.session.user)
	context.title = _("My Learning")
	context.parents = [{"route": "/learn", "title": _("Learning")}]
	context.show_sidebar = False
	context.labels_json = portal.json_for_script(portal.js_labels())
