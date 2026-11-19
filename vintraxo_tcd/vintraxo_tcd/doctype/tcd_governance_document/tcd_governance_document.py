from frappe.model.document import Document

from vintraxo_tcd.core import governance


class TCDGovernanceDocument(Document):
	def autoname(self):
		self.code = (self.code or "").strip().upper()
		self.name = self.code

	def validate(self):
		governance.validate(self)

	def on_update(self):
		governance.on_update(self)
