frappe.ui.form.on("TCD Session", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status === "Cancelled" || !frm.perm[0]?.write) return;
		frm.add_custom_button(__("Load Learners"), () =>
			frappe.xcall("vintraxo_tcd.api.load_session_learners", { name: frm.doc.name }).then((n) => {
				frappe.show_alert({ message: __("{0} learners added", [n]), indicator: "green" });
				frm.reload_doc();
			})
		);
		if (frm.doc.status === "Scheduled" && frm.doc.attendance?.length) {
			frm.add_custom_button(__("Everyone Present"), () => {
				(frm.doc.attendance || []).forEach((row) => row.status || frappe.model.set_value(row.doctype, row.name, "status", "Present"));
				frm.refresh_field("attendance");
			});
		}
	},
});
