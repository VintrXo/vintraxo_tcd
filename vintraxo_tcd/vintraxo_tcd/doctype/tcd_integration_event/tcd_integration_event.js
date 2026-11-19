frappe.ui.form.on("TCD Integration Event", {
	refresh(frm) {
		if (frm.doc.status === "Sent") return;
		frm.add_custom_button(__("Retry Now"), () =>
			frappe
				.call("vintraxo_tcd.api.retry_integration_event", { name: frm.doc.name })
				.then(() => frm.reload_doc())
		);
	},
});
