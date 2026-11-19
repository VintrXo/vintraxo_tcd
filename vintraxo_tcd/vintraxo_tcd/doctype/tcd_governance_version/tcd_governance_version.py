import frappe
from frappe import _
from frappe.model.document import Document


class TCDGovernanceVersion(Document):
	"""Immutable record written only by vintraxo_tcd.core.governance."""

	def validate(self):
		if self.is_new() and self.flags.from_governance:
			return
		frappe.throw(_("This record is written automatically and cannot be changed."))

	def on_trash(self):
		if not frappe.flags.in_test and not frappe.flags.in_patch:
			frappe.throw(_("Audit records cannot be deleted."))
