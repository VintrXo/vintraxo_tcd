import frappe
from frappe import _
from frappe.model.document import Document

from vintraxo_tcd.core import courses
from vintraxo_tcd.core.content import ensure_unique_slug


def set_offering_defaults(doc):
	if not doc.language or not doc.visibility:
		settings = frappe.get_cached_doc("TCD Settings")
		doc.language = doc.language or settings.default_language or "ar"
		doc.visibility = doc.visibility or settings.default_visibility or "Internal"
	if doc.completion_rule == "Minimum Score" and not 0 < (doc.minimum_score or 0) <= 100:
		frappe.throw(_("Minimum score must be between 1 and 100."))


class TCDCourse(Document):
	def validate(self):
		set_offering_defaults(self)
		if self.category and frappe.db.get_value("TCD Category", self.category, "space") != self.space:
			frappe.throw(_("Category must belong to the same space."))
		ensure_unique_slug(self)
		courses.validate_offering_status(self)

	def on_trash(self):
		if frappe.db.exists("TCD Enrollment", {"course": self.name}):
			frappe.throw(_("Cannot delete a course that has enrollments. Archive it instead."))
		if courses.paths_with_course(self.name):
			frappe.throw(_("Remove this course from its learning paths first."))
		for chapter in frappe.get_all("TCD Chapter", filters={"course": self.name}, pluck="name"):
			frappe.delete_doc("TCD Chapter", chapter, ignore_permissions=True, force=True)
