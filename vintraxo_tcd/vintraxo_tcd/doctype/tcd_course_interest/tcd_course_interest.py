import frappe
from frappe import _
from frappe.model.document import Document


class TCDCourseInterest(Document):
	def validate(self):
		if self.is_new() and not self.flags.from_service:
			frappe.throw(_("Learners ask to be notified from the course page."))
