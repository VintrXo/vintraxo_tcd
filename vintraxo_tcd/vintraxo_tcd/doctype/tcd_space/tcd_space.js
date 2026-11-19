frappe.ui.form.on("TCD Space", {
	refresh(frm) {
		if (frm.is_new() || !frappe.user.has_role(["TCD Administrator", "System Manager"])) return;
		frm.add_custom_button(__("Export Space"), () => {
			window.open(`/api/method/vintraxo_tcd.api.export_space?space=${encodeURIComponent(frm.doc.name)}`);
		});
		if (frm.doc.github_repo) {
			const sync = (method) =>
				frappe.xcall(`vintraxo_tcd.api.${method}`, { space: frm.doc.name }, "POST", { freeze: true }).then((r) => {
					frappe.msgprint(Object.entries(r).map(([k, v]) => `${frappe.utils.escape_html(__(k))}: ${v}`).join("<br>"));
					frm.reload_doc();
				});
			frm.add_custom_button(__("Push to GitHub"), () => sync("github_push"), __("GitHub"));
			frm.add_custom_button(__("Pull from GitHub"), () => sync("github_pull"), __("GitHub"));
		}
	},
});
