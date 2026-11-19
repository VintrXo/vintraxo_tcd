from frappe.model.document import Document

from vintraxo_tcd.core import sessions


class TCDSession(Document):
	def validate(self):
		sessions.validate(self)

	def on_update(self):
		sessions.on_update(self)
