frappe.ui.form.on("TCD Enrollment", {
	refresh(frm) {
		if (frm.doc.status === "Pending Approval" && !frm.is_new()) {
			frm.add_custom_button(__("Approve Completion"), () =>
				frappe
					.call({ method: "vintraxo_tcd.api.approve_enrollment", args: { name: frm.doc.name }, freeze: true })
					.then(() => frm.reload_doc())
			).addClass("btn-primary");
		}
		frm.set_query("course", () => ({ filters: { status: "Published" } }));
		frm.set_query("learning_path", () => ({ filters: { status: "Published" } }));
	},
});
