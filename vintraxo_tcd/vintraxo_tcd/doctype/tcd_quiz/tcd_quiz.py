from frappe.model.document import Document

from vintraxo_tcd.core.quiz import validate_quiz


class TCDQuiz(Document):
	def validate(self):
		validate_quiz(self)
