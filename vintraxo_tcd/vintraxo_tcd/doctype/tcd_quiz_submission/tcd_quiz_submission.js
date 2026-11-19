// Manual review of quiz answers (essay, file, short answer, code/SQL marked for review).
frappe.ui.form.on("TCD Quiz Submission", {
	refresh(frm) {
		if (frm.doc.status !== "Pending Review") return;
		frm.add_custom_button(__("Review Answers"), () => tcd_review_quiz(frm)).addClass("btn-primary");
	},
});

function tcd_review_quiz(frm) {
	frappe.call({ method: "vintraxo_tcd.api.get_review_items", args: { name: frm.doc.name } }).then((r) => {
		const items = r.message || [];
		const esc = frappe.utils.escape_html;
		const fields = [];
		items.forEach((it, i) => {
			let answer = it.answer;
			if (answer && typeof answer === "object") answer = (answer.code || "") + "\n---\n" + (answer.output || "");
			let html = `<div class="mb-2"><b>${i + 1}. ${esc(it.question)}</b> <span class="text-muted">(${esc(__(it.type))}, ${it.points})</span></div>`;
			if (it.type === "File" && answer) html += `<a href="${esc(String(answer))}" target="_blank" rel="noopener">${esc(__("Open file"))}</a>`;
			else html += `<pre style="white-space:pre-wrap;direction:ltr;text-align:left">${esc(String(answer || __("No answer")))}</pre>`;
			if (it.auto_hint !== null && it.auto_hint !== undefined) {
				html += `<p class="text-muted small">${esc(it.auto_hint ? __("Output matches the expected result.") : __("Output differs from the expected result."))}</p>`;
			}
			fields.push({ fieldtype: "HTML", fieldname: `info_${i}`, options: html });
			if (it.rubric && it.rubric.length) {
				it.rubric.forEach((c, j) =>
					fields.push({ fieldtype: "Float", fieldname: `r_${i}_${j}`, label: `${c.criterion} (0-${c.max_points})` })
				);
			} else {
				fields.push({ fieldtype: "Float", fieldname: `p_${i}`, label: __("Points (0-{0})", [it.points]) });
			}
			fields.push({ fieldtype: "Small Text", fieldname: `f_${i}`, label: __("Feedback") });
			fields.push({ fieldtype: "Section Break", fieldname: `s_${i}` });
		});
		const d = new frappe.ui.Dialog({
			title: __("Review Answers"),
			size: "large",
			fields,
			primary_action_label: __("Save Review"),
			primary_action(values) {
				const reviews = {};
				items.forEach((it, i) => {
					const review = { feedback: values[`f_${i}`] || "" };
					if (it.rubric && it.rubric.length) {
						review.rubric = {};
						it.rubric.forEach((c, j) => (review.rubric[c.criterion] = values[`r_${i}_${j}`] || 0));
					} else {
						review.points = values[`p_${i}`] || 0;
					}
					reviews[it.id] = review;
				});
				frappe
					.call({ method: "vintraxo_tcd.api.review_quiz_submission", args: { name: frm.doc.name, reviews }, freeze: true })
					.then(() => {
						d.hide();
						frm.reload_doc();
					});
			},
		});
		d.show();
	});
}
