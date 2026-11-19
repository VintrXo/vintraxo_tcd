frappe.query_reports["TCD Training Compliance"] = {
	filters: [
		{
			fieldname: "training_rule",
			label: __("Training Rule"),
			fieldtype: "Link",
			options: "TCD Training Rule",
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Data",
		},
	],
};
