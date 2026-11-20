from frappe.model.document import Document


class TCDEvaluation(Document):
	def validate(self):
		from vintraxo_tcd.core import evaluations

		evaluations.validate_evaluation(self)
