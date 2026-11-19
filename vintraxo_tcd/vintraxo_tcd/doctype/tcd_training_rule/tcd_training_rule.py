from frappe.model.document import Document

from vintraxo_tcd.core import training


class TCDTrainingRule(Document):
	def validate(self):
		training.validate_rule(self)

	def on_update(self):
		training.on_rule_update(self)
