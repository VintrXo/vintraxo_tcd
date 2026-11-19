/* VintraXo TCD: "AI lesson draft" on the TCD Content list (Phase 9). */
frappe.listview_settings["TCD Content"] = Object.assign(frappe.listview_settings["TCD Content"] || {}, {
	onload(list) {
		frappe.xcall("vintraxo_tcd.api.ai_status").then((r) => {
			if (!r.enabled || !frappe.model.can_create("TCD Content")) return;
			list.page.add_inner_button(__("AI lesson draft"), () => {
				const d = new frappe.ui.Dialog({
					title: __("AI lesson draft"),
					fields: [
						{ fieldname: "space", fieldtype: "Link", options: "TCD Space", label: __("Space"), reqd: 1 },
						{ fieldname: "title", fieldtype: "Data", label: __("Title"), reqd: 1 },
						{ fieldname: "instructions", fieldtype: "Small Text", label: __("What should the lesson cover?") },
					],
					primary_action_label: __("Write draft"),
					primary_action(values) {
						d.hide();
						frappe
							.xcall("vintraxo_tcd.api.ai_draft_lesson", values, "POST", { freeze: true, freeze_message: __("Writing the draft...") })
							.then((name) => frappe.set_route("Form", "TCD Content", name));
					},
				});
				d.show();
			});
		});
	},
});
