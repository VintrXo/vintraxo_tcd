import frappe
from frappe.model.document import Document

from vintraxo_tcd.core import payments


class TCDPayment(Document):
	def validate(self):
		if self.is_new() and not self.flags.from_service:
			frappe.throw(frappe._("Payments are created by the checkout."))

	def on_payment_authorized(self, status=None):
		"""Frappe Payments calls this after the gateway confirms (or fails) the payment."""
		payments.on_payment_authorized(self, status)
