from frappe.model.document import Document

from vintraxo_tcd.core.connect import validate_relation


class TCDContentRelation(Document):
	def validate(self):
		validate_relation(self)
