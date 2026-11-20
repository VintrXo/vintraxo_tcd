// VintraXo TCD: small Markdown toolbar + preview for text areas marked data-md (Phase 25).
// The preview HTML comes from the server's sanitizing Markdown renderer (the one pages use).
(function () {
	"use strict";

	function labels() {
		try {
			return JSON.parse(document.getElementById("tcd-labels").textContent);
		} catch (_) {
			return {};
		}
	}

	const ACTIONS = [
		["bold", "B", (s) => `**${s || "text"}**`],
		["italic", "I", (s) => `_${s || "text"}_`],
		["heading", "H", (s) => `\n## ${s || "Heading"}\n`],
		["list", "•", (s) => (s || "item").split("\n").map((l) => `- ${l}`).join("\n")],
		["link", "🔗", (s) => `[${s || "text"}](https://)`],
		["code", "</>", (s) => (s && s.includes("\n") ? "\n```\n" + s + "\n```\n" : "`" + (s || "code") + "`")],
	];

	function wrap(area, fn) {
		const { selectionStart: a, selectionEnd: b, value } = area;
		const out = fn(value.slice(a, b));
		area.value = value.slice(0, a) + out + value.slice(b);
		area.selectionStart = a;
		area.selectionEnd = a + out.length;
		area.focus();
		area.dispatchEvent(new Event("input", { bubbles: true }));
	}

	async function preview(text, space) {
		const res = await fetch("/api/method/vintraxo_tcd.api.preview_markdown", {
			method: "POST",
			credentials: "same-origin",
			headers: { "Content-Type": "application/json", Accept: "application/json", "X-Frappe-CSRF-Token": (window.frappe && window.frappe.csrf_token) || "" },
			body: JSON.stringify({ text, space: space || null }),
		});
		const data = await res.json().catch(() => ({}));
		if (!res.ok) throw new Error(res.statusText);
		return data.message || "";
	}

	function enhance(area) {
		if (!area || area.dataset.mdReady) return;
		area.dataset.mdReady = "1";
		const t = labels();
		const bar = document.createElement("div");
		bar.className = "tcd-md-bar";
		bar.setAttribute("role", "toolbar");
		ACTIONS.forEach(([key, text, fn]) => {
			const b = document.createElement("button");
			b.type = "button";
			b.className = "btn btn-default btn-xs";
			b.textContent = text;
			b.title = t["md_" + key] || key;
			b.setAttribute("aria-label", b.title);
			b.addEventListener("click", () => wrap(area, fn));
			bar.append(b);
		});
		const toggle = document.createElement("button");
		toggle.type = "button";
		toggle.className = "btn btn-default btn-xs tcd-md-preview-btn";
		toggle.textContent = t.preview || "Preview";
		toggle.setAttribute("aria-pressed", "false");
		const out = document.createElement("div");
		out.className = "tcd-md-preview tcd-markdown";
		out.hidden = true;
		toggle.addEventListener("click", async () => {
			const on = out.hidden;
			toggle.setAttribute("aria-pressed", on ? "true" : "false");
			if (!on) {
				out.hidden = true;
				area.hidden = false;
				return;
			}
			try {
				out.innerHTML = await preview(area.value, area.dataset.space);
			} catch (e) {
				out.textContent = e.message;
			}
			out.hidden = false;
			area.hidden = true;
		});
		bar.append(toggle);
		area.before(bar);
		area.after(out);
	}

	function init() {
		document.querySelectorAll("textarea[data-md]").forEach(enhance);
	}

	window.tcdMarkdown = { enhance };
	if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
	else init();
})();
