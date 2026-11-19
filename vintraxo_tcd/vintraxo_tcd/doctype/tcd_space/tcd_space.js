frappe.ui.form.on("TCD Space", {
	refresh(frm) {
		if (frm.is_new() || !frappe.user.has_role(["TCD Administrator", "System Manager"])) return;
		frm.add_custom_button(__("Export Space"), () => {
			window.open(`/api/method/vintraxo_tcd.api.export_space?space=${encodeURIComponent(frm.doc.name)}`);
		});
	},
});
