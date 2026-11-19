import frappe
from frappe.model.document import Document

from vintraxo_tcd.core.credentials import validate_certificate


class TCDCertificate(Document):
	def validate(self):
		if self.is_new():
			validate_certificate(self)

	def on_update(self):
		if not self.is_new() and not self.flags.from_credentials and self.has_value_changed("user"):
			frappe.throw(frappe._("Certificates cannot be reassigned."))
