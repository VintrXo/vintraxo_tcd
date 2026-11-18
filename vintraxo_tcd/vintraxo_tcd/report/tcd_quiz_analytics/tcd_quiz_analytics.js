frappe.query_reports["TCD Quiz Analytics"] = {
	filters: [
		{ fieldname: "quiz", label: __("Quiz"), fieldtype: "Link", options: "TCD Quiz", reqd: 1 },
		{ fieldname: "from_date", label: __("From Date"), fieldtype: "Date" },
		{ fieldname: "to_date", label: __("To Date"), fieldtype: "Date" },
	],
	formatter(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname === "correct_rate" && data && data.correct_rate !== null) {
			const color = data.correct_rate >= 70 ? "green" : data.correct_rate >= 40 ? "orange" : "red";
			value = `<span style="color: var(--${color}-600)">${value}</span>`;
		}
		return value;
	},
};
