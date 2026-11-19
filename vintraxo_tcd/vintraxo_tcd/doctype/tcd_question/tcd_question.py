from frappe.model.document import Document

from vintraxo_tcd.core.assessment import validate_question


class TCDQuestion(Document):
	def validate(self):
		validate_question(self)
