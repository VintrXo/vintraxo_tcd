// Grade or return a submission (instructors of the course).
frappe.ui.form.on("TCD Assignment Submission", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status === "Graded" || !frm.perm?.[0]?.write) return;
		const act = (action) => {
			const fields = [{ fieldname: "feedback", fieldtype: "Small Text", label: __("Feedback"), reqd: action === "Returned" }];
			if (action === "Graded") fields.unshift({ fieldname: "score", fieldtype: "Float", label: __("Score"), reqd: 1 });
			const d = new frappe.ui.Dialog({
				title: action === "Graded" ? __("Grade") : __("Return for changes"),
				fields,
				primary_action_label: action === "Graded" ? __("Grade") : __("Return"),
				primary_action(values) {
					frappe
						.call({ method: "vintraxo_tcd.api.grade_submission", args: { name: frm.doc.name, action, ...values }, freeze: true })
						.then(() => {
							d.hide();
							frm.reload_doc();
						});
				},
			});
			d.show();
		};
		frm.add_custom_button(__("Grade"), () => act("Graded")).addClass("btn-primary");
		frm.add_custom_button(__("Return for changes"), () => act("Returned"));
	},
});
