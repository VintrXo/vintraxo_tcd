import frappe
from frappe import _
from frappe.model.document import Document


class TCDCategory(Document):
	def validate(self):
		self.category_name = (self.category_name or "").strip()
		self.validate_parent()
		self.validate_unique_name()

	def validate_parent(self):
		if not self.parent_category:
			return
		seen = {self.name}
		parent = self.parent_category
		while parent:
			if parent in seen:
				frappe.throw(_("Parent Category would create a loop."))
			seen.add(parent)
			space, next_parent = frappe.db.get_value(
				"TCD Category", parent, ["space", "parent_category"]
			) or (
				None,
				None,
			)
			if parent == self.parent_category and space != self.space:
				frappe.throw(_("Parent Category must belong to the same space."))
			parent = next_parent

	def validate_unique_name(self):
		filters = {
			"space": self.space,
			"category_name": self.category_name,
			"parent_category": self.parent_category or ("is", "not set"),
			"name": ("!=", self.name),
		}
		if frappe.db.exists("TCD Category", filters):
			frappe.throw(
				_("A category named {0} already exists here.").format(frappe.bold(self.category_name))
			)

	def on_trash(self):
		if frappe.db.exists("TCD Category", {"parent_category": self.name}):
			frappe.throw(_("Cannot delete a category that has sub-categories."))
		if frappe.db.exists("TCD Content", {"category": self.name}):
			frappe.throw(_("Cannot delete a category that has content."))
