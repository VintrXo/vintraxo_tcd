import frappe
from frappe import _
from frappe.model.document import Document


class TCDCompetencyProfile(Document):
	def validate(self):
		seen = set()
		for row in self.requirements:
			if row.skill in seen:
				frappe.throw(_("Row {0}: {1} is listed twice.").format(row.idx, frappe.bold(row.skill)))
			seen.add(row.skill)
