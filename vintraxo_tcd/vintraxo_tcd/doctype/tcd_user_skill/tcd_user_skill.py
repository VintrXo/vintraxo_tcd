from frappe.model.document import Document

from vintraxo_tcd.core.credentials import validate_user_skill


class TCDUserSkill(Document):
	def validate(self):
		validate_user_skill(self)
