from frappe.model.document import Document

from vintraxo_tcd.core import careers


class TCDLearnerProfile(Document):
	def validate(self):
		careers.validate_profile(self)
