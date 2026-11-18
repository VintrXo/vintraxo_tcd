import frappe
from frappe import _
from frappe.model.document import Document

from vintraxo_tcd.core import courses


class TCDChapter(Document):
	def validate(self):
		courses.validate_chapter(self)

	def on_trash(self):
		if (
			frappe.db.get_value("TCD Course", self.course, "status") == "Published"
			and not self.flags.ignore_permissions
		):
			frappe.throw(_("Move the course back to Draft to change its chapters."))
