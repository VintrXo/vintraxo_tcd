import frappe
from frappe import _
from frappe.model.document import Document


class TCDCourseFeedback(Document):
	"""Written only through api.rate_course."""

	def validate(self):
		if not self.flags.from_api:
			frappe.throw(_("Course feedback is given from the course page."))
		if not 1 <= int(self.rating or 0) <= 5:
			frappe.throw(_("Rating must be between 1 and 5."))
		if frappe.db.exists(
			"TCD Course Feedback", {"course": self.course, "user": self.user, "name": ("!=", self.name)}
		):
			frappe.throw(_("You already rated this course."))
