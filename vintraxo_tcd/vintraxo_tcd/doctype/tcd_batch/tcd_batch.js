frappe.ui.form.on("TCD Batch", {
	refresh(frm) {
		if (frm.is_new() || !(frm.doc.timetable || []).length) return;
		frm.add_custom_button(__("Generate Sessions", null, "TCD"), () =>
			frappe.confirm(__("Create the sessions of the weekly timetable between the start and end dates?", null, "TCD"), () =>
				frappe.xcall("vintraxo_tcd.api.generate_batch_sessions", { batch: frm.doc.name }, "POST", { freeze: true }).then((r) => {
					frappe.msgprint(__("Sessions created: {0}. Already there: {1}.", [r.created, r.skipped], "TCD"));
				})
			)
		);
	},
});
