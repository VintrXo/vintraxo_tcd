import frappe
from frappe import _

from vintraxo_tcd.core.credentials import verify

no_cache = 1


def get_context(context):
	"""Public certificate verification: minimal facts only (ADR-0014)."""
	code = frappe.form_dict.get("code")
	row = verify(code)
	if not row:
		context.http_status_code = 404
		context.found = False
	else:
		context.found = True
		context.cert = {
			k: row[k] for k in ("full_name", "title", "certificate_for", "issued_on", "expires_on", "status")
		}
	context.title = _("Certificate verification")
	context.show_sidebar = False
	context.no_breadcrumbs = True
