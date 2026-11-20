from frappe.model.document import Document


class TCDBatchFeedback(Document):
	def validate(self):
		from vintraxo_tcd.core import batches

		batches.validate_feedback(self)
