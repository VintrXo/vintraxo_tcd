// VintraXo TCD authoring studio (Phase 18): block editor for pages and the course outline editor.
// All user text is set through value / textContent, never innerHTML. The server validates every save.
(function () {
	"use strict";

	const API = "/api/method/vintraxo_tcd.api.";

	function json(id, fallback) {
		try {
			return JSON.parse(document.getElementById(id).textContent);
		} catch (_) {
			return fallback;
		}
	}

	function el(tag, attrs, text) {
		const node = document.createElement(tag);
		Object.entries(attrs || {}).forEach(([k, v]) => {
			if (v === false || v === null || v === undefined) return;
			node.setAttribute(k, v === true ? "" : v);
		});
		if (text !== undefined && text !== null) node.textContent = text;
		return node;
	}

	function serverMessage(data) {
		try {
			const msgs = JSON.parse(data._server_messages || "[]").map((m) => JSON.parse(m).message);
			if (msgs.length) return new DOMParser().parseFromString(msgs.join(" "), "text/html").body.textContent;
		} catch (_) {
			/* ignore */
		}
		return data.exception || data.exc_type || "";
	}

	async function call(method, args, post) {
		const opts = { method: post ? "POST" : "GET", credentials: "same-origin", headers: { Accept: "application/json" } };
		let url = API + method;
		if (post) {
			opts.headers["Content-Type"] = "application/json";
			opts.headers["X-Frappe-CSRF-Token"] = (window.frappe && window.frappe.csrf_token) || "";
			opts.body = JSON.stringify(args || {});
		} else if (args) {
			url += "?" + new URLSearchParams(args);
		}
		const res = await fetch(url, opts);
		const data = await res.json().catch(() => ({}));
		if (!res.ok) throw new Error(serverMessage(data) || res.statusText);
		return data.message;
	}

	async function uploadPublic(file) {
		const form = new FormData();
		form.append("file", file, file.name);
		form.append("is_private", "0");
		const res = await fetch("/api/method/upload_file", {
			method: "POST",
			credentials: "same-origin",
			headers: { Accept: "application/json", "X-Frappe-CSRF-Token": (window.frappe && window.frappe.csrf_token) || "" },
			body: form,
		});
		const data = await res.json().catch(() => ({}));
		if (!res.ok) throw new Error(serverMessage(data) || res.statusText);
		return data.message.file_url;
	}

	function status(box, text, isError) {
		if (!box) return;
		box.textContent = text || "";
		box.hidden = !text;
		box.classList.toggle("tcd-error", !!isError);
	}

	// ------------------------------------------------------------ block editor

	class BlockEditor {
		constructor(root, spec, blocks, t, locked) {
			this.root = root;
			this.spec = spec;
			this.blocks = Array.isArray(blocks) ? blocks : [];
			this.t = t;
			this.locked = locked;
			this.onChange = () => {};
			this.render();
		}

		render() {
			this.root.replaceChildren();
			if (!this.blocks.length) this.root.append(el("p", { class: "tcd-muted" }, this.t.empty || "No blocks yet."));
			this.blocks.forEach((b, i) => this.root.append(this.card(b, i)));
			if (!this.locked) this.root.append(this.addBar());
		}

		changed() {
			this.onChange();
		}

		addBar() {
			const bar = el("div", { class: "tcd-studio-addbar", role: "group", "aria-label": this.t.add_block || "Add block" });
			bar.append(el("span", { class: "tcd-muted tcd-small" }, (this.t.add_block || "Add block") + ":"));
			Object.entries(this.spec).forEach(([type, s]) => {
				const b = el("button", { type: "button", class: "btn btn-default btn-xs" }, "+ " + s.label);
				b.addEventListener("click", () => {
					const defaults = { heading: { level: 2 }, callout: { variant: "info" }, list: { items: [] }, playground: { language: "python" } };
					this.blocks.push({ type, ...(defaults[type] || {}) });
					this.render();
					this.changed();
					const cards = this.root.querySelectorAll(".tcd-studio-block");
					cards[cards.length - 1]?.querySelector("input:not([type=checkbox]),textarea,select")?.focus();
				});
				bar.append(b);
			});
			return bar;
		}

		card(block, i) {
			const s = this.spec[block.type];
			const card = el("section", { class: "tcd-studio-block", "aria-label": (s ? s.label : block.type) + " #" + (i + 1) });
			const head = el("div", { class: "tcd-studio-block-head" });
			head.append(el("span", { class: "tcd-badge" }, (s ? s.label : block.type) + " · " + (i + 1)));
			if (!this.locked) {
				const tools = el("span", { class: "tcd-studio-tools" });
				const tool = (label, text, fn, disabled) => {
					const b = el("button", { type: "button", class: "btn btn-default btn-xs", "aria-label": label, title: label, disabled: !!disabled }, text);
					b.addEventListener("click", fn);
					tools.append(b);
				};
				tool(this.t.move_up || "Move up", "↑", () => this.move(i, -1), i === 0);
				tool(this.t.move_down || "Move down", "↓", () => this.move(i, 1), i === this.blocks.length - 1);
				tool(this.t.duplicate || "Duplicate", this.t.duplicate || "Duplicate", () => {
					this.blocks.splice(i + 1, 0, JSON.parse(JSON.stringify(block)));
					this.render();
					this.changed();
				});
				tool(this.t.remove || "Remove", "✕", () => {
					this.blocks.splice(i, 1);
					this.render();
					this.changed();
				});
				head.append(tools);
			}
			card.append(head);
			if (!s) {
				card.append(el("p", { class: "tcd-error tcd-small" }, block.type));
				return card;
			}
			s.fields.forEach(([field, kind, label, options, dir]) => card.append(this.field(block, field, kind, label, options, dir)));
			return card;
		}

		move(i, delta) {
			const [b] = this.blocks.splice(i, 1);
			this.blocks.splice(i + delta, 0, b);
			this.render();
			this.changed();
		}

		field(block, field, kind, label, options, dir) {
			const id = "tcd-f-" + Math.random().toString(36).slice(2, 10);
			const wrap = el("div", { class: "tcd-studio-field" });
			const lab = el("label", { for: id }, label);
			let input;
			if (kind === "select") {
				input = el("select", { class: "form-control" });
				(options || []).forEach((o) => input.append(el("option", { value: o }, o)));
				input.value = String(block[field] ?? (field === "level" ? "2" : (options || [""])[0]));
			} else if (kind === "check") {
				input = el("input", { type: "checkbox" });
				input.checked = !!block[field];
				wrap.classList.add("tcd-studio-check");
			} else if (kind === "data" || kind === "upload") {
				input = el("input", { type: "text", class: "form-control", dir: dir || "auto" });
				input.value = block[field] ?? "";
			} else {
				input = el("textarea", { class: "form-control" + (kind === "code" ? " tcd-studio-code" : ""), rows: kind === "code" ? 6 : 3, dir: kind === "code" ? "ltr" : "auto", spellcheck: kind === "code" ? "false" : "true" });
				input.value = kind === "lines" ? (block[field] || []).join("\n") : block[field] ?? "";
			}
			input.id = id;
			input.disabled = this.locked;
			const update = () => {
				let value;
				if (kind === "check") value = input.checked;
				else if (kind === "lines") value = input.value.split("\n").map((x) => x.trim()).filter(Boolean);
				else if (field === "level") value = parseInt(input.value, 10);
				else value = input.value;
				block[field] = value;
				this.changed();
			};
			input.addEventListener("input", update);
			input.addEventListener("change", update);
			if (kind === "check") wrap.append(input, lab);
			else wrap.append(lab, input);
			if (kind === "upload" && !this.locked) {
				const fileInput = el("input", { type: "file", class: "tcd-studio-file", accept: options || null, "aria-label": (this.t.upload || "Upload") + " " + label });
				const note = el("span", { class: "tcd-muted tcd-small", role: "status" });
				fileInput.addEventListener("change", async () => {
					const file = fileInput.files[0];
					if (!file) return;
					note.textContent = this.t.uploading || "Uploading...";
					try {
						input.value = await uploadPublic(file);
						update();
						note.textContent = "";
					} catch (e) {
						note.textContent = e.message;
					}
				});
				wrap.append(fileInput, note);
			}
			return wrap;
		}
	}

	// ------------------------------------------------------------ page editor

	function initPage() {
		const form = document.querySelector(".tcd-studio-page-form");
		if (!form) return;
		const t = json("tcd-studio-labels", {});
		const spec = json("tcd-studio-spec", {});
		const doc = json("tcd-studio-doc", {});
		const msg = form.querySelector(".tcd-studio-status");
		const locked = form.dataset.locked === "1";
		const editor = new BlockEditor(form.querySelector(".tcd-studio-blocks"), spec, doc.blocks || [], t, locked);
		let dirty = false;
		const markDirty = () => {
			dirty = true;
			status(msg, t.unsaved || "Unsaved changes.");
		};
		editor.onChange = markDirty;
		form.querySelectorAll("[name]").forEach((f) => f.addEventListener("input", markDirty));
		window.addEventListener("beforeunload", (e) => {
			if (dirty) e.preventDefault();
		});

		const save = async () => {
			const data = { name: doc.name || null, blocks: editor.blocks };
			["title", "space", "content_type", "language", "visibility", "summary"].forEach((f) => {
				if (form.elements[f]) data[f] = form.elements[f].value;
			});
			status(msg, t.saving || "Saving...");
			const r = await call("studio_save_page", { data: JSON.stringify(data) }, true);
			dirty = false;
			if (!doc.name) {
				window.location.replace("/learn/studio/page?name=" + encodeURIComponent(r.name));
				return r;
			}
			status(msg, t.saved || "Saved.");
			return r;
		};
		form.addEventListener("submit", async (e) => {
			e.preventDefault();
			try {
				await save();
			} catch (err) {
				status(msg, err.message, true);
			}
		});
		form.querySelectorAll("[data-status]").forEach((btn) =>
			btn.addEventListener("click", async () => {
				btn.disabled = true;
				try {
					if (dirty && !locked) await save();
					await call("set_content_status", { name: doc.name, status: btn.dataset.status }, true);
					dirty = false;
					window.location.reload();
				} catch (err) {
					status(msg, err.message, true);
					btn.disabled = false;
				}
			})
		);
	}

	// ------------------------------------------------------------ course editor

	function initCourse() {
		const form = document.querySelector(".tcd-studio-course-form");
		if (!form) return;
		const t = json("tcd-studio-labels", {});
		const data = json("tcd-studio-course", { doc: {}, chapters: [] });
		const doc = data.doc;
		const chapters = data.chapters || [];
		const msg = form.querySelector(".tcd-studio-status");
		const root = form.querySelector(".tcd-studio-chapters");
		const locked = form.dataset.locked === "1";
		let dirty = false;
		const markDirty = () => {
			dirty = true;
			status(msg, t.unsaved || "Unsaved changes.");
		};
		form.querySelectorAll("[name]").forEach((f) => f.addEventListener("input", markDirty));
		window.addEventListener("beforeunload", (e) => {
			if (dirty) e.preventDefault();
		});

		const render = () => {
			if (!root) return;
			root.replaceChildren();
			chapters.forEach((ch, ci) => root.append(chapterCard(ch, ci)));
			if (!locked && doc.name) {
				const add = el("button", { type: "button", class: "btn btn-default btn-sm" }, "+ " + (t.add_chapter || "Add chapter"));
				add.addEventListener("click", () => {
					chapters.push({ title: "", items: [] });
					render();
					markDirty();
					root.querySelectorAll(".tcd-studio-chapter-title")[chapters.length - 1]?.focus();
				});
				root.append(add);
			}
		};

		const chapterCard = (ch, ci) => {
			const card = el("section", { class: "tcd-studio-block tcd-studio-chapter" });
			const head = el("div", { class: "tcd-studio-block-head" });
			const title = el("input", { type: "text", class: "form-control tcd-studio-chapter-title", "aria-label": t.chapter_title || "Chapter title", placeholder: t.chapter_title || "Chapter title", dir: "auto" });
			title.value = ch.title || "";
			title.disabled = locked;
			title.addEventListener("input", () => {
				ch.title = title.value;
				markDirty();
			});
			head.append(title);
			if (!locked) {
				const tools = el("span", { class: "tcd-studio-tools" });
				const tool = (label, text, fn, disabled) => {
					const b = el("button", { type: "button", class: "btn btn-default btn-xs", "aria-label": label, title: label, disabled: !!disabled }, text);
					b.addEventListener("click", fn);
					tools.append(b);
				};
				tool(t.move_up || "Move up", "↑", () => swap(chapters, ci, ci - 1), ci === 0);
				tool(t.move_down || "Move down", "↓", () => swap(chapters, ci, ci + 1), ci === chapters.length - 1);
				tool(t.remove || "Remove", "✕", () => {
					chapters.splice(ci, 1);
					render();
					markDirty();
				});
				head.append(tools);
			}
			card.append(head);
			const list = el("ol", { class: "tcd-studio-items" });
			(ch.items || []).forEach((it, ii) => {
				const li = el("li", { class: "tcd-studio-item" });
				li.append(el("span", { class: "tcd-studio-item-title" }, it.title || it.content));
				const opt = el("label", { class: "tcd-small" });
				const box = el("input", { type: "checkbox", disabled: locked });
				box.checked = !!it.is_optional;
				box.addEventListener("change", () => {
					it.is_optional = box.checked ? 1 : 0;
					markDirty();
				});
				opt.append(box, document.createTextNode(" " + (t.optional || "Optional")));
				li.append(opt);
				if (!locked) {
					const tools = el("span", { class: "tcd-studio-tools" });
					const tool = (label, text, fn, disabled) => {
						const b = el("button", { type: "button", class: "btn btn-default btn-xs", "aria-label": label, title: label, disabled: !!disabled }, text);
						b.addEventListener("click", fn);
						tools.append(b);
					};
					tool(t.move_up || "Move up", "↑", () => swap(ch.items, ii, ii - 1), ii === 0);
					tool(t.move_down || "Move down", "↓", () => swap(ch.items, ii, ii + 1), ii === ch.items.length - 1);
					tool(t.remove || "Remove", "✕", () => {
						ch.items.splice(ii, 1);
						render();
						markDirty();
					});
					li.append(tools);
				}
				list.append(li);
			});
			card.append(list);
			if (!locked) card.append(pagePicker(ch));
			return card;
		};

		const swap = (arr, a, b) => {
			[arr[a], arr[b]] = [arr[b], arr[a]];
			render();
			markDirty();
		};

		const pagePicker = (ch) => {
			const wrap = el("div", { class: "tcd-studio-picker" });
			const input = el("input", { type: "search", class: "form-control", placeholder: t.search_pages || "Search pages", "aria-label": t.add_page || "Add a page" });
			const results = el("ul", { class: "tcd-studio-results", role: "listbox" });
			let timer;
			input.addEventListener("input", () => {
				clearTimeout(timer);
				timer = setTimeout(async () => {
					results.replaceChildren();
					if (input.value.trim().length < 2) return;
					try {
						const pages = await call("studio_find_pages", { query: input.value, space: doc.space || "" });
						if (!pages.length) results.append(el("li", { class: "tcd-muted tcd-small" }, t.no_results || "Nothing found."));
						pages.forEach((p) => {
							const li = el("li");
							const b = el("button", { type: "button", class: "btn btn-default btn-xs" }, "+ " + p.title);
							b.addEventListener("click", () => {
								ch.items = ch.items || [];
								ch.items.push({ content: p.name, title: p.title, is_optional: 0 });
								render();
								markDirty();
							});
							li.append(b, el("span", { class: "tcd-muted tcd-small" }, " " + p.status));
							results.append(li);
						});
					} catch (e) {
						results.append(el("li", { class: "tcd-error tcd-small" }, e.message));
					}
				}, 250);
			});
			wrap.append(el("label", { class: "tcd-small" }, t.add_page || "Add a page"), input, results);
			return wrap;
		};

		const save = async () => {
			const payload = { name: doc.name || null };
			["title", "space", "language", "visibility", "summary", "completion_rule", "minimum_score", "access", "intro_video", "cover_image", "evaluation_minutes"].forEach((f) => {
				if (form.elements[f]) payload[f] = form.elements[f].value;
			});
			["self_enrollment", "issue_certificate", "requires_evaluation"].forEach((f) => {
				if (form.elements[f]) payload[f] = form.elements[f].checked ? 1 : 0;
			});
			if (doc.name && !locked) payload.chapters = chapters.map((c) => ({ name: c.name || null, title: c.title, items: (c.items || []).map((i) => ({ content: i.content, is_optional: i.is_optional ? 1 : 0 })) }));
			status(msg, t.saving || "Saving...");
			const r = await call("studio_save_course", { data: JSON.stringify(payload) }, true);
			dirty = false;
			if (!doc.name) {
				window.location.replace("/learn/studio/course?name=" + encodeURIComponent(r.name));
				return r;
			}
			window.location.reload();
			return r;
		};
		form.addEventListener("submit", async (e) => {
			e.preventDefault();
			try {
				await save();
			} catch (err) {
				status(msg, err.message, true);
			}
		});
		form.querySelectorAll("[data-course-status]").forEach((btn) =>
			btn.addEventListener("click", async () => {
				btn.disabled = true;
				try {
					await call("studio_course_status", { name: doc.name, status: btn.dataset.courseStatus }, true);
					dirty = false;
					window.location.reload();
				} catch (err) {
					status(msg, err.message, true);
					btn.disabled = false;
				}
			})
		);
		render();
	}

	function init() {
		initPage();
		initCourse();
	}

	if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
	else init();
})();
