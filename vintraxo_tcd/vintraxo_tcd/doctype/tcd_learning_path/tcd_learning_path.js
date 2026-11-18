frappe.ui.form.on("TCD Learning Path", {
	refresh(frm) {
		if (!frm.is_new() && window.tcd_offering_buttons) window.tcd_offering_buttons(frm, "Learning Path");
		frm.set_query("course", "items", () => ({ filters: { space: frm.doc.space } }));
	},
});
