import frappe
from frappe import _

from vintraxo_tcd.core import portal

no_cache = 1


def get_context(context):
	portal.require_portal()
	context.update(portal.home_context(frappe.form_dict.get("q")))
	context.title = _("Learning")
	context.show_sidebar = False
