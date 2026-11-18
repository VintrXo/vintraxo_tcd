// Shared desk helpers for VintraXo TCD forms.

function tcd_offering_buttons(frm, enrollment_for) {
	if (frm.doc.status === "Published" && frappe.model.can_create("TCD Enrollment")) {
		frm.add_custom_button(__("Enroll Student Group"), () => {
			const d = new frappe.ui.Dialog({
				title: __("Enroll Student Group"),
				fields: [
					{ fieldname: "student_group", fieldtype: "Link", options: "TCD Student Group", label: __("Student Group"), reqd: 1 },
					{ fieldname: "due_date", fieldtype: "Date", label: __("Due Date") },
				],
				primary_action_label: __("Enroll"),
				primary_action(values) {
					frappe
						.call({
							method: "vintraxo_tcd.api.enroll_group",
							args: { ...values, enrollment_for, name: frm.doc.name },
							freeze: true,
						})
						.then((r) => {
							d.hide();
							const m = r.message || {};
							let msg = __("Enrolled: {0}", [m.enrolled?.length || 0]);
							if (m.skipped?.length) {
								msg += "<br>" + __("Skipped: {0}", [m.skipped.length]) + "<ul>";
								m.skipped.forEach((s) => (msg += `<li>${frappe.utils.escape_html(s.user)}: ${frappe.utils.escape_html(s.reason)}</li>`));
								msg += "</ul>";
							}
							frappe.msgprint(msg);
						});
				},
			});
			d.show();
		});
		frm.add_custom_button(__("Enrollments"), () => {
			const field = enrollment_for === "Course" ? "course" : "learning_path";
			frappe.set_route("List", "TCD Enrollment", { [field]: frm.doc.name });
		});
	}
	if (frm.doc.space && frm.doc.slug) {
		const kind = enrollment_for === "Course" ? "course" : "path";
		frm.add_custom_button(__("View in Portal"), () =>
			window.open(`/learn/${encodeURIComponent(frm.doc.space)}/${kind}/${encodeURIComponent(frm.doc.slug)}`, "_blank", "noopener")
		);
	}
}
window.tcd_offering_buttons = tcd_offering_buttons;
