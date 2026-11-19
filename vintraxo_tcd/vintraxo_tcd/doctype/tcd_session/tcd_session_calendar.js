frappe.views.calendar["TCD Session"] = {
	field_map: { start: "starts_on", end: "ends_on", id: "name", title: "title", allDay: 0 },
	filters: [
		{ fieldname: "course", fieldtype: "Link", options: "TCD Course", label: __("Course") },
		{ fieldname: "batch", fieldtype: "Link", options: "TCD Batch", label: __("Batch") },
	],
	get_events_method: "frappe.desk.calendar.get_events",
};
