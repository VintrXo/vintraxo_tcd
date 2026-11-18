import frappe
from frappe import _
from frappe.model.document import Document


class TCDProgress(Document):
	"""Written only through vintraxo_tcd.core.progress."""

	def validate(self):
		if not self.flags.ignore_permissions:
			frappe.throw(_("Progress is recorded automatically."))
		if frappe.db.exists(
			"TCD Progress", {"user": self.user, "content": self.content, "name": ("!=", self.name)}
		):
			frappe.throw(_("Progress for this user and content already exists."))
		self.percent = min(max(self.percent or 0, 0), 100)
