// TCD Content form: visual block editor + review workflow buttons.
// All user text is set through value/textContent, never innerHTML.

const TCD_BLOCK_TYPES = {
	heading: { label: __("Heading", null, "TCD Block"), fields: [["text", "data", __("Text", null, "TCD Block")], ["level", "select", __("Level", null, "TCD Block"), ["1", "2", "3", "4"]]] },
	paragraph: { label: __("Paragraph", null, "TCD Block"), fields: [["text", "text", __("Text", null, "TCD Block")]] },
	markdown: { label: __("Markdown", null, "TCD Block"), fields: [["text", "text", __("Markdown (links: [[page-slug]])", null, "TCD Block")]] },
	code: { label: __("Code", null, "TCD Block"), fields: [["language", "data", __("Language", null, "TCD Block"), null, "ltr"], ["code", "code", __("Code", null, "TCD Block")]] },
	callout: {
		label: __("Callout", null, "TCD Block"),
		fields: [
			["variant", "select", __("Variant", null, "TCD Block"), ["info", "tip", "warning", "danger"]],
			["title", "data", __("Title", null, "TCD Block")],
			["text", "text", __("Text", null, "TCD Block")],
		],
	},
	list: { label: __("List", null, "TCD Block"), fields: [["ordered", "check", __("Numbered", null, "TCD Block")], ["items", "lines", __("Items (one per line)", null, "TCD Block")]] },
	image: {
		label: __("Image", null, "TCD Block"),
		fields: [["url", "data", __("Image URL", null, "TCD Block"), null, "ltr"], ["alt", "data", __("Alt Text", null, "TCD Block")], ["caption", "data", __("Caption", null, "TCD Block")]],
	},
	playground: {
		label: __("Playground", null, "TCD Block"),
		fields: [
			["language", "select", __("Language", null, "TCD Block"), ["python", "sql", "javascript", "html", "java", "cpp", "c", "go", "csharp", "bash"]],
			["code", "code", __("Starter Code", null, "TCD Block")],
			["expected_output", "code", __("Expected Output (optional)", null, "TCD Block")],
		],
	},
	exercise: {
		label: __("Exercise", null, "TCD Block"),
		fields: [
			["prompt", "text", __("Question", null, "TCD Block")],
			["language", "data", __("Language", null, "TCD Block"), null, "ltr"],
			["code", "code", __("Code (write ___ for each blank)", null, "TCD Block")],
			["answers", "lines", __("Answers (one per blank, in order; a | b accepts either)", null, "TCD Block")],
			["hint", "text", __("Hint (optional)", null, "TCD Block")],
		],
	},
	reference: {
		label: __("Reference Table", null, "TCD Block"),
		fields: [
			["title", "data", __("Title", null, "TCD Block")],
			["language", "data", __("Language", null, "TCD Block"), null, "ltr"],
			["entries", "lines", __("Entries (one per line: name | description | example)", null, "TCD Block")],
		],
	},
	video: {
		label: __("Video", null, "TCD Block"),
		fields: [
			["url", "upload", __("Video URL (YouTube, Vimeo or upload)", null, "TCD Block"), [".mp4", ".webm"], "ltr"],
			["title", "data", __("Title", null, "TCD Block")],
			["caption", "data", __("Caption", null, "TCD Block")],
		],
	},
	link: {
		label: __("External Link", null, "TCD Block"),
		fields: [
			["url", "data", __("Link URL (https)", null, "TCD Block"), null, "ltr"],
			["title", "data", __("Title", null, "TCD Block")],
			["description", "text", __("Description", null, "TCD Block")],
		],
	},
	file: {
		label: __("File", null, "TCD Block"),
		fields: [
			["url", "upload", __("File", null, "TCD Block"), null, "ltr"],
			["title", "data", __("Title", null, "TCD Block")],
		],
	},
};
const TCD_REQUIRED = {
	heading: "text",
	paragraph: "text",
	markdown: "text",
	code: "code",
	callout: "text",
	list: "items",
	image: "url",
	playground: "code",
	video: "url",
	link: "url",
	file: "url",
	exercise: "prompt",
	reference: "entries",
};
const TCD_LOCKED = ["Approved", "Published"];

