/*
 * VintraXo TCD playground runtime.
 *
 * Learner code never runs on the server and never runs in the page's origin:
 * every run creates an <iframe sandbox="allow-scripts"> (opaque origin: no cookies,
 * no access to this page or the Frappe API as the learner). Inside it a Web Worker
 * executes the code; the worker is terminated when the time limit is reached, and
 * the parent removes the whole iframe as a last resort.
 *
 *   python      -> Pyodide (WASM)
 *   sql         -> sql.js  (SQLite WASM), fresh in-memory database per run
 *   javascript  -> plain worker with console capture
 *   html        -> rendered preview in a sandboxed iframe
 */
(function () {
	"use strict";

	const MAX_OUTPUT = 100000; // characters
	const LOAD_GRACE_SECONDS = 90; // time allowed to download a runtime

	// ------------------------------------------------------------ worker sources
	// These functions are serialized with toString() and run inside the worker.

	function pythonWorker(indexURL) {
		/* global importScripts, loadPyodide */
		let ready;
		try {
			importScripts(indexURL + "pyodide.js");
			ready = loadPyodide({ indexURL: indexURL }).then(function (py) {
				py.setStdout({ batched: (s) => postMessage({ type: "stdout", text: s + "\n" }) });
				py.setStderr({ batched: (s) => postMessage({ type: "stderr", text: s + "\n" }) });
				postMessage({ type: "loaded" });
				return py;
			});
		} catch (e) {
			ready = Promise.reject(e);
		}
		ready.catch((e) => postMessage({ type: "error", text: "Could not load Python: " + (e.message || e) }));
		onmessage = async function (e) {
			const py = await ready;
			const t = performance.now();
			try {
				await py.loadPackagesFromImports(e.data.code);
				const result = await py.runPythonAsync(e.data.code);
				if (result !== undefined && result !== null) {
					postMessage({ type: "stdout", text: String(result) + "\n" });
				}
				postMessage({ type: "done", ms: Math.round(performance.now() - t) });
			} catch (err) {
				postMessage({ type: "error", text: String(err.message || err) });
			}
		};
	}

	function sqlWorker(baseURL) {
		/* global importScripts, initSqlJs */
		let ready;
		try {
			importScripts(baseURL + "sql-wasm.js");
			ready = initSqlJs({ locateFile: (f) => baseURL + f }).then(function (SQL) {
				postMessage({ type: "loaded" });
				return SQL;
			});
		} catch (e) {
			ready = Promise.reject(e);
		}
		ready.catch((e) => postMessage({ type: "error", text: "Could not load SQLite: " + (e.message || e) }));
		onmessage = async function (e) {
			const SQL = await ready;
			const db = new SQL.Database();
			const t = performance.now();
			try {
				const results = db.exec(e.data.code);
				results.forEach((r) => postMessage({ type: "table", columns: r.columns, values: r.values }));
				if (!results.length) postMessage({ type: "stdout", text: "OK (" + db.getRowsModified() + " rows changed)\n" });
				postMessage({ type: "done", ms: Math.round(performance.now() - t) });
			} catch (err) {
				postMessage({ type: "error", text: String(err.message || err) });
			} finally {
				db.close();
			}
		};
	}

	function javascriptWorker() {
		const fmt = (args) =>
			args
				.map(function (x) {
					if (typeof x === "string") return x;
					try {
						return JSON.stringify(x);
					} catch (_) {
						return String(x);
					}
				})
				.join(" ");
		console.log = console.info = console.debug = (...a) => postMessage({ type: "stdout", text: fmt(a) + "\n" });
		console.warn = console.error = (...a) => postMessage({ type: "stderr", text: fmt(a) + "\n" });
		const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
		// pending setTimeout calls keep the run open (so "await wait(500)" and timers print); the page's hard
		// time limit still stops code that never finishes
		const nativeSet = setTimeout, nativeClear = clearTimeout, live = new Set();
		let started = 0, codeDone = false;
		const settle = () => nativeSet(() => {
			if (codeDone && live.size === 0) {
				codeDone = false;
				postMessage({ type: "done", ms: Math.round(performance.now() - started) });
			}
		}, 0);
		self.setTimeout = (fn, ms, ...args) => {
			const id = nativeSet(() => {
				live.delete(id);
				try {
					if (typeof fn === "function") fn(...args);
				} catch (err) {
					postMessage({ type: "error", text: String((err && err.stack) || err) });
				}
				settle();
			}, ms);
			live.add(id);
			return id;
		};
		self.clearTimeout = (id) => {
			live.delete(id);
			nativeClear(id);
			settle();
		};
		postMessage({ type: "loaded" });
		onmessage = async function (e) {
			started = performance.now();
			try {
				await new AsyncFunction(e.data.code)();
				codeDone = true;
				settle();
			} catch (err) {
				postMessage({ type: "error", text: String((err && err.stack) || err) });
			}
		};
	}

	function workerSource(language, config) {
		const call = (fn, arg) => "(" + fn.toString() + ")(" + JSON.stringify(arg) + ");";
		if (language === "python") return call(pythonWorker, config.pyodide_index_url);
		if (language === "sql") return call(sqlWorker, config.sqljs_base_url);
		if (language === "javascript") return call(javascriptWorker, null);
		return null;
	}

	// ------------------------------------------------------------ sandbox runner (inside the iframe)

	const RUNNER_HTML =
		"<!doctype html><meta charset='utf-8'><script>" +
		"(" +
		function () {
			window.addEventListener(
				"message",
				function (e) {
					if (e.source !== parent) return;
					const job = e.data;
					let worker, timer;
					const send = (msg) => parent.postMessage(msg, "*");
					try {
						const url = URL.createObjectURL(new Blob([job.source], { type: "text/javascript" }));
						worker = new Worker(url);
					} catch (err) {
						send({ type: "error", text: "This browser cannot start the playground: " + err.message });
						return;
					}
					worker.onmessage = function (m) {
						const d = m.data;
						if (d.type === "loaded") {
							send({ type: "started" });
							timer = setTimeout(function () {
								worker.terminate();
								send({ type: "timeout" });
							}, job.timeout * 1000);
							worker.postMessage({ code: job.code });
							return;
						}
						if (d.type === "done" || d.type === "error") {
							clearTimeout(timer);
							worker.terminate();
						}
						send(d);
					};
					worker.onerror = function (ev) {
						clearTimeout(timer);
						worker.terminate();
						send({ type: "error", text: ev.message || "Worker error" });
					};
				},
				{ once: true }
			);
			parent.postMessage({ type: "runner-ready" }, "*");
		}.toString() +
		")();<\/script>";

	// ------------------------------------------------------------ UI

	function labels() {
		try {
			return JSON.parse(document.getElementById("tcd-labels").textContent);
		} catch (_) {
			return {};
		}
	}

	function config() {
		try {
			return JSON.parse(document.getElementById("tcd-playground-config").textContent);
		} catch (_) {
			return { enabled: false };
		}
	}

	function el(tag, attrs, text) {
		const node = document.createElement(tag);
		Object.entries(attrs || {}).forEach(([k, v]) => node.setAttribute(k, v));
		if (text !== undefined) node.textContent = text;
		return node;
	}

	function format(template, ...args) {
		return String(template || "").replace(/\{(\d+)\}/g, (_, i) => args[i]);
	}

	/** Languages the browser cannot run go to the isolated code runner (Phase 10) through the API. */
	function onRunner(language, cfg) {
		return !workerSource(language, cfg) && language !== "html" && (cfg.runner_languages || []).includes(language);
	}

	async function runOnServer(language, code) {
		const res = await fetch("/api/method/vintraxo_tcd.api.run_code", {
			method: "POST",
			credentials: "same-origin",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
				"X-Frappe-CSRF-Token": (window.frappe && window.frappe.csrf_token) || "",
			},
			body: JSON.stringify({ language: language, code: code }),
		});
		const data = await res.json().catch(() => ({}));
		if (!res.ok) {
			let msg = res.statusText;
			try {
				const msgs = JSON.parse(data._server_messages || "[]").map((m) => JSON.parse(m).message);
				if (msgs.length) msg = new DOMParser().parseFromString(msgs.join(" "), "text/html").body.textContent;
			} catch (_) {
				/* keep statusText */
			}
			throw new Error(msg);
		}
		return data.message; // {status, output, error, time_ms, memory_kb}
	}

	class Playground {
		constructor(section, cfg, t) {
			this.section = section;
			this.cfg = cfg;
			this.t = t;
			this.language = section.dataset.language;
			this.editor = section.querySelector(".tcd-editor");
			this.output = section.querySelector(".tcd-output");
			const expected = section.querySelector("template.tcd-expected");
			this.expected = expected ? expected.content.textContent : null;
			const setup = section.querySelector("template.tcd-setup");
			this.setup = setup ? setup.content.textContent : ""; // hidden code run before the learner's code
			this.original = this.editor.value;
			this.frame = null;
			this.buildActions();
			this.enableTabKey();
			this.onMessage = this.onMessage.bind(this);
		}

		buildActions() {
			const bar = this.section.querySelector(".tcd-playground-actions");
			this.runBtn = el("button", { type: "button", class: "btn btn-primary btn-xs" }, this.t.run || "Run");
			this.stopBtn = el("button", { type: "button", class: "btn btn-default btn-xs", hidden: "" }, this.t.stop || "Stop");
			this.resetBtn = el("button", { type: "button", class: "btn btn-default btn-xs" }, this.t.reset || "Reset");
			this.runBtn.addEventListener("click", () => this.run());
			this.stopBtn.addEventListener("click", () => this.finish(this.t.stopped || "Stopped.", "warn"));
			this.resetBtn.addEventListener("click", () => {
				this.editor.value = this.original;
				this.editor.dispatchEvent(new Event("input"));
				this.clearOutput();
			});
			this.fullBtn = el("button", { type: "button", class: "btn btn-default btn-xs tcd-full-btn", "aria-pressed": "false" }, this.t.full_screen || "Full screen");
			this.fullBtn.addEventListener("click", () => this.toggleFull());
			bar.append(this.runBtn, this.stopBtn, this.resetBtn, this.fullBtn);
			// a server language (Java, C#, ...) while the code runner is off: say so instead of failing on click
			if (this.language !== "html" && !workerSource(this.language, this.cfg) && !onRunner(this.language, this.cfg)) {
				this.runBtn.disabled = true;
				const note = el("p", { class: "tcd-muted tcd-small tcd-runner-off" }, this.t.runner_off || "This example runs once the code runner is enabled.");
				this.section.insertBefore(note, this.output);
			}
		}

		// "Try it yourself" (Phase 17): the editor and the result side by side over the whole window
		toggleFull(force) {
			const on = force === undefined ? !this.section.classList.contains("tcd-playground-full") : force;
			this.section.classList.toggle("tcd-playground-full", on);
			document.documentElement.classList.toggle("tcd-no-scroll", on);
			this.fullBtn.setAttribute("aria-pressed", on ? "true" : "false");
			this.fullBtn.textContent = on ? this.t.exit_full_screen || "Exit full screen" : this.t.full_screen || "Full screen";
			if (on) {
				this.output.hidden = false;
				this.editor.focus();
				this.onEsc = (e) => {
					if (e.key === "Escape") this.toggleFull(false);
				};
				document.addEventListener("keydown", this.onEsc);
			} else {
				if (!this.output.childElementCount) this.output.hidden = true;
				document.removeEventListener("keydown", this.onEsc);
				this.fullBtn.focus();
			}
		}

		enableTabKey() {
			this.editor.addEventListener("keydown", (e) => {
				if (e.key === "Tab" && !e.shiftKey && !e.ctrlKey && !e.metaKey) {
					e.preventDefault();
					const { selectionStart: s, selectionEnd: end, value } = this.editor;
					this.editor.value = value.slice(0, s) + "    " + value.slice(end);
					this.editor.selectionStart = this.editor.selectionEnd = s + 4;
					this.editor.dispatchEvent(new Event("input"));
				} else if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
					e.preventDefault();
					this.run();
				}
			});
		}

		clearOutput() {
			this.output.replaceChildren();
			this.output.hidden = true;
			this.stdout = "";
			this.size = 0;
		}

		status(text, kind) {
			const line = el("div", { class: "tcd-run-status" + (kind ? " tcd-run-" + kind : "") }, text);
			this.output.append(line);
			this.output.hidden = false;
		}

		write(text, kind) {
			if (this.size > MAX_OUTPUT) return;
			this.size += text.length;
			if (this.size > MAX_OUTPUT) text = text.slice(0, MAX_OUTPUT) + "\n...";
			if (kind !== "stderr") this.stdout += text;
			let pre = this.output.lastElementChild;
			if (!pre || pre.tagName !== "PRE" || pre.dataset.kind !== kind) {
				pre = el("pre", { "data-kind": kind, class: kind === "stderr" ? "tcd-stderr" : "" });
				this.output.append(pre);
			}
			pre.textContent += text;
			this.output.hidden = false;
		}

		table(columns, values) {
			const wrap = el("div", { class: "tcd-table-wrap" });
			const table = el("table", { class: "table table-sm" });
			const head = el("tr");
			columns.forEach((c) => head.append(el("th", {}, String(c))));
			table.append(el("thead"));
			table.tHead.append(head);
			const body = el("tbody");
			values.slice(0, 500).forEach((row) => {
				const tr = el("tr");
				row.forEach((v) => tr.append(el("td", {}, v === null ? "NULL" : String(v))));
				body.append(tr);
			});
			table.append(body);
			wrap.append(table);
			this.output.append(wrap);
			this.output.hidden = false;
			this.stdout += columns.join("|") + "\n" + values.map((r) => r.join("|")).join("\n") + "\n";
		}

		run() {
			this.kill();
			this.clearOutput();
			const code = this.editor.value;

			if (this.language === "html") {
				const preview = el("iframe", {
					sandbox: "allow-scripts",
					class: "tcd-preview",
					title: this.t.preview || "Preview",
					referrerpolicy: "no-referrer",
				});
				preview.srcdoc = this.setup ? this.setup + "\n" + code : code; // e.g. a framework's <link>/<script>
				this.output.append(preview);
				this.output.hidden = false;
				return;
			}

			const full = this.setup ? this.setup + "\n" + code : code;
			if (onRunner(this.language, this.cfg)) return this.runServer(full);
			const source = workerSource(this.language, this.cfg);
			if (!source) return this.status(this.language + ": unsupported", "error");

			this.running = true;
			this.runBtn.disabled = true;
			this.stopBtn.hidden = false;
			this.status(this.language === "javascript" ? this.t.running || "Running..." : this.t.loading_runtime || "Loading...");

			this.job = { source: source, code: full, timeout: this.cfg.timeout_seconds || 5 };
			this.frame = el("iframe", { sandbox: "allow-scripts", hidden: "", "aria-hidden": "true", tabindex: "-1" });
			this.frame.srcdoc = RUNNER_HTML;
			window.addEventListener("message", this.onMessage);
			this.section.append(this.frame);
			this.hardStop = setTimeout(
				() => this.finish(format(this.t.timeout, this.job.timeout), "error"),
				(this.job.timeout + LOAD_GRACE_SECONDS) * 1000
			);
		}

		onMessage(e) {
			if (!this.frame || e.source !== this.frame.contentWindow) return;
			const d = e.data || {};
			switch (d.type) {
				case "runner-ready":
					this.frame.contentWindow.postMessage(this.job, "*");
					break;
				case "started":
					this.output.querySelector(".tcd-run-status")?.remove();
					this.output.hidden = true;
					break;
				case "stdout":
				case "stderr":
					this.write(String(d.text || ""), d.type);
					break;
				case "table":
					this.table(d.columns || [], d.values || []);
					break;
				case "done":
					this.finish(format(this.t.done_in, d.ms), "ok");
					this.checkExpected();
					break;
				case "error":
					this.write(String(d.text || ""), "stderr");
					this.finish(this.t.error || "Error", "error");
					break;
				case "timeout":
					this.finish(format(this.t.timeout, this.job.timeout), "error");
					break;
			}
		}

		async runServer(code) {
			this.running = true;
			this.runBtn.disabled = true;
			this.status(this.t.running_on_server || this.t.running || "Running...");
			try {
				const r = await runOnServer(this.language, code);
				this.output.querySelector(".tcd-run-status")?.remove();
				if (r.output) this.write(r.output, "stdout");
				if (r.error) this.write(r.error, "stderr");
				if (r.status === "Finished") {
					this.finish(format(this.t.done_in, r.time_ms), "ok");
					this.checkExpected();
				} else {
					this.finish(this.t["runner_" + r.status.toLowerCase().replace(/ /g, "_")] || r.status, "error");
				}
			} catch (err) {
				this.finish(err.message, "error");
			}
		}

		checkExpected() {
			if (this.expected === null) return;
			const norm = (s) => s.replace(/\r/g, "").trim();
			if (norm(this.stdout) === norm(this.expected)) this.status(this.t.output_matches, "ok");
			else this.status(this.t.output_differs, "warn");
		}

		finish(message, kind) {
			if (!this.running) return;
			this.kill();
			if (!this.output.querySelector("pre, .tcd-table-wrap") && kind === "ok") {
				this.status(this.t.no_output || "(no output)");
			}
			this.status(message, kind);
		}

		kill() {
			this.running = false;
			clearTimeout(this.hardStop);
			window.removeEventListener("message", this.onMessage);
			if (this.frame) this.frame.remove(); // also terminates the worker inside
			this.frame = null;
			this.runBtn.disabled = false;
			this.stopBtn.hidden = true;
		}
	}

	/**
	 * Headless run in the same sandbox (used by code/SQL quiz questions).
	 * Resolves with { stdout, stderr, tables, error, timedOut } and never touches the page origin.
	 */
	function runHeadless(language, code, options = {}) {
		const cfg = config();
		if (onRunner(language, cfg) || options.server) {
			const full = (options.setup ? options.setup + "\n" : "") + code;
			return runOnServer(language, full).then(
				(r) => ({ stdout: r.output || "", stderr: r.error || "", tables: [], error: r.status === "Finished" ? null : r.error || r.status, timedOut: r.status === "Time Limit" }),
				(err) => ({ stdout: "", stderr: "", tables: [], error: err.message, timedOut: false })
			);
		}
		const source = workerSource(language, cfg);
		if (!source) return Promise.resolve({ error: language + ": unsupported" });
		const timeout = options.timeout || cfg.timeout_seconds || 5;
		const job = { source: source, code: (options.setup ? options.setup + "\n" : "") + code, timeout: timeout };
		return new Promise((resolve) => {
			const out = { stdout: "", stderr: "", tables: [], error: null, timedOut: false };
			const frame = el("iframe", { sandbox: "allow-scripts", hidden: "", "aria-hidden": "true", tabindex: "-1" });
			let hard;
			const done = () => {
				clearTimeout(hard);
				window.removeEventListener("message", onMessage);
				frame.remove();
				resolve(out);
			};
			const onMessage = (e) => {
				if (e.source !== frame.contentWindow) return;
				const d = e.data || {};
				if (d.type === "runner-ready") frame.contentWindow.postMessage(job, "*");
				else if (d.type === "stdout") out.stdout += String(d.text || "");
				else if (d.type === "stderr") out.stderr += String(d.text || "");
				else if (d.type === "table") out.tables.push({ columns: d.columns || [], values: d.values || [] });
				else if (d.type === "error") (out.error = String(d.text || "")), done();
				else if (d.type === "timeout") (out.timedOut = true), done();
				else if (d.type === "done") done();
			};
			window.addEventListener("message", onMessage);
			frame.srcdoc = RUNNER_HTML;
			document.body.append(frame);
			hard = setTimeout(() => ((out.timedOut = true), done()), (timeout + LOAD_GRACE_SECONDS) * 1000);
		});
	}

	/** Canonical text output used for grading: stdout, or SQL tables as "col|col" + one line per row. */
	function canonicalOutput(language, result) {
		if (language === "sql") {
			return result.tables
				.map((t) => [t.columns.join("|"), ...t.values.map((r) => r.map((v) => (v === null ? "NULL" : String(v))).join("|"))].join("\n"))
				.join("\n");
		}
		return result.stdout;
	}

	window.TCDPlayground = { run: runHeadless, canonicalOutput: canonicalOutput };

	function init() {
		const cfg = config();
		if (!cfg.enabled) return;
		const t = labels();
		document.querySelectorAll(".tcd-playground").forEach((section) => new Playground(section, cfg, t));
	}

	if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
	else init();
})();
