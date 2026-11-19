import frappe
from frappe import _
from frappe.model.document import Document


class TCDContentFeedback(Document):
	"""Written only through api.content_feedback."""

	def validate(self):
		if not self.flags.from_api:
			frappe.throw(_("Page feedback is given from the page."))
		if frappe.db.exists(
			"TCD Content Feedback", {"content": self.content, "user": self.user, "name": ("!=", self.name)}
		):
			frappe.throw(_("You already gave feedback on this page."))
