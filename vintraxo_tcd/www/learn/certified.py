import frappe
from frappe import _

from vintraxo_tcd.core import community, portal

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	course = frappe.form_dict.get("course") or None
	context.stats = community.stats()
	context.rows = community.certified(course)
	context.courses = community.course_options()
	context.course = course
	context.labels_json = portal.json_for_script(portal.js_labels())
	context.title = _("Certified learners")
	context.parents = [{"route": "/learn", "title": _("Learning")}]
	context.show_sidebar = False
