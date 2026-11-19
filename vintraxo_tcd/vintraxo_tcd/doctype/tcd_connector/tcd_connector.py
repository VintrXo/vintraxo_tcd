from frappe.model.document import Document

from vintraxo_tcd.core import integrations


class TCDConnector(Document):
	def validate(self):
		integrations.validate_connector(self)
