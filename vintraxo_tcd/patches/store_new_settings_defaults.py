import frappe

# Settings added after a site was created have no stored value, and Frappe then reads Check/Int fields as 0,
# which would silently turn these features off on existing sites.
DEFAULTS = {
	"enable_discussions": 1,
	"sync_training_to_hr": 1,
	"enable_change_requests": 1,
	"default_review_months": 12,
	"runner_cpu_seconds": 5,
	"runner_wall_seconds": 10,
	"runner_memory_mb": 256,
	"runner_runs_per_minute": 10,
	"zoom_attendance_percent": 50,
}


def execute():
	for field, value in DEFAULTS.items():
		if not frappe.db.exists("Singles", {"doctype": "TCD Settings", "field": field}):
			frappe.db.set_single_value("TCD Settings", field, value)