class TCDBlockEditor {
	constructor(frm) {
		this.frm = frm;
		this.wrapper = frm.fields_dict.blocks_editor.$wrapper.get(0);
		this.load();
		this.render();
	}

	load() {
		try {
			const v = this.frm.doc.blocks;
			this.blocks = Array.isArray(v) ? v : JSON.parse(v || "[]");
			if (!Array.isArray(this.blocks)) throw new Error();
			this.error = null;
		} catch (e) {
			this.blocks = [];
			this.error = __("Blocks JSON is invalid. Fix it in the advanced section below.");
		}
	}

	get readOnly() {
		const frm = this.frm;
		return !frm.perm?.[0]?.write || TCD_LOCKED.includes(frm.doc.status) || !!this.error;
	}

	commit() {
		this.frm.__tcd_syncing = true;
		const blocks = this.blocks.map((b) => {
			const out = {};
			Object.entries(b).forEach(([k, v]) => {
				if (v !== "" && v !== null && v !== undefined && !(Array.isArray(v) && !v.length)) out[k] = v;
			});
			return out;
		});
		this.frm.set_value("blocks", JSON.stringify(blocks, null, 1)).then(() => (this.frm.__tcd_syncing = false));
	}

	el(tag, cls, text) {
		const n = document.createElement(tag);
		if (cls) n.className = cls;
		if (text !== undefined) n.textContent = text;
		return n;
	}

	render() {
		const root = this.el("div", "tcd-editor-root");
		root.dir = this.frm.doc.language === "ar" ? "rtl" : "ltr";
		if (this.error) root.append(this.el("div", "alert alert-danger", this.error));
		else if (TCD_LOCKED.includes(this.frm.doc.status))
			root.append(this.el("div", "alert alert-warning", __("This content is {0}. Move it back to Draft to edit.", [__(this.frm.doc.status, null, "TCD")])));

		if (!this.blocks.length && !this.error) root.append(this.el("p", "text-muted", __("No blocks yet. Add one below.")));
		this.blocks.forEach((block, i) => root.append(this.renderBlock(block, i)));
		if (!this.readOnly) root.append(this.renderAddBar());

		this.wrapper.replaceChildren(this.style(), root);
	}

	renderBlock(block, i) {
		const spec = TCD_BLOCK_TYPES[block.type];
		const card = this.el("div", "tcd-block-card");
		const head = this.el("div", "tcd-block-head");
		head.append(this.el("span", "indicator-pill gray", spec ? spec.label : String(block.type)), this.el("span", "text-muted small", "#" + (i + 1)));

		if (!this.readOnly) {
			const tools = this.el("span", "tcd-block-tools");
			[
				["↑", __("Move up"), () => this.move(i, -1), i === 0],
				["↓", __("Move down"), () => this.move(i, 1), i === this.blocks.length - 1],
				[__("Copy"), __("Duplicate"), () => this.duplicate(i)],
				["✕", __("Delete"), () => this.remove(i)],
			].forEach(([icon, title, fn, disabled]) => {
				const b = this.el("button", "btn btn-xs btn-default", icon);
				b.type = "button";
				b.title = title;
				b.setAttribute("aria-label", title);
				b.disabled = !!disabled;
				b.addEventListener("click", fn);
				tools.append(b);
			});
			head.append(tools);
		}
		card.append(head);

		if (!spec) {
			card.append(this.el("div", "text-danger small", __("Unknown block type. Edit it in the JSON section.")));
			return card;
		}
		spec.fields.forEach(([field, kind, label, options, dir]) => card.append(this.renderField(block, field, kind, label, options, dir)));
		if (!this.readOnly && !block[TCD_REQUIRED[block.type]]?.length) {
			card.classList.add("tcd-block-incomplete");
		}
		return card;
	}

