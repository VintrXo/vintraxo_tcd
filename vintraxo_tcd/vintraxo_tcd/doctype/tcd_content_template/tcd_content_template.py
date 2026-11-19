from frappe.model.document import Document

from vintraxo_tcd.core.wiki import validate_template


class TCDContentTemplate(Document):
	def validate(self):
		validate_template(self)
