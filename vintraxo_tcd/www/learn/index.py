import frappe
from frappe import _

from vintraxo_tcd.core import portal

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal(allow_guest=True)
	context.is_guest = frappe.session.user == "Guest"
	from vintraxo_tcd.core import studio

	context.can_author = studio.can_author()
	context.full_name = "" if context.is_guest else frappe.utils.get_fullname(frappe.session.user)
	form = frappe.form_dict
	request = getattr(frappe.local, "request", None)
	picked = request.args.getlist("t") if request else []
	types = ",".join(picked) or form.get("types")
	context.update(portal.home_context(form.get("q"), types, form.get("space"), form.get("tag")))
	context.title = _("Learning")
	context.show_sidebar = False
