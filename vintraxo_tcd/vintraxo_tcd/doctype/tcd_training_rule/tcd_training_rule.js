frappe.ui.form.on("TCD Training Rule", {
	refresh(frm) {
		if (frm.is_new() || !frm.doc.enabled || frm.doc.target_type === "Content") return;
		frm.add_custom_button(__("Apply Now"), () =>
			frappe
				.call("vintraxo_tcd.api.apply_training_rule", { name: frm.doc.name })
				.then(({ message: n }) => {
					frappe.show_alert({ message: __("{0} users enrolled", [n]), indicator: "green" });
					frm.reload_doc();
				})
		);
	},
});
