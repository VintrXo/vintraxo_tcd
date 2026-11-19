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

	function init() {
		initEnroll();
		const t0 = labels();
		initAssignment(t0);
		initRating(t0);
		initHelpful(t0);
		initApprove();
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

		async load() {
			try {
				this.quiz = await call("get_quiz", { name: this.name });
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
			const form = el("form", { class: "tcd-quiz-form", novalidate: "" });
			q.questions.forEach((question, i) => {
				const fs = el("fieldset", { class: "tcd-question", "data-id": question.id });
				fs.append(el("legend", {}, i + 1 + ". " + question.question));
				const multiple = question.type === "Multiple Choice";
				question.options.forEach((opt, j) => {
					const label = el("label", { class: "tcd-option" });
					const input = el("input", {
						type: multiple ? "checkbox" : "radio",
						name: "q-" + question.id,
						value: String(j + 1),
					});
					label.append(input, el("span", {}, opt));
					fs.append(label);
				});
				form.append(fs);
			});

			const footer = el("div", { class: "tcd-quiz-footer" });
			const submit = el("button", { type: "submit", class: "btn btn-primary" }, this.t.submit || "Submit");
			const info = el("span", { class: "tcd-muted" }, this.attemptsText());
			if (q.attempts_left === 0) submit.disabled = true;
			footer.append(submit, info);
			form.append(footer);

			if (q.passed) form.prepend(el("p", { class: "tcd-status tcd-status-completed" }, this.t.passed || "Passed"));

			form.addEventListener("submit", (e) => {
				e.preventDefault();
				this.submit(form, submit);
			});
			this.body.replaceChildren(form);
		}

		async submit(form, button) {
			const answers = {};
			form.querySelectorAll("fieldset[data-id]").forEach((fs) => {
				answers[fs.dataset.id] = Array.from(fs.querySelectorAll("input:checked")).map((i) => Number(i.value));
			});
			button.disabled = true;
			try {
				const res = await call("submit_quiz", { name: this.name, answers: answers }, true);
				this.showResult(form, res);
				if (res.passed) this.onPassed();
			} catch (e) {
				this.body.append(el("p", { class: "tcd-error" }, e.message));
				button.disabled = false;
			}
		}

		showResult(form, res) {
			const t = this.t;
			form.querySelectorAll("input").forEach((i) => (i.disabled = true));
			form.querySelector(".tcd-quiz-footer").remove();
			const byId = Object.fromEntries(res.results.map((r) => [r.id, r]));

			form.querySelectorAll("fieldset[data-id]").forEach((fs) => {
				const r = byId[fs.dataset.id];
				if (!r) return;
				fs.classList.add(r.is_correct ? "tcd-correct" : "tcd-wrong");
				const note = el("div", { class: "tcd-feedback" }, r.is_correct ? t.correct : t.wrong);
				if (!r.is_correct && r.correct) {
					const options = Array.from(fs.querySelectorAll(".tcd-option span")).map((s) => s.textContent);
					note.textContent += " - " + t.correct_answer + ": " + r.correct.map((n) => options[n - 1]).join(", ");
				}
				fs.append(note);
				if (r.explanation) fs.append(el("p", { class: "tcd-muted" }, r.explanation));
			});

			const summary = el("div", { class: "tcd-quiz-result " + (res.passed ? "tcd-pass" : "tcd-fail") });
			summary.append(
				el("strong", {}, res.passed ? t.passed : t.failed),
				el("span", {}, " " + format(t.score, res.score, res.max_score, res.percentage))
			);
			this.quiz.attempts_used += 1;
			if (this.quiz.attempts_left !== null && this.quiz.attempts_left !== undefined) this.quiz.attempts_left -= 1;
			if (!res.passed && this.quiz.attempts_left !== 0) {
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
