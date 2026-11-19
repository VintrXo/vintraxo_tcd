frappe.ui.form.on("TCD Change Request", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Show Changes"), () =>
			frappe.xcall("vintraxo_tcd.api.change_request_diff", { name: frm.doc.name }).then((r) => {
				const esc = frappe.utils.escape_html;
				const rows = r.diff.map((line) => {
					const color = line.startsWith("+") ? "var(--green-700,#15803d)" : line.startsWith("-") ? "var(--red-700,#b91c1c)" : "inherit";
					return `<div style="color:${color}">${esc(line) || "&nbsp;"}</div>`;
				});
				const d = new frappe.ui.Dialog({ title: __("Suggested changes"), size: "extra-large" });
				d.$body.html(
					(r.conflict ? `<p class="text-danger">${esc(__("The page changed after this suggestion."))}</p>` : "") +
						`<div style="white-space:pre-wrap;font-family:monospace;font-size:12px;unicode-bidi:plaintext">${rows.join("")}</div>`
				);
				d.show();
			})
		);
		if (frm.doc.status !== "Open" || !frappe.user.has_role(["TCD Content Reviewer", "TCD Administrator", "System Manager"])) return;
		const decide = (method, label) =>
			frappe.prompt([{ fieldname: "comment", fieldtype: "Small Text", label: __("Comment") }], ({ comment }) =>
				frappe.xcall(`vintraxo_tcd.api.${method}`, { name: frm.doc.name, comment: comment || "" }).then(() => frm.reload_doc()), label);
		frm.add_custom_button(__("Accept"), () => decide("accept_change_request", __("Accept")), __("Decision"));
		frm.add_custom_button(__("Reject"), () => decide("reject_change_request", __("Reject")), __("Decision"));
	},
});
