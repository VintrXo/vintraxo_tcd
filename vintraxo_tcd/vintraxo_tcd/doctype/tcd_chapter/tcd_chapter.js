frappe.ui.form.on("TCD Chapter", {
	refresh(frm) {
		frm.set_query("content", "items", () => ({
			filters: { space: frm.doc.space, content_type: ["in", ["Lesson", "Article", "Reference"]] },
		}));
	},
});
