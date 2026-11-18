import frappe
from frappe import _
from frappe.model.document import Document

from vintraxo_tcd.core import courses
from vintraxo_tcd.core.permissions import can_access_content


class TCDEnrollment(Document):
	def validate(self):
		courses.validate_enrollment(self)
		if self.is_new():
			doctype, target = courses.offering_of(self)
			if not can_access_content(frappe.get_doc(doctype, target), self.user):
				frappe.throw(
					_("{0} cannot access this course or learning path.").format(frappe.bold(self.user))
				)

	def after_insert(self):
		if self.course:
			courses.refresh_course(self.user, self.course)
		elif self.learning_path:
			courses.refresh_path(self.user, self.learning_path)
