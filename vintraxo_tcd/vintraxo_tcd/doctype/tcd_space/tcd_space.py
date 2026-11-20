import re

import frappe
from frappe import _
from frappe.model.document import Document

RESERVED = {"my", "instructor", "course", "path", "search", "policies", "team", "profile", "jobs", "studio"}


class TCDSpace(Document):
	def validate(self):
		self.space_name = (self.space_name or "").strip().lower()
		if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,79}", self.space_name):
			frappe.throw(_("Space ID must be 2-80 characters: lowercase letters, digits, - or _."))
		if self.space_name in RESERVED:
			frappe.throw(
				_("{0} is a reserved name. Choose another Space ID.").format(frappe.bold(self.space_name))
			)
		roles = [r.role for r in self.allowed_roles]
		if len(roles) != len(set(roles)):
			frappe.throw(_("Each role can be listed only once."))
		if self.visibility == "Restricted" and not roles:
			frappe.msgprint(
				_("This Restricted space has no allowed roles, so only administrators can open it."),
				indicator="orange",
				alert=True,
			)

	def on_trash(self):
		if frappe.db.exists("TCD Content", {"space": self.name}):
			frappe.throw(
				_("Cannot delete a space that still has content. Archive or move the content first.")
			)
