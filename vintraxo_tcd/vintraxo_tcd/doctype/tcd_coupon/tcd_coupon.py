from frappe.model.document import Document

from vintraxo_tcd.core import payments


class TCDCoupon(Document):
	def autoname(self):
		self.code = (self.code or "").strip().upper()
		self.name = self.code

	def validate(self):
		payments.validate_coupon_doc(self)
