import frappe
from frappe.model.document import Document


class TCDSettings(Document):
	def validate(self):
		timeout = self.playground_timeout_seconds or 0
		if timeout < 1 or timeout > 60:
			frappe.throw("Playground timeout must be between 1 and 60 seconds.")
