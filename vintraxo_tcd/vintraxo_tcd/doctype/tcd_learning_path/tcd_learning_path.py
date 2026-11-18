import frappe
from frappe import _
from frappe.model.document import Document

from vintraxo_tcd.core import courses
from vintraxo_tcd.core.content import ensure_unique_slug
from vintraxo_tcd.vintraxo_tcd.doctype.tcd_course.tcd_course import set_offering_defaults


class TCDLearningPath(Document):
	def validate(self):
		set_offering_defaults(self)
		ensure_unique_slug(self)
		courses.validate_path_items(self)
		before = self.get_doc_before_save()
		if before and before.status == "Published" and self.status == "Published":
			if [(r.course, r.is_optional) for r in before.items] != [
				(r.course, r.is_optional) for r in self.items
			]:
				frappe.throw(_("Move the learning path back to Draft to change its courses."))
		courses.validate_offering_status(self)

	def on_trash(self):
		if frappe.db.exists("TCD Enrollment", {"learning_path": self.name}):
			frappe.throw(_("Cannot delete a learning path that has enrollments. Archive it instead."))
