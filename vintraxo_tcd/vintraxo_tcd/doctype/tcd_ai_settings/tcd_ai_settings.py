from frappe.model.document import Document

from vintraxo_tcd.core import ai


class TCDAISettings(Document):
	def validate(self):
		ai.validate_settings(self)
