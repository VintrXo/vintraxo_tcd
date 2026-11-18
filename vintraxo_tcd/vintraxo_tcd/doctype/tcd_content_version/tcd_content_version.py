import frappe
from frappe import _
from frappe.model.document import Document


class TCDContentVersion(Document):
	"""Immutable snapshot of approved content. Created only by TCD Content."""

	def validate(self):
		if self.is_new():
			if not self.flags.from_content:
				frappe.throw(_("Content versions are created automatically on approval."))
			return
		frappe.throw(_("Content versions cannot be changed."))
