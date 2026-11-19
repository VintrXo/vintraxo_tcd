// Compare an approved version with the current content, or restore it as a new draft.
frappe.ui.form.on("TCD Content Version", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Compare with Current"), () => {
			frappe
				.call({ method: "vintraxo_tcd.api.compare_versions", args: { old: frm.doc.name, new: frm.doc.content } })
				.then((r) => tcd_show_diff(r.message));
		});
		if (frappe.model.can_write("TCD Content")) {
			frm.add_custom_button(__("Restore as Draft"), () => {
				frappe.confirm(__("Replace the current content with this version and move it to Draft?"), () =>
					frappe
						.call({ method: "vintraxo_tcd.api.restore_version", args: { name: frm.doc.name }, freeze: true })
						.then((r) => frappe.set_route("Form", "TCD Content", r.message.name))
				);
			});
		}
	},
});

function tcd_show_diff(res) {
	const esc = frappe.utils.escape_html;
	const rows = (res.diff || []).map((line) => {
		const cls = line.startsWith("+") ? "tcd-add" : line.startsWith("-") ? "tcd-del" : line.startsWith("@@") ? "tcd-hunk" : "";
		return `<div class="${cls}">${esc(line) || "&nbsp;"}</div>`;
	});
	const body = rows.length ? rows.join("") : `<p class="text-muted">${esc(__("No differences."))}</p>`;
	const d = new frappe.ui.Dialog({ title: `${esc(res.from)} → ${esc(res.to)}`, size: "extra-large" });
	d.$body.html(
		`<style>.tcd-diff{direction:ltr;text-align:left;font-family:var(--font-family-monospace,monospace);font-size:12px;white-space:pre-wrap;unicode-bidi:plaintext}
		.tcd-diff .tcd-add{background:var(--green-50,#ecfdf3);color:var(--green-700,#15803d)}
		.tcd-diff .tcd-del{background:var(--red-50,#fef2f2);color:var(--red-700,#b91c1c)}
		.tcd-diff .tcd-hunk{color:var(--text-muted)}</style>
		<p class="text-muted">+${res.added} / -${res.removed}</p><div class="tcd-diff">${body}</div>`
	);
	d.show();
}
