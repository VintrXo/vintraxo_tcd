frappe.ui.form.on("TCD Settings", {
	refresh(frm) {
		frm.add_custom_button(__("Readiness check", null, "TCD"), () =>
			frappe.xcall("vintraxo_tcd.core.ops.readiness_report", {}, "GET", { freeze: true }).then((r) => {
				const colors = { ok: "green", warn: "orange", fail: "red" };
				const esc = frappe.utils.escape_html;
				const rows = r.items
					.map(
						(i) =>
							`<tr><td><span class="indicator-pill ${colors[i.status]}">${esc(__(i.status === "ok" ? "OK" : i.status === "warn" ? "Warning" : "Problem", null, "TCD"))}</span></td>` +
							`<td>${esc(i.area)}</td><td>${esc(i.message)}${i.fix && i.status !== "ok" ? `<br><code>${esc(i.fix)}</code>` : ""}</td></tr>`
					)
					.join("");
				frappe.msgprint({
					title: __("Readiness check", null, "TCD"),
					wide: true,
					indicator: r.summary.fail ? "red" : r.summary.warn ? "orange" : "green",
					message: `<table class="table table-sm"><tbody>${rows}</tbody></table>`,
				});
			})
		);
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
