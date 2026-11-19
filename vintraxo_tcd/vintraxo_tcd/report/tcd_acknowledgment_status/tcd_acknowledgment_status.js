frappe.query_reports["TCD Acknowledgment Status"] = {
	filters: [
		{ fieldname: "document", label: __("Document"), fieldtype: "Link", options: "TCD Governance Document", reqd: 1 },
		{ fieldname: "only_missing", label: __("Only not acknowledged"), fieldtype: "Check" },
	],
};
