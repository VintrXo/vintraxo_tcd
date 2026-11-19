/* VintraXo TCD learner portal: progress tracking, completion and quizzes. */
(function () {
	"use strict";

	const API = "/api/method/vintraxo_tcd.api.";

	function labels() {
		try {
			return JSON.parse(document.getElementById("tcd-labels").textContent);
		} catch (_) {
			return {};
		}
	}

	function format(template, ...args) {
		return String(template || "").replace(/\{(\d+)\}/g, (_, i) => args[i]);
	}

	function el(tag, attrs, text) {
		const node = document.createElement(tag);
		Object.entries(attrs || {}).forEach(([k, v]) => node.setAttribute(k, v));
		if (text !== undefined) node.textContent = text;
		return node;
	}

	function serverMessage(data) {
		try {
			const msgs = JSON.parse(data._server_messages || "[]").map((m) => JSON.parse(m).message);
			if (msgs.length) {
				// DOMParser documents are inert (no scripts, no image loads): safe for stripping tags
				return new DOMParser().parseFromString(msgs.join(" "), "text/html").body.textContent;
			}
		} catch (_) {
			/* ignore */
		}
		return data.exception || data.exc_type || "";
	}

	async function call(method, args, post) {
		const opts = {
			method: post ? "POST" : "GET",
			credentials: "same-origin",
			headers: { Accept: "application/json" },
		};
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

	// ------------------------------------------------------------ page

	function initEnroll() {
		document.querySelectorAll(".tcd-enroll[data-name]").forEach((btn) => {
			btn.addEventListener("click", async () => {
				const message = btn.closest("section")?.querySelector(".tcd-message");
				btn.disabled = true;
				try {
					await call("enroll", { enrollment_for: btn.dataset.for, name: btn.dataset.name }, true);
					window.location.reload();
				} catch (e) {
					if (message) {
						message.textContent = e.message;
						message.hidden = false;
						message.classList.add("tcd-error");
					}
					btn.disabled = false;
				}
			});
		});
	}

	async function uploadPrivate(file) {
		const form = new FormData();
		form.append("file", file, file.name);
		form.append("is_private", "1");
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

	function showIn(section, text, isError) {
		let msg = section.querySelector(".tcd-message");
		if (!msg) {
			msg = el("p", { class: "tcd-message", role: "status" });
			section.append(msg);
		}
		msg.textContent = text;
		msg.hidden = !text;
		msg.classList.toggle("tcd-error", !!isError);
	}

	function initAssignment(t) {
		document.querySelectorAll(".tcd-assignment[data-assignment]").forEach((section) => {
			const form = section.querySelector(".tcd-assignment-form");
			if (!form) return;
			form.addEventListener("submit", async (e) => {
				e.preventDefault();
				const button = form.querySelector("button[type=submit]");
				button.disabled = true;
				try {
					const args = { name: section.dataset.assignment };
					const text = form.querySelector("textarea[name=answer_text]");
					if (text) args.answer_text = text.value;
					const fileInput = form.querySelector("input[type=file]");
					if (fileInput && fileInput.files.length) {
						showIn(section, t.uploading || "Uploading...");
						args.attachment = await uploadPrivate(fileInput.files[0]);
					}
					await call("submit_assignment", args, true);
					window.location.reload();
				} catch (err) {
					showIn(section, err.message, true);
					button.disabled = false;
				}
			});
		});
	}

	function initRating(t) {
		const section = document.querySelector(".tcd-rating[data-course]");
		const form = section && section.querySelector(".tcd-rating-form");
		if (!form) return;
		form.addEventListener("submit", async (e) => {
			e.preventDefault();
			const checked = form.querySelector("input[name=rating]:checked");
			if (!checked) return showIn(section, t.choose_rating || "Choose a rating.", true);
			try {
				await call(
					"rate_course",
					{ name: section.dataset.course, rating: Number(checked.value), comment: form.querySelector("textarea").value },
					true
				);
				showIn(section, t.saved || "Saved.");
			} catch (err) {
				showIn(section, err.message, true);
			}
		});
	}

	function initHelpful(t) {
		const section = document.querySelector(".tcd-helpful[data-content]");
		const form = section && section.querySelector(".tcd-helpful-form");
		if (!form) return;
		form.addEventListener("submit", async (e) => {
			e.preventDefault();
			const checked = form.querySelector("input[name=helpful]:checked");
			if (!checked) return showIn(section, t.choose_rating || "Choose an answer.", true);
			try {
				await call(
					"content_feedback",
					{ name: section.dataset.content, helpful: Number(checked.value), comment: form.querySelector("textarea").value },
					true
				);
				showIn(section, t.thanks || "Thank you.");
			} catch (err) {
				showIn(section, err.message, true);
			}
		});
	}

	function initAcknowledge() {
		const section = document.querySelector(".tcd-ack[data-code]");
		const btn = section && section.querySelector(".tcd-ack-btn");
		if (!btn) return;
		const box = section.querySelector("input[type=checkbox]");
		box.addEventListener("change", () => (btn.disabled = !box.checked));
		btn.addEventListener("click", async () => {
			btn.disabled = true;
			try {
				await call("acknowledge", { code: section.dataset.code }, true);
				window.location.reload();
			} catch (err) {
				showIn(section, err.message, true);
				btn.disabled = false;
			}
		});
	}

	function initApprove() {
		document.querySelectorAll(".tcd-approve[data-name]").forEach((btn) => {
			btn.addEventListener("click", async () => {
				btn.disabled = true;
				try {
					await call("approve_enrollment", { name: btn.dataset.name }, true);
					btn.closest("li").remove();
				} catch (err) {
					showIn(btn.closest("section"), err.message, true);
					btn.disabled = false;
				}
			});
		});
	}

	function initAssistant(t) {
		const form = document.querySelector(".tcd-assistant-form");
		if (!form) return;
		const out = document.querySelector(".tcd-assistant-output");
		let mode = "ask";
		form.querySelectorAll("button[data-mode]").forEach((b) => b.addEventListener("click", () => (mode = b.dataset.mode)));
		const safeUrl = (u) => (typeof u === "string" && u.startsWith("/") && !u.startsWith("//") ? u : "#");
		const sourceList = (sources) => {
			const ol = el("ol", { class: "tcd-assistant-sources" });
			sources.forEach((s, i) => {
				const li = el("li", { id: "tcd-src-" + (i + 1) });
				li.appendChild(el("a", { href: safeUrl(s.url) }, s.title));
				ol.appendChild(li);
			});
			return ol;
		};
		form.addEventListener("submit", async (e) => {
			e.preventDefault();
			const question = form.question.value.trim();
			if (!question) return;
			const buttons = form.querySelectorAll("button");
			buttons.forEach((b) => (b.disabled = true));
			out.replaceChildren(el("p", { class: "tcd-muted" }, t.thinking));
			try {
				if (mode === "search") {
					const r = await call("ai_search", { query: question }, true);
					out.replaceChildren();
					if (r.keywords && r.keywords.length) out.appendChild(el("p", { class: "tcd-muted tcd-small" }, format(t.related_terms, r.keywords.join("، "))));
					if (!r.results.length) out.appendChild(el("p", { class: "tcd-muted" }, t.no_results));
					else out.appendChild(sourceList(r.results));
				} else {
					const r = await call("ai_ask", { question }, true);
					const answer = el("div", { class: "tcd-assistant-answer" });
					r.answer.forEach((seg) => {
						answer.appendChild(document.createTextNode(seg.text));
						(seg.sources || []).forEach((n) => {
							const sup = el("sup");
							sup.appendChild(el("a", { href: "#tcd-src-" + (n + 1) }, "[" + (n + 1) + "]"));
							answer.appendChild(sup);
						});
					});
					out.replaceChildren(answer);
					if (r.sources.length) {
						out.appendChild(el("h3", {}, t.sources));
						out.appendChild(sourceList(r.sources));
					}
				}
			} catch (err) {
				out.replaceChildren(el("p", { class: "tcd-error" }, err.message));
			} finally {
				buttons.forEach((b) => (b.disabled = false));
			}
		});
	}

	function init() {
		initEnroll();
		const t0 = labels();
		initAssignment(t0);
		initRating(t0);
		initHelpful(t0);
		initAcknowledge();
		initApprove();
		initAssistant(t0);
		const page = document.querySelector(".tcd-content[data-content]");
		if (!page) return;
		const t = labels();
		const name = page.dataset.content;
		const message = page.querySelector(".tcd-message");
		const completeBtn = page.querySelector(".tcd-complete");
		const progressLabel = page.querySelector("[data-progress-label]");

		const show = (text, isError) => {
			message.textContent = text;
			message.hidden = !text;
			message.classList.toggle("tcd-error", !!isError);
		};

		const setCompleted = () => {
			page.dataset.progress = "Completed";
			if (progressLabel) {
				progressLabel.textContent = t.completed || "Completed";
				progressLabel.className = "tcd-status tcd-status-completed";
			}
			if (completeBtn) completeBtn.hidden = true;
		};

		if (page.dataset.progress === "Not Started") {
			call("track_view", { name: name }, true).catch(() => {});
		}

		if (completeBtn) {
			completeBtn.addEventListener("click", async () => {
				completeBtn.disabled = true;
				try {
					await call("complete_lesson", { name: name }, true);
					setCompleted();
					show("");
				} catch (e) {
					show(e.message, true);
				} finally {
					completeBtn.disabled = false;
				}
			});
		}

		const quizSection = page.querySelector(".tcd-quiz[data-quiz]");
		if (quizSection) new Quiz(quizSection, t, setCompleted).load();
	}

	// ------------------------------------------------------------ quiz

	class Quiz {
		constructor(section, t, onPassed) {
			this.section = section;
			this.body = section.querySelector(".tcd-quiz-body");
			this.name = section.dataset.quiz;
			this.t = t;
			this.onPassed = onPassed;
		}

		async load(start) {
			try {
				this.quiz = await call(start ? "start_quiz" : "get_quiz", { name: this.name }, !!start);
				this.render();
			} catch (e) {
				this.body.replaceChildren(el("p", { class: "tcd-error" }, e.message));
			}
		}

		attemptsText() {
			const q = this.quiz;
			if (q.attempts_left === null || q.attempts_left === undefined) return "";
			return q.attempts_left > 0 ? format(this.t.attempts_left, q.attempts_left) : this.t.no_attempts;
		}

		render() {
			const q = this.quiz;
			const t = this.t;
			clearInterval(this.timer);
			const wrap = el("div");
			if (q.passed) wrap.append(el("p", { class: "tcd-status tcd-status-completed" }, t.passed || "Passed"));
			if (q.pending_review) wrap.append(el("p", { class: "tcd-callout tcd-callout-info" }, t.pending_review));
			if (q.requires_start) {
				const info = el("p", { class: "tcd-muted" });
				info.textContent = [q.time_limit_minutes ? format(t.time_limit, q.time_limit_minutes) : "", this.attemptsText()]
					.filter(Boolean)
					.join(" · ");
				const btn = el("button", { type: "button", class: "btn btn-primary" }, t.start_quiz || "Start");
				btn.disabled = q.attempts_left === 0;
				btn.addEventListener("click", () => this.load(true));
				wrap.append(info, btn);
				this.body.replaceChildren(wrap);
				return;
			}
			const form = el("form", { class: "tcd-quiz-form", novalidate: "" });
			if (q.attempt && q.attempt.seconds_left !== null && q.attempt.seconds_left !== undefined) {
				const clock = el("p", { class: "tcd-timer", role: "timer", "aria-live": "off" });
				form.append(clock);
				let left = q.attempt.seconds_left;
				const tick = () => {
					clock.textContent = format(t.time_left, Math.floor(left / 60) + ":" + String(left % 60).padStart(2, "0"));
					if (left <= 0) {
						clearInterval(this.timer);
						form.requestSubmit();
					}
					left -= 1;
				};
				tick();
				this.timer = setInterval(tick, 1000);
			}
			q.questions.forEach((question, i) => form.append(this.renderQuestion(question, i)));
			const footer = el("div", { class: "tcd-quiz-footer" });
			const submit = el("button", { type: "submit", class: "btn btn-primary" }, t.submit || "Submit");
			if (q.attempts_left === 0 && !q.attempt) submit.disabled = true;
			footer.append(submit, el("span", { class: "tcd-muted" }, this.attemptsText()));
			form.append(footer);
			form.addEventListener("submit", (e) => {
				e.preventDefault();
				this.submit(form, submit);
			});
			wrap.append(form);
			this.body.replaceChildren(wrap);
		}

		renderQuestion(question, i) {
			const t = this.t;
			const fs = el("fieldset", { class: "tcd-question", "data-id": question.id, "data-type": question.type });
			fs.append(el("legend", {}, i + 1 + ". " + question.question));
			if (question.scenario) fs.prepend(el("div", { class: "tcd-scenario" }, question.scenario));
			const name = "q-" + question.id;
			const type = question.type;
			if (["Single Choice", "Multiple Choice", "True False"].includes(type)) {
				question.options.forEach((opt) => {
					const label = el("label", { class: "tcd-option" });
					const input = el("input", { type: type === "Multiple Choice" ? "checkbox" : "radio", name, value: String(opt.value) });
					label.append(input, el("span", {}, opt.label));
					fs.append(label);
				});
			} else if (type === "Fill Blank") {
				for (let b = 0; b < question.blanks; b++) {
					fs.append(el("input", { type: "text", class: "form-control tcd-blank", dir: "auto", "aria-label": format(t.blank_n, b + 1) }));
				}
			} else if (type === "Matching") {
				question.lefts.forEach((left, li) => {
					const row = el("label", { class: "tcd-match" });
					const select = el("select", { class: "form-control tcd-select", "data-left": String(li) });
					select.append(el("option", { value: "" }, "—"));
					question.rights.forEach((r) => select.append(el("option", { value: r }, r)));
					row.append(el("span", {}, left), select);
					fs.append(row);
				});
			} else if (type === "Ordering") {
				const list = el("ol", { class: "tcd-order" });
				question.items.forEach((it) => {
					const li = el("li", { "data-value": String(it.value) });
					const up = el("button", { type: "button", class: "btn btn-xs btn-default", "aria-label": t.move_up || "Up" }, "↑");
					const down = el("button", { type: "button", class: "btn btn-xs btn-default", "aria-label": t.move_down || "Down" }, "↓");
					up.addEventListener("click", () => li.previousElementSibling && list.insertBefore(li, li.previousElementSibling));
					down.addEventListener("click", () => li.nextElementSibling && list.insertBefore(li.nextElementSibling, li));
					li.append(el("span", {}, it.label), up, down);
					list.append(li);
				});
				fs.append(list);
			} else if (type === "Short Answer") {
				fs.append(el("input", { type: "text", class: "form-control tcd-text-answer", dir: "auto" }));
			} else if (type === "Essay") {
				fs.append(el("textarea", { class: "form-control tcd-text-answer", rows: "6", dir: "auto" }));
			} else if (type === "File") {
				const accept = (question.allowed_extensions || "").split(",").filter(Boolean).map((x) => "." + x.trim()).join(",");
				fs.append(el("input", accept ? { type: "file", class: "tcd-file-answer", accept } : { type: "file", class: "tcd-file-answer" }));
			} else if (type === "Code" || type === "SQL") {
				const editor = el("textarea", { class: "tcd-editor tcd-code-answer", dir: "ltr", spellcheck: "false", rows: "8" });
				editor.value = question.starter_code || "";
				const run = el("button", { type: "button", class: "btn btn-xs btn-default" }, t.run || "Run");
				const output = el("pre", { class: "tcd-code-output", dir: "ltr", hidden: "" });
				run.addEventListener("click", () => this.runCode(fs, question));
				fs.append(editor, run, output, el("p", { class: "tcd-muted tcd-small" }, t.code_note));
			}
			if (question.manual) fs.append(el("p", { class: "tcd-muted tcd-small" }, t.manual_note));
			if (question.rubric && question.rubric.length) {
				const r = el("ul", { class: "tcd-rubric tcd-muted tcd-small" });
				question.rubric.forEach((c) => r.append(el("li", {}, c.criterion + " (" + c.max_points + ")")));
				fs.append(r);
			}
			return fs;
		}

		async runCode(fs, question) {
			const output = fs.querySelector(".tcd-code-output");
			if (!window.TCDPlayground) return null;
			output.hidden = false;
			output.textContent = this.t.running || "Running...";
			const res = await window.TCDPlayground.run(question.language, fs.querySelector(".tcd-code-answer").value, {
				setup: question.setup_code,
				server: question.run_on_server,
			});
			const text = res.error || (res.timedOut ? this.t.stopped : window.TCDPlayground.canonicalOutput(question.language, res));
			output.textContent = text || this.t.no_output || "";
			fs.dataset.output = res.error || res.timedOut ? "" : window.TCDPlayground.canonicalOutput(question.language, res);
			fs.dataset.code = fs.querySelector(".tcd-code-answer").value;
			return fs.dataset.output;
		}

		async collect(form) {
			const answers = {};
			for (const fs of form.querySelectorAll("fieldset[data-id]")) {
				const id = fs.dataset.id;
				const type = fs.dataset.type;
				if (["Single Choice", "Multiple Choice", "True False"].includes(type)) {
					answers[id] = Array.from(fs.querySelectorAll("input:checked")).map((i) => Number(i.value));
				} else if (type === "Fill Blank") {
					answers[id] = Array.from(fs.querySelectorAll(".tcd-blank")).map((i) => i.value);
				} else if (type === "Matching") {
					answers[id] = {};
					fs.querySelectorAll("select[data-left]").forEach((s) => (answers[id][s.dataset.left] = s.value));
				} else if (type === "Ordering") {
					answers[id] = Array.from(fs.querySelectorAll(".tcd-order li")).map((li) => Number(li.dataset.value));
				} else if (type === "Short Answer" || type === "Essay") {
					answers[id] = fs.querySelector(".tcd-text-answer").value;
				} else if (type === "File") {
					const input = fs.querySelector(".tcd-file-answer");
					answers[id] = input.files.length ? await uploadPrivate(input.files[0]) : "";
				} else if (type === "Code" || type === "SQL") {
					const question = this.quiz.questions.find((x) => x.id === id);
					const code = fs.querySelector(".tcd-code-answer").value;
					if (fs.dataset.code !== code) await this.runCode(fs, question);
					answers[id] = { code, output: fs.dataset.output || "" };
				}
			}
			return answers;
		}

		async submit(form, button) {
			button.disabled = true;
			try {
				const answers = await this.collect(form);
				const res = await call("submit_quiz", { name: this.name, answers: answers }, true);
				clearInterval(this.timer);
				this.showResult(form, res);
				if (res.passed) this.onPassed();
			} catch (e) {
				this.body.append(el("p", { class: "tcd-error" }, e.message));
				button.disabled = false;
			}
		}

		showResult(form, res) {
			const t = this.t;
			form.querySelectorAll("input, select, textarea, button").forEach((i) => (i.disabled = true));
			form.querySelector(".tcd-quiz-footer")?.remove();
			form.querySelector(".tcd-timer")?.remove();
			const byId = Object.fromEntries(res.results.map((r) => [r.id, r]));
			form.querySelectorAll("fieldset[data-id]").forEach((fs) => {
				const r = byId[fs.dataset.id];
				if (!r) return;
				if (r.pending) {
					fs.classList.add("tcd-pending");
					fs.append(el("div", { class: "tcd-feedback" }, t.waiting_review));
					return;
				}
				fs.classList.add(r.is_correct ? "tcd-correct" : "tcd-wrong");
				const note = el("div", { class: "tcd-feedback" }, r.is_correct ? t.correct : t.wrong);
				if (!r.is_correct && r.correct) {
					const labels = {};
					fs.querySelectorAll(".tcd-option").forEach((o) => (labels[o.querySelector("input").value] = o.querySelector("span").textContent));
					note.textContent += " - " + t.correct_answer + ": " + r.correct.map((n) => labels[String(n)]).join(", ");
				}
				fs.append(note);
				if (r.feedback) fs.append(el("p", { class: "tcd-muted" }, r.feedback));
				if (r.explanation) fs.append(el("p", { class: "tcd-muted" }, r.explanation));
			});
			const summary = el("div", { class: "tcd-quiz-result " + (res.passed ? "tcd-pass" : "tcd-fail") });
			const head = res.timed_out ? t.time_over : res.pending_review ? t.pending_review : res.passed ? t.passed : t.failed;
			summary.append(el("strong", {}, head), el("span", {}, " " + format(t.score, res.score, res.max_score, res.percentage)));
			if (!res.passed && !res.pending_review) {
				const again = el("button", { type: "button", class: "btn btn-default btn-sm" }, t.try_again);
				again.addEventListener("click", () => this.load());
				summary.append(" ", again);
			}
			form.append(summary);
			summary.scrollIntoView({ behavior: "smooth", block: "nearest" });
		}
	}

	if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
	else init();
})();
