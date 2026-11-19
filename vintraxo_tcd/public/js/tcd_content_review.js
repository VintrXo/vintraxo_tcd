/* VintraXo TCD: review cycle actions on TCD Content (Phase 12). */
frappe.ui.form.on("TCD Content", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status !== "Published" || !frm.perm[0]?.write) return;
		if (frm.doc.next_review_date && frappe.datetime.get_diff(frm.doc.next_review_date, frappe.datetime.get_today()) < 0) {
			frm.dashboard.set_headline_alert(__("This page is past its review date."), "orange");
		}
		frm.add_custom_button(__("Mark as Reviewed"), () =>
			frappe.xcall("vintraxo_tcd.api.confirm_content_review", { name: frm.doc.name }).then(() => {
				frappe.show_alert({ message: __("Review recorded"), indicator: "green" });
				frm.reload_doc();
			})
		);
	},
});
