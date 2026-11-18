import frappe
from frappe import _
from frappe.model.document import Document


class TCDStudentGroup(Document):
	def validate(self):
		seen = set()
		for row in self.members:
			if row.user in seen:
				frappe.throw(_("Row {0}: {1} is listed twice.").format(row.idx, frappe.bold(row.user)))
			seen.add(row.user)
