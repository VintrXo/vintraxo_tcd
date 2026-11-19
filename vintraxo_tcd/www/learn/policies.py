import frappe
from frappe import _

from vintraxo_tcd.core import governance, portal

no_cache = 1


@portal.portal_page
def get_context(context):
	portal.require_portal()
	kind = frappe.form_dict.get("kind")
	context.kind = kind if kind in ("Policy", "SOP", "Document") else ""
	context.documents = governance.documents_for(frappe.session.user, context.kind or None)
	context.title = _("Policies and procedures")
	context.parents = [{"route": "/learn", "title": _("Learning")}]
	context.show_sidebar = False
