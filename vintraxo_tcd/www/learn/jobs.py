import frappe
from frappe import _

from vintraxo_tcd.core import careers, portal

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	context.jobs = careers.open_jobs(frappe.session.user)
	context.labels_json = portal.json_for_script(portal.js_labels())
	context.title = _("Internal jobs")
	context.parents = [{"route": "/learn", "title": _("Learning")}]
	context.show_sidebar = False
