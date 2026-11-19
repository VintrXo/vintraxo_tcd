frappe.query_reports["TCD Competency Gap"] = {
	filters: [
		{ fieldname: "profile", label: __("Competency Profile"), fieldtype: "Link", options: "TCD Competency Profile", reqd: 1 },
		{ fieldname: "user", label: __("User"), fieldtype: "Link", options: "User" },
		{ fieldname: "only_gaps", label: __("Only Gaps"), fieldtype: "Check" },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "gap" && data && data.gap > 0) value = `<span style="color: var(--red-600)">${value}</span>`;
		return value;
	},
};
