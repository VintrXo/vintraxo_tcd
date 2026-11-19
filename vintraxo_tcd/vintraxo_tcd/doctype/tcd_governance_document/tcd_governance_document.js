// Lifecycle buttons for policies, SOPs and documents (rules enforced on the server).
frappe.ui.form.on("TCD Governance Document", {
	refresh(frm) {
		if (frm.is_new()) return;
		const can_write = !!frm.perm?.[0]?.write;
		const is_approver = frm.doc.status === "Approval" && frm.doc.approver === frappe.session.user;
		if (!can_write && !is_approver) return;
		const next = {
			Draft: [["Review", __("Send for Review")]],
			Review: [["Approval", __("Send for Approval")], ["Draft", __("Back to Draft")]],
			Approval: [["Active", __("Activate")], ["Draft", __("Back to Draft")]],
			Active: [["Revision", __("Start Revision")], ["Archived", __("Archive")]],
			Revision: [["Review", __("Send for Review")], ["Archived", __("Archive")]],
			Archived: [["Draft", __("Back to Draft")]],
		}[frm.doc.status] || [];
		next.forEach(([status, label]) =>
			frm.add_custom_button(
				label,
				() => {
					if (frm.is_dirty()) return frappe.msgprint(__("Save your changes first."));
					frappe
						.call({ method: "vintraxo_tcd.api.set_governance_status", args: { code: frm.doc.name, status }, freeze: true })
						.then(() => frm.reload_doc());
				},
				__("Status")
			)
		);
		if (frm.doc.version) {
			frm.add_custom_button(__("View in Portal"), () => window.open(`/learn/policies/${encodeURIComponent(frm.doc.name)}`, "_blank", "noopener"));
			frm.add_custom_button(__("Acknowledgment Status"), () => frappe.set_route("query-report", "TCD Acknowledgment Status", { document: frm.doc.name }));
		}
	},
});
