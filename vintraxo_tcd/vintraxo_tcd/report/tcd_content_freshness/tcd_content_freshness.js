frappe.query_reports["TCD Content Freshness"] = {
	filters: [
		{ fieldname: "space", label: __("Space"), fieldtype: "Link", options: "TCD Space" },
		{ fieldname: "only_overdue", label: __("Only past review date"), fieldtype: "Check" },
	],
};
