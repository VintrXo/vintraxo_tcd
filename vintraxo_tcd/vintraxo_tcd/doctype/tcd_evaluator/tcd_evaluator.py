from frappe.model.document import Document


class TCDEvaluator(Document):
	def validate(self):
		from vintraxo_tcd.core import evaluations

		evaluations.validate_evaluator(self)
