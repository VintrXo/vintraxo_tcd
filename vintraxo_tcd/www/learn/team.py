import frappe
from frappe import _

from vintraxo_tcd.core import portal, teams
from vintraxo_tcd.core.permissions import is_admin

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	user = frappe.session.user
	if not (teams.is_manager(user) or is_admin(user)):
		raise frappe.PageDoesNotExistError
	team = frappe.form_dict.get("team") or None
	try:
		context.data = teams.overview(user, team)
	except frappe.PermissionError:
		raise frappe.PageDoesNotExistError from None
	context.title = _("My Team")
	context.parents = [{"route": "/learn", "title": _("Learning")}]
	context.show_sidebar = False
