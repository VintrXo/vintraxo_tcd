import frappe
from frappe import _
from frappe.model.document import Document


class TCDAssignmentSubmission(Document):
	"""Written only through api.submit_assignment / api.grade_submission."""

	def validate(self):
		if not self.flags.from_api:
			frappe.throw(_("Use the submit and grade actions to change submissions."))
		if frappe.db.exists(
			"TCD Assignment Submission",
			{"assignment": self.assignment, "user": self.user, "name": ("!=", self.name)},
		):
			frappe.throw(_("A submission for this assignment already exists."))
