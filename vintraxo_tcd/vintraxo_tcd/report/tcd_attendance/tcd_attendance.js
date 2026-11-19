frappe.query_reports["TCD Attendance"] = {
	filters: [
		{ fieldname: "course", label: __("Course"), fieldtype: "Link", options: "TCD Course" },
		{ fieldname: "batch", label: __("Batch"), fieldtype: "Link", options: "TCD Batch" },
	],
};
