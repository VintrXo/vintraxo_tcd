// VintraXo TCD: syntax highlighting, copy buttons and a highlighted code editor (Phase 17).
// No third-party code. Every token is escaped before it is placed in the page.
(function () {
	"use strict";

	const KEYWORDS = {
		python:
			"and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield match case",
		javascript:
			"async await break case catch class const continue debugger default delete do else export extends finally for function if import in instanceof let new of return static super switch this throw try typeof var void while with yield",
		sql: "select from where and or not insert into values update set delete create table drop alter add primary key foreign references join inner left right full outer on group by order having limit offset as distinct union all exists in is null like between case when then else end asc desc index view count sum avg min max default unique check",
		clike:
			"abstract auto bool boolean break byte case catch char class const continue default delete do double else enum extends final finally float for func go goto if implements import int interface long namespace new package private protected public return short signed sizeof static struct super switch this throw throws try typedef unsigned using var virtual void volatile while string fmt echo fi then done esac in function local",
	};
	const LITERALS = "True False None true false null undefined NaN Infinity nil";
	const BUILTINS =
		"print len range int str float list dict set tuple type input open sum min max abs sorted enumerate zip map filter isinstance console document window Math JSON Object Array String Number Promise";

	const words = (s) => new Set(s.split(/\s+/));
	const LITERAL = words(LITERALS);
	const BUILTIN = words(BUILTINS);
	const KW = Object.fromEntries(Object.entries(KEYWORDS).map(([k, v]) => [k, words(v)]));

	function esc(text) {
		return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
	}
	function span(kind, text) {
		return '<span class="tcd-tok-' + kind + '">' + esc(text) + "</span>";
	}

	function family(lang) {
		lang = (lang || "").toLowerCase();
		if (["python", "py"].includes(lang)) return "python";
		if (["javascript", "js", "typescript", "ts", "json"].includes(lang)) return "javascript";
		if (["sql", "mysql", "postgresql", "sqlite"].includes(lang)) return "sql";
		if (["html", "xml", "svg"].includes(lang)) return "html";
		if (["java", "c", "cpp", "c++", "go", "csharp", "cs", "bash", "sh", "shell", "php", "kotlin", "swift"].includes(lang)) return "clike";
		return "";
	}

	const RULES = {
		python: [
			["comment", /#[^\n]*/y],
			["string", /[rRbBfFuU]{0,2}("""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?)/y],
			["meta", /@[A-Za-z_][\w.]*/y],
		],
		javascript: [
			["comment", /\/\/[^\n]*|\/\*[\s\S]*?(?:\*\/|$)/y],
			["string", /`(?:\\.|[^`\\])*`?|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?/y],
		],
		sql: [
			["comment", /--[^\n]*|\/\*[\s\S]*?(?:\*\/|$)/y],
			["string", /'(?:''|[^'])*'?|"(?:[^"])*"?/y],
		],
		clike: [
			["comment", /\/\/[^\n]*|\/\*[\s\S]*?(?:\*\/|$)|#(?:include|define|!)[^\n]*/y],
			["string", /"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?|`[^`]*`?/y],
		],
	};
	const NUMBER = /\b(?:0x[\da-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\b/y;
	const IDENT = /[A-Za-z_$][\w$]*/y;

	function highlightCode(code, lang) {
		const fam = family(lang);
		if (fam === "html") return highlightHTML(code);
		if (!fam) return esc(code);
		const rules = RULES[fam];
		const kw = KW[fam];
		let out = "";
		let i = 0;
		let plain = "";
		const flush = () => {
			if (plain) out += esc(plain);
			plain = "";
		};
		while (i < code.length) {
			let matched = false;
			for (const [kind, re] of rules) {
				re.lastIndex = i;
				const m = re.exec(code);
				if (m && m[0]) {
					flush();
					out += span(kind, m[0]);
					i += m[0].length;
					matched = true;
					break;
				}
			}
			if (matched) continue;
			NUMBER.lastIndex = i;
			let m = NUMBER.exec(code);
			if (m && m[0] && !/[\w$]/.test(code[i - 1] || "")) {
				flush();
				out += span("number", m[0]);
				i += m[0].length;
				continue;
			}
			IDENT.lastIndex = i;
			m = IDENT.exec(code);
			if (m && !/[\w$]/.test(code[i - 1] || "")) {
				const w = m[0];
				const key = fam === "sql" ? w.toLowerCase() : w;
				flush();
				if (kw.has(key)) out += span("keyword", w);
				else if (LITERAL.has(w)) out += span("literal", w);
				else if (code[i + w.length] === "(" || BUILTIN.has(w)) out += span("func", w);
				else out += esc(w);
				i += w.length;
				continue;
			}
			plain += code[i];
			i += 1;
		}
		flush();
		return out;
	}

	function highlightHTML(code) {
		let out = "";
		let i = 0;
		const TAG = /<!--[\s\S]*?(?:-->|$)|<\/?[A-Za-z][\w:-]*(?:\s+[^\s=>\/]+(?:\s*=\s*(?:"[^"]*"?|'[^']*'?|[^\s>]+))?)*\s*\/?>?/y;
		while (i < code.length) {
			TAG.lastIndex = i;
			const m = TAG.exec(code);
			if (m && m[0] && code[i] === "<") {
				const t = m[0];
				if (t.startsWith("<!--")) out += span("comment", t);
				else {
					const name = /^<\/?[\w:-]*/.exec(t)[0];
					let rest = t.slice(name.length);
					const close = /\/?>$/.exec(rest);
					const end = close ? close[0] : "";
					rest = rest.slice(0, rest.length - end.length);
					out += span("keyword", name);
					out += rest.replace(/([^\s=]+)(\s*=\s*)?("[^"]*"?|'[^']*'?|[^\s>]+)?|(\s+)/g, (all, attr, eq, val, ws) => {
						if (ws) return ws;
						return span("attr", attr) + (eq ? esc(eq) : "") + (val ? span("string", val) : "");
					});
					out += esc(end);
				}
				i += t.length;
				continue;
			}
			const next = code.indexOf("<", i + 1);
			const stop = next === -1 ? code.length : next;
			out += esc(code.slice(i, stop));
			i = stop;
		}
		return out;
	}

	function labels() {
		try {
			return JSON.parse(document.getElementById("tcd-labels").textContent);
		} catch (_) {
			return {};
		}
	}

	function langOf(codeEl, pre) {
		const cls = [...(codeEl ? codeEl.classList : []), ...pre.classList].find((c) => c.startsWith("language-"));
		return cls ? cls.slice(9) : pre.closest("[data-language]")?.dataset.language || "";
	}

	function copyText(text) {
		if (navigator.clipboard && window.isSecureContext) {
			return navigator.clipboard.writeText(text).catch(() => copyFallback(text));
		}
		return copyFallback(text);
	}

	function copyFallback(text) {
		const area = document.createElement("textarea");
		area.value = text;
		area.setAttribute("readonly", "");
		area.style.position = "fixed";
		area.style.opacity = "0";
		document.body.append(area);
		area.select();
		let ok = false;
		try {
			ok = document.execCommand("copy");
		} finally {
			area.remove();
		}
		return ok ? Promise.resolve() : Promise.reject(new Error("copy"));
	}

	function decorateBlocks(t) {
		document.querySelectorAll(".tcd-page pre.tcd-code, .tcd-page .tcd-markdown pre").forEach((pre) => {
			if (pre.dataset.tcdHl) return;
			pre.dataset.tcdHl = "1";
			const codeEl = pre.querySelector("code") || pre;
			codeEl.classList.add("nohighlight"); // keep the site-wide highlighter away
			pre.classList.add("nohighlight");
			const exercise = pre.classList.contains("tcd-exercise-code");
			if (!exercise) {
				const text = codeEl.textContent;
				codeEl.innerHTML = highlightCode(text, langOf(codeEl, pre));
				const btn = document.createElement("button");
				btn.type = "button";
				btn.className = "tcd-copy-btn";
				btn.textContent = t.copy || "Copy";
				btn.addEventListener("click", () => {
					copyText(text)
						.then(() => {
							btn.textContent = t.copied || "Copied";
							setTimeout(() => (btn.textContent = t.copy || "Copy"), 1500);
						})
						.catch(() => {
							// the browser refused: select the code so the learner can copy it by hand
							const range = document.createRange();
							range.selectNodeContents(codeEl);
							const sel = window.getSelection();
							sel.removeAllRanges();
							sel.addRange(range);
						});
				});
				const wrap = document.createElement("div");
				wrap.className = "tcd-code-wrap";
				pre.replaceWith(wrap);
				wrap.append(pre, btn);
			}
		});
	}

	function decorateInline() {
		document.querySelectorAll(".tcd-reference").forEach((box) => {
			const lang = box.dataset.language || "";
			box.querySelectorAll("code.tcd-reference-example").forEach((c) => {
				if (c.dataset.tcdHl) return;
				c.dataset.tcdHl = "1";
				c.innerHTML = highlightCode(c.textContent, lang);
			});
		});
	}

	function decorateEditors() {
		document.querySelectorAll(".tcd-playground textarea.tcd-editor").forEach((area) => {
			if (area.dataset.tcdHl) return;
			area.dataset.tcdHl = "1";
			const lang = area.closest("[data-language]")?.dataset.language || "";
			const wrap = document.createElement("div");
			wrap.className = "tcd-editor-wrap";
			const pre = document.createElement("pre");
			pre.className = "tcd-editor-hl";
			pre.setAttribute("aria-hidden", "true");
			area.setAttribute("wrap", "off");
			area.classList.add("tcd-editor-overlay");
			area.replaceWith(wrap);
			wrap.append(pre, area);
			const paint = () => {
				// trailing newline keeps the last empty line visible
				pre.innerHTML = highlightCode(area.value, lang) + "\n";
				pre.scrollTop = area.scrollTop;
				pre.scrollLeft = area.scrollLeft;
			};
			area.addEventListener("input", paint);
			area.addEventListener("scroll", () => {
				pre.scrollTop = area.scrollTop;
				pre.scrollLeft = area.scrollLeft;
			});
			paint();
		});
	}

	function init() {
		const t = labels();
		decorateBlocks(t);
		decorateInline();
		decorateEditors();
	}

	window.tcdHighlight = { code: highlightCode };
	if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
	else init();
})();
