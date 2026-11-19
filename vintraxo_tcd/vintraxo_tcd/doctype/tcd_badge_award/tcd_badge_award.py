from frappe.model.document import Document

from vintraxo_tcd.core import badges


class TCDBadgeAward(Document):
	def validate(self):
		badges.validate_award(self)
