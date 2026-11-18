from frappe.model.document import Document

from vintraxo_tcd.core.assignments import validate_assignment


class TCDAssignment(Document):
	def validate(self):
		validate_assignment(self)
