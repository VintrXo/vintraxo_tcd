import frappe
from frappe import _

from vintraxo_tcd.core import portal
from vintraxo_tcd.core.dashboards import instructor_dashboard
from vintraxo_tcd.core.permissions import is_admin, is_staff

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	user = frappe.session.user
	if not (is_admin(user) or (is_staff(user) and "TCD Instructor" in frappe.get_roles(user))):
		raise frappe.PageDoesNotExistError
	context.data = instructor_dashboard(user)
	from vintraxo_tcd.core import evaluations

	context.evaluations = evaluations.for_evaluator(user)
	context.title = _("Instructor Dashboard")
	context.parents = [{"route": "/learn", "title": _("Learning")}]
	context.labels_json = portal.json_for_script(portal.js_labels())
	context.show_sidebar = False
