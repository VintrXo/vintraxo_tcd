/* VintraXo TCD: AI actions on TCD Content (Phase 9). Shown only when AI is enabled for the user. */
(function () {
	const status = () =>
		frappe.xcall("vintraxo_tcd.api.ai_status").then((r) => r.enabled).catch(() => false);

	function showSummary(text) {
		const d = new frappe.ui.Dialog({ title: __("AI summary") });
		const box = document.createElement("div");
		box.style.whiteSpace = "pre-wrap";
		box.textContent = text; // plain text, never HTML
		d.$body.append(box);
		d.$body.append(`<p class="text-muted small">${__("Written by AI. Check it against the page.")}</p>`);
		d.show();
	}

	function questionsDialog(frm) {
		frappe.prompt(
			[{ fieldname: "count", fieldtype: "Int", label: __("Number of questions"), default: 5 }],
			({ count }) =>
				frappe
					.xcall("vintraxo_tcd.api.ai_generate_questions", { content: frm.doc.name, count })
					.then((names) => {
						frappe.show_alert({ message: __("{0} questions saved for review", [names.length]), indicator: "green" });
						frappe.set_route("List", "TCD Question", { ai_source: frm.doc.name });
					}),
			__("Generate quiz questions"),
			__("Generate")
		);
	}

	frappe.ui.form.on("TCD Content", {
		refresh(frm) {
			if (frm.doc.ai_generated) {
				frm.dashboard.set_headline_alert(__("AI draft: check the facts before sending it for review."), "orange");
			}
			if (frm.is_new()) return;
			status().then((enabled) => {
				if (!enabled) return;
				frm.add_custom_button(
					__("Summarize"),
					() =>
						frappe
							.xcall("vintraxo_tcd.api.ai_summarize", { content: frm.doc.name }, "POST", { freeze: true })
							.then((r) => showSummary(r.summary)),
					__("AI")
				);
				if (frappe.model.can_create("TCD Question")) {
					frm.add_custom_button(__("Generate quiz questions"), () => questionsDialog(frm), __("AI"));
				}
			});
		},
	});
})();