	renderField(block, field, kind, label, options, dir) {
		const group = this.el("div", "form-group tcd-block-field");
		const id = "tcd-" + frappe.utils.get_random(8);
		const lab = this.el("label", "control-label", label);
		lab.htmlFor = id;
		let input;
		if (kind === "select") {
			input = this.el("select", "form-control input-xs");
			options.forEach((o) => {
				const opt = this.el("option", "", o);
				opt.value = o;
				input.append(opt);
			});
			input.value = String(block[field] ?? options[field === "level" ? 1 : 0]);
		} else if (kind === "check") {
			input = this.el("input");
			input.type = "checkbox";
			input.checked = !!block[field];
			group.classList.add("tcd-check");
		} else if (kind === "data" || kind === "upload") {
			input = this.el("input", "form-control input-xs");
			input.type = "text";
			input.value = block[field] ?? "";
			input.dir = dir || "auto";
		} else {
			input = this.el("textarea", "form-control" + (kind === "code" ? " tcd-code-input" : ""));
			input.value = kind === "lines" ? (block[field] || []).join("\n") : block[field] ?? "";
			input.rows = kind === "code" ? 6 : 3;
			input.dir = kind === "code" ? "ltr" : "auto";
			if (kind === "code") input.spellcheck = false;
		}
		input.id = id;
		input.disabled = this.readOnly;
		const update = () => {
			let value;
			if (kind === "check") value = input.checked;
			else if (kind === "lines") value = input.value.split("\n").map((s) => s.trim()).filter(Boolean);
			else if (field === "level") value = parseInt(input.value, 10);
			else value = input.value;
			block[field] = value;
			this.commit();
		};
		input.addEventListener(kind === "check" || kind === "select" ? "change" : "input", frappe.utils.debounce(update, 250));
		if (kind === "check") group.append(input, lab);
		else group.append(lab, input);
		if (kind === "upload" && !this.readOnly) {
			const btn = this.el("button", "btn btn-xs btn-default tcd-upload-btn", __("Upload"));
			btn.type = "button";
			btn.addEventListener("click", () => {
				new frappe.ui.FileUploader({
					allow_multiple: false,
					make_attachments_public: true,
					allow_toggle_private: false,
					allow_web_link: false,
					restrictions: options ? { allowed_file_types: options } : {},
					on_success: (file) => {
						input.value = file.file_url;
						block[field] = file.file_url;
						this.commit();
					},
				});
			});
			group.append(btn);
		}
		return group;
	}

	renderAddBar() {
		const bar = this.el("div", "tcd-add-bar");
		bar.append(this.el("span", "text-muted small", __("Add block:")));
		Object.entries(TCD_BLOCK_TYPES).forEach(([type, spec]) => {
			const b = this.el("button", "btn btn-xs btn-default", "+ " + spec.label);
			b.type = "button";
			b.addEventListener("click", () => this.add(type));
			bar.append(b);
		});
		return bar;
	}

	add(type) {
		const defaults = { heading: { level: 2 }, callout: { variant: "info" }, list: { items: [] }, playground: { language: "python" } };
		this.blocks.push({ type, ...(defaults[type] || {}) });
		this.commit();
		this.render();
		const cards = this.wrapper.querySelectorAll(".tcd-block-card");
		cards[cards.length - 1]?.querySelector("input:not([type=checkbox]), textarea")?.focus();
	}

	move(i, delta) {
		const [b] = this.blocks.splice(i, 1);
		this.blocks.splice(i + delta, 0, b);
		this.commit();
		this.render();
	}

	duplicate(i) {
		this.blocks.splice(i + 1, 0, JSON.parse(JSON.stringify(this.blocks[i])));
		this.commit();
		this.render();
	}

	remove(i) {
		frappe.confirm(__("Delete this block?"), () => {
			this.blocks.splice(i, 1);
			this.commit();
			this.render();
		});
	}

