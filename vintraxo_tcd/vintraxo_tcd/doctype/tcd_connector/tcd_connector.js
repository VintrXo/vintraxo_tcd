frappe.ui.form.on("TCD Connector", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Send Test"), () =>
			frappe
				.call("vintraxo_tcd.api.test_connector", { name: frm.doc.name })
				.then(({ message: r }) =>
					r.ok
						? frappe.show_alert({ message: __("Test sent ({0})", [r.status_code]), indicator: "green" })
						: frappe.msgprint(__("Test failed: {0}", [r.error || r.status_code]))
				)
		);
		frm.add_custom_button(__("Integration Log"), () =>
			frappe.set_route("List", "TCD Integration Event", { connector: frm.doc.name })
		);
	},
});
