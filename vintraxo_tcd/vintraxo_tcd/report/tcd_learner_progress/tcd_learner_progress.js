frappe.query_reports["TCD Learner Progress"] = {
	filters: [
		{ fieldname: "space", label: __("Space"), fieldtype: "Link", options: "TCD Space" },
		{
			fieldname: "content",
			label: __("Content"),
			fieldtype: "Link",
			options: "TCD Content",
			get_query: () => {
				const space = frappe.query_report.get_filter_value("space");
				return space ? { filters: { space } } : {};
			},
		},
		{ fieldname: "content_type", label: __("Type"), fieldtype: "Select", options: "\nArticle\nTutorial\nLesson\nReference" },
		{ fieldname: "status", label: __("Status"), fieldtype: "Select", options: "\nIn Progress\nCompleted" },
		{ fieldname: "user", label: __("Learner"), fieldtype: "Link", options: "User" },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "status" && data) {
			const color = data.status === "Completed" ? "green" : "orange";
			value = `<span class="indicator-pill ${color}">${frappe.utils.escape_html(__(data.status))}</span>`;
		}
		return value;
	},
};
