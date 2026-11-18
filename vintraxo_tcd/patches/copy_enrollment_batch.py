import frappe
from frappe.model.utils.rename_field import rename_field


def execute():
	"""ADR-0007: copy TCD Enrollment.student_group into the new `batch` field."""
	if frappe.db.has_column("TCD Enrollment", "student_group"):
		rename_field("TCD Enrollment", "student_group", "batch")
