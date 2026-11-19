from frappe.model.document import Document

from vintraxo_tcd.core import careers


class TCDJobApplication(Document):
	def validate(self):
		careers.validate_application(self)
