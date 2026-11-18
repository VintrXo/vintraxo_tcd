import frappe
from frappe import _
from frappe.model.document import Document


class TCDContentRelation(Document):
	def validate(self):
		if self.from_content == self.to_content:
			frappe.throw(_("Content cannot be related to itself."))
		filters = {
			"from_content": self.from_content,
			"to_content": self.to_content,
			"relation_type": self.relation_type,
			"name": ("!=", self.name),
		}
		if frappe.db.exists("TCD Content Relation", filters):
			frappe.throw(_("This relation already exists."))
		if self.relation_type in ("Prerequisite", "Next") and frappe.db.exists(
			"TCD Content Relation",
			{
				"from_content": self.to_content,
				"to_content": self.from_content,
				"relation_type": self.relation_type,
			},
		):
			frappe.throw(_("The reverse {0} relation already exists.").format(_(self.relation_type)))
