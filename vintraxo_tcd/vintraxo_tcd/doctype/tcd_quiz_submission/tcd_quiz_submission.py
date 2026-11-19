import frappe
from frappe import _
from frappe.model.document import Document


class TCDQuizSubmission(Document):
	"""Written only by vintraxo_tcd.core.quiz (start, submit, review)."""

	def validate(self):
		if self.flags.from_quiz:
			return
		frappe.throw(_("Quiz submissions are created by submitting the quiz and cannot be changed."))
