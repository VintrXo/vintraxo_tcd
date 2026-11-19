from frappe.model.document import Document

from vintraxo_tcd.core import change_requests


class TCDChangeRequest(Document):
	def validate(self):
		change_requests.validate(self)