	style() {
		const s = document.createElement("style");
		s.textContent = `
			.tcd-block-card { border: 1px solid var(--border-color); border-radius: var(--border-radius-md); padding: var(--padding-sm) var(--padding-md); margin-bottom: var(--margin-sm); background: var(--card-bg); }
			.tcd-block-incomplete { border-inline-start: 3px solid var(--orange-500); }
			.tcd-block-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
			.tcd-block-tools { margin-inline-start: auto; display: flex; gap: 4px; }
			.tcd-block-field { margin-bottom: 8px; }
			.tcd-block-field.tcd-check { display: flex; align-items: center; gap: 6px; }
			.tcd-block-field.tcd-check label { margin: 0; }
			.tcd-code-input { font-family: var(--font-family-monospace, monospace); font-size: 12px; direction: ltr; text-align: left; tab-size: 4; }
			.tcd-add-bar { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; padding-top: 6px; }
		`;
		return s;
	}
}

frappe.ui.form.on("TCD Content", {
	refresh(frm) {
		frm.__tcd_editor = new TCDBlockEditor(frm);
		tcd_add_workflow_buttons(frm);
	},
	blocks(frm) {
		// typed into the raw JSON field: rebuild the visual editor
		if (!frm.__tcd_syncing && frm.__tcd_editor) {
			frm.__tcd_editor.load();
			frm.__tcd_editor.render();
		}
	},
	language(frm) {
		frm.__tcd_editor?.render();
	},
	content_type(frm) {
		frm.toggle_display("lessons_section", frm.doc.content_type === "Tutorial");
	},
});

function tcd_add_workflow_buttons(frm) {
	if (frm.doc.status === "Draft" && (frm.is_new() || frm.perm?.[0]?.write)) {
		frm.add_custom_button(__("Apply Template"), () => tcd_apply_template(frm));
	}
	if (frm.is_new()) return;
	const onload = frm.doc.__onload || {};
	const reviewer = !!onload.is_reviewer;
	const can_write = !!frm.perm?.[0]?.write;
	const group = __("Status");
	const status = frm.doc.status;

	const ACTIONS = {
		"In Review": __("Submit for Review"),
		Approved: __("Approve"),
		Published: __("Publish"),
		Archived: __("Archive"),
		Draft: __("Back to Draft"),
	};
	const go = (target) => {
		frm.add_custom_button(
			ACTIONS[target],
			() => {
				if (frm.is_dirty()) {
					frappe.msgprint(__("Save your changes first."));
					return;
				}
				frappe
					.call({
						method: "vintraxo_tcd.api.set_content_status",
						args: { name: frm.doc.name, status: target },
						freeze: true,
					})
					.then(() => frm.reload_doc());
			},
			group
		);
	};

	if (can_write) {
		if (status === "Draft") {
			go("In Review");
			if (!onload.require_approval) go("Published");
		}
		if (status === "In Review" && reviewer) go("Approved");
		if (status === "Approved" && reviewer) go("Published");
		if (status === "Published") go("Archived");
		if (status !== "Draft") go("Draft");
	}

	if (onload.portal_url) {
		frm.add_custom_button(__("View in Portal"), () => window.open(onload.portal_url, "_blank", "noopener"));
	}
	if (frm.doc.current_version) {
		frm.add_custom_button(__("Approved Version"), () => frappe.set_route("Form", "TCD Content Version", frm.doc.current_version));
	}
}

function tcd_apply_template(frm) {
	const d = new frappe.ui.Dialog({
		title: __("Apply Template"),
		fields: [
			{ fieldname: "template", fieldtype: "Link", options: "TCD Content Template", label: __("Template"), reqd: 1 },
			{ fieldname: "note", fieldtype: "HTML", options: `<p class="text-muted small">${frappe.utils.escape_html(__("The template blocks replace the current blocks."))}</p>` },
		],
		primary_action_label: __("Apply"),
		primary_action({ template }) {
			frappe.call({ method: "vintraxo_tcd.api.get_template", args: { name: template } }).then((r) => {
				const t = r.message || {};
				frm.set_value("content_type", t.content_type);
				if (t.lesson_type) frm.set_value("lesson_type", t.lesson_type);
				frm.set_value("blocks", t.blocks || "[]").then(() => {
					frm.__tcd_editor?.load();
					frm.__tcd_editor?.render();
				});
				d.hide();
			});
		},
	});
	d.show();
}
