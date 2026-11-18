import frappe
from frappe import _
from frappe.model.document import Document


class TCDQuizSubmission(Document):
	"""Immutable graded attempt, created only by vintraxo_tcd.core.quiz.grade."""

	def validate(self):
		if self.is_new() and self.flags.from_quiz:
			return
		frappe.throw(_("Quiz submissions are created by submitting the quiz and cannot be changed."))
