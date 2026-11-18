import frappe
from frappe import _
from frappe.model.document import Document


class TCDBatch(Document):
	def validate(self):
		if self.start_date and self.end_date and self.end_date < self.start_date:
			frappe.throw(_("End date cannot be before start date."))
		seen = set()
		for row in self.members:
			if row.user in seen:
				frappe.throw(_("Row {0}: {1} is listed twice.").format(row.idx, frappe.bold(row.user)))
			seen.add(row.user)
