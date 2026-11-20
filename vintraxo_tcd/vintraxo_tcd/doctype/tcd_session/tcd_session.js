frappe.ui.form.on("TCD Session", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status === "Cancelled" || !frm.perm[0]?.write) return;
		frm.add_custom_button(__("Load Learners"), () =>
			frappe.xcall("vintraxo_tcd.api.load_session_learners", { name: frm.doc.name }).then((n) => {
				frappe.show_alert({ message: __("{0} learners added", [n]), indicator: "green" });
				frm.reload_doc();
			})
		);
		if (frm.doc.conferencing === "Zoom" && frm.doc.meeting_id && frappe.datetime.str_to_obj(frm.doc.ends_on) < new Date()) {
			frm.add_custom_button(__("Attendance from Zoom", null, "TCD"), () =>
				frappe.xcall("vintraxo_tcd.api.zoom_attendance", { session: frm.doc.name }, "POST", { freeze: true }).then((r) => {
					frappe.show_alert({ message: __("Present: {0}, absent: {1}, kept: {2}", [r.present, r.absent, r.kept], "TCD"), indicator: "green" });
					frm.reload_doc();
				})
			);
		}
		if (frm.doc.status === "Scheduled" && frm.doc.attendance?.length) {
			frm.add_custom_button(__("Everyone Present"), () => {
				(frm.doc.attendance || []).forEach((row) => row.status || frappe.model.set_value(row.doctype, row.name, "status", "Present"));
				frm.refresh_field("attendance");
			});
		}
	},
});
