frappe.ui.form.on("TCD Certificate", {
	refresh(frm) {
		if (frm.is_new()) return;
		frm.add_custom_button(__("Verification Page"), () => window.open(`/verify/${encodeURIComponent(frm.doc.verification_code)}`, "_blank", "noopener"));
		if (["Active", "Expired"].includes(frm.doc.status)) {
			frm.add_custom_button(__("Renew"), () =>
				frappe.confirm(__("Issue a new certificate with a new expiry date?"), () =>
					frappe.call({ method: "vintraxo_tcd.api.renew_certificate", args: { name: frm.doc.name }, freeze: true }).then((r) =>
						frappe.set_route("Form", "TCD Certificate", r.message.name)
					)
				)
			);
		}
		if (frm.doc.status === "Active" && frappe.user.has_role(["System Manager", "TCD Administrator"])) {
			frm.add_custom_button(__("Revoke"), () =>
				frappe.prompt({ fieldname: "reason", fieldtype: "Small Text", label: __("Reason"), reqd: 1 }, ({ reason }) =>
					frappe.call({ method: "vintraxo_tcd.api.revoke_certificate", args: { name: frm.doc.name, reason } }).then(() => frm.reload_doc())
				)
			);
		}
	},
});
