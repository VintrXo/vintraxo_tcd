// TCD Course: enroll a student group, open in portal.
frappe.ui.form.on("TCD Course", {
	refresh(frm) {
		if (frm.is_new()) return;
		window.tcd_offering_buttons(frm, "Course");
		frm.add_custom_button(__("Chapters"), () => frappe.set_route("List", "TCD Chapter", { course: frm.doc.name }));
	},
});
