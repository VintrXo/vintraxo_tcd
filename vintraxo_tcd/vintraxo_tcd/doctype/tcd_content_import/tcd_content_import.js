frappe.ui.form.on("TCD Content Import", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status === "Completed" || !frm.doc.import_file) return;
		frm.add_custom_button(__("Start Import"), () =>
			frappe
				.xcall("vintraxo_tcd.api.run_content_import", { name: frm.doc.name }, "POST", { freeze: true, freeze_message: __("Importing...") })
				.then(() => frm.reload_doc())
				.catch(() => frm.reload_doc())
		);
	},
});
