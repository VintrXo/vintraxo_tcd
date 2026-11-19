from frappe.model.document import Document

from vintraxo_tcd.core import teams


class TCDTeam(Document):
	def validate(self):
		teams.validate_team(self)
