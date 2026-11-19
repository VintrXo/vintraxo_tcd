frappe.ui.form.on("TCD Settings", {
	refresh(frm) {
		if (!frm.doc.runner_enabled) return;
		frm.add_custom_button(__("Test Runner"), () =>
			frappe.xcall("vintraxo_tcd.api.test_runner", {}, "POST", { freeze: true }).then((r) => {
				const unknown = r.unknown.length ? __("Unknown language ids: {0}", [r.unknown.join(", ")]) : __("All languages found.");
				frappe.msgprint({
					title: __("Code runner"),
					indicator: r.unknown.length ? "orange" : "green",
					message: `${__("Version")}: ${frappe.utils.escape_html(r.version || "?")}<br>${__("Languages on the runner")}: ${r.available}<br>${frappe.utils.escape_html(unknown)}`,
				});
			})
		);
	},
});
