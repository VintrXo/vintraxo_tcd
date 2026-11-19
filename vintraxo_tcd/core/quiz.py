"""Quiz definition checks, learner-safe payloads and server-side grading."""

import json

import frappe
from frappe import _
from frappe.utils import add_to_date, flt, get_datetime, now_datetime

from vintraxo_tcd.core import assessment, progress

GRACE_SECONDS = 60

TRUE_FALSE = ("True", "False")


def options_of(q) -> list[str]:
	if q.question_type == "True False":
		return [_(o) for o in TRUE_FALSE]
	return [line.strip() for line in (q.options or "").splitlines() if line.strip()]


def correct_of(q) -> set[int]:
	try:
		return {int(x) for x in str(q.correct_answers or "").replace(" ", "").split(",") if x}
	except ValueError:
		frappe.throw(_("Question {0}: correct answers must be numbers like 1 or 1,3.").format(q.idx))


def validate_quiz(doc):
	if not doc.questions and not doc.get("bank_items"):
		frappe.throw(_("Add at least one question."))
	if not 0 < flt(doc.pass_percentage) <= 100:
		frappe.throw(_("Pass percentage must be between 1 and 100."))
	if (doc.max_attempts or 0) < 0:
		frappe.throw(_("Max attempts cannot be negative."))
	if (doc.time_limit_minutes or 0) < 0:
		frappe.throw(_("Time limit cannot be negative."))
	for q in doc.questions:
		opts = options_of(q)
		correct = correct_of(q)
		if len(opts) < 2:
			frappe.throw(_("Question {0}: add at least two options.").format(q.idx))
		if not correct or not all(1 <= c <= len(opts) for c in correct):
			frappe.throw(
				_("Question {0}: correct answers must be between 1 and {1}.").format(q.idx, len(opts))
			)
		if q.question_type != "Multiple Choice" and len(correct) != 1:
			frappe.throw(_("Question {0}: exactly one correct answer is allowed.").format(q.idx))
		if (q.points or 0) < 1:
			q.points = 1
		q.correct_answers = ",".join(str(c) for c in sorted(correct))
	for row in doc.get("bank_items") or []:
		if bool(row.question) == bool(row.category):
			frappe.throw(_("Bank row {0}: choose a question or a category (not both).").format(row.idx))
		if row.category:
			row.pick_count = max(int(row.pick_count or 1), 1)
			available = frappe.db.count("TCD Question", {"category": row.category})
			if available < row.pick_count:
				frappe.throw(
					_("Bank row {0}: category {1} has only {2} questions.").format(
						row.idx, frappe.bold(row.category), available
					)
				)


def attempts_used(quiz: str, user: str) -> int:
	return frappe.db.count("TCD Quiz Submission", {"quiz": quiz, "user": user})


def requires_start(quiz) -> bool:
	"""Timed quizzes and random bank picks need a fixed paper before the questions are shown."""
	return bool(quiz.time_limit_minutes) or any(r.category for r in quiz.get("bank_items") or [])


def open_attempt(quiz, user: str):
	name = frappe.db.get_value(
		"TCD Quiz Submission",
		{"quiz": quiz.name, "user": user, "status": "In Progress"},
		order_by="creation desc",
	)
	return frappe.get_doc("TCD Quiz Submission", name) if name else None


def _paper(sub) -> list:
	return json.loads(sub.paper) if isinstance(sub.paper, str) else (sub.paper or [])


def _questions(quiz, paper) -> list:
	out = []
	for ref in paper:
		item = assessment.load_item(ref["key"], ref["source"], quiz)
		if item:
			out.append(assessment.payload(item, ref))
	return out


def learner_payload(quiz, user: str) -> dict:
	"""Quiz meta + questions without answers (from the open attempt when there is one)."""
	used = attempts_used(quiz.name, user)
	attempt = open_attempt(quiz, user)
	if attempt:
		questions = _questions(quiz, _paper(attempt))
	elif requires_start(quiz):
		questions = []
	else:
		questions = _questions(quiz, assessment.build_paper(quiz))
	return {
		"name": quiz.name,
		"title": quiz.title,
		"content": quiz.content,
		"pass_percentage": quiz.pass_percentage,
		"max_attempts": quiz.max_attempts or 0,
		"attempts_used": used,
		"attempts_left": None if not quiz.max_attempts else max(quiz.max_attempts - used, 0),
		"passed": progress.has_passed(user, quiz.name),
		"time_limit_minutes": quiz.time_limit_minutes or 0,
		"requires_start": requires_start(quiz) and not attempt,
		"attempt": attempt
		and {
			"name": attempt.name,
			"deadline": attempt.deadline,
			"seconds_left": max(0, int((get_datetime(attempt.deadline) - now_datetime()).total_seconds()))
			if attempt.deadline
			else None,
		},
		"pending_review": bool(
			frappe.db.exists(
				"TCD Quiz Submission", {"quiz": quiz.name, "user": user, "status": "Pending Review"}
			)
		),
		"questions": questions,
	}


def _check_attempts(quiz, user: str):
	if not quiz.is_active:
		frappe.throw(_("This quiz is not active."))
	if quiz.max_attempts and attempts_used(quiz.name, user) >= quiz.max_attempts:
		frappe.throw(_("No attempts left for this quiz."))


def start(quiz, user: str):
	"""Open (or resume) an attempt with a fixed paper and deadline."""
	attempt = open_attempt(quiz, user)
	if attempt and not _expired(attempt):
		return attempt
	if attempt:
		_finish(quiz, attempt, {}, timed_out=True)
	_check_attempts(quiz, user)
	started = now_datetime()
	sub = frappe.get_doc(
		{
			"doctype": "TCD Quiz Submission",
			"quiz": quiz.name,
			"content": quiz.content,
			"user": user,
			"attempt": attempts_used(quiz.name, user) + 1,
			"status": "In Progress",
			"started_on": started,
			"deadline": add_to_date(started, minutes=quiz.time_limit_minutes)
			if quiz.time_limit_minutes
			else None,
			"paper": json.dumps(assessment.build_paper(quiz)),
		}
	)
	sub.flags.from_quiz = True
	sub.insert(ignore_permissions=True)
	return sub


def _expired(sub) -> bool:
	return bool(sub.deadline) and now_datetime() > add_to_date(
		get_datetime(sub.deadline), seconds=GRACE_SECONDS
	)


def _parse_answers(answers) -> dict:
	if isinstance(answers, str):
		try:
			answers = json.loads(answers)
		except ValueError:
			frappe.throw(_("Answers must be valid JSON."))
	if not isinstance(answers, dict):
		frappe.throw(_("Answers must be an object of question id -> answer."))
	if len(json.dumps(answers)) > 200000:
		frappe.throw(_("The answers are too long."))
	return {str(k): v for k, v in answers.items()}


def grade(quiz, user: str, answers) -> dict:
	given = _parse_answers(answers)
	attempt = open_attempt(quiz, user)
	if attempt and _expired(attempt):
		result = _finish(quiz, attempt, {}, timed_out=True)
		result["timed_out"] = True
		return result
	if not attempt:
		if requires_start(quiz):
			frappe.throw(_("Start the quiz first."))
		_check_attempts(quiz, user)
		attempt = frappe.get_doc(
			{
				"doctype": "TCD Quiz Submission",
				"quiz": quiz.name,
				"content": quiz.content,
				"user": user,
				"attempt": attempts_used(quiz.name, user) + 1,
				"status": "In Progress",
				"started_on": now_datetime(),
				"paper": json.dumps(assessment.build_paper(quiz)),
			}
		)
	return _finish(quiz, attempt, given)


def _grade_paper(quiz, sub, given: dict, review: dict | None = None):
	review = review or {}
	score = max_score = 0.0
	results, flags, pending = [], {}, []
	for ref in _paper(sub):
		item = assessment.load_item(ref["key"], ref["source"], quiz)
		if not item:
			continue
		r = assessment.grade_item(item, given.get(item["key"]))
		if r["manual"]:
			if item["key"] in review:
				r["earned"] = assessment.review_points(item, review[item["key"]])
				r["correct"] = r["earned"] >= item["points"]
				r["manual"] = False
			else:
				pending.append(item["key"])
		max_score += r["max"]
		score += r["earned"] or 0
		entry = {
			"id": item["key"],
			"type": item["type"],
			"is_correct": r["correct"],
			"pending": item["key"] in pending,
		}
		chosen = given.get(item["key"])
		if item["type"] in assessment.CHOICE:
			values = chosen if isinstance(chosen, list) else [chosen]
			entry["chosen"] = sorted(int(v) for v in values if str(v).lstrip("-").isdigit())
		if quiz.show_answers_after_submit:
			if item["type"] in assessment.CHOICE:
				entry["correct"] = sorted(assessment.correct_of(item))
			entry["explanation"] = item.get("explanation")
			if item["key"] in review and review[item["key"]].get("feedback"):
				entry["feedback"] = review[item["key"]]["feedback"]
		results.append(entry)
		if not entry["pending"]:
			flags[item["key"]] = r["correct"]
	return round(score, 2), round(max_score, 2), results, flags, pending


def _finish(quiz, sub, given: dict, timed_out: bool = False) -> dict:
	score, max_score, results, flags, pending = _grade_paper(quiz, sub, given)
	percentage = flt(score * 100 / max_score, 2) if max_score else 0
	passed = not pending and percentage >= flt(quiz.pass_percentage)
	sub.update(
		{
			"answers": json.dumps(given, ensure_ascii=False),
			"score": score,
			"max_score": max_score,
			"percentage": percentage,
			"passed": int(passed),
			"results": json.dumps(flags),
			"status": "Pending Review" if pending else "Graded",
			"submitted_on": now_datetime(),
		}
	)
	sub.flags.from_quiz = True
	sub.save(ignore_permissions=True)
	_after_grade(quiz, sub)
	if pending:
		from vintraxo_tcd.core import notify

		notify.quiz_pending_review(sub)
	return {
		"submission": sub.name,
		"attempt": sub.attempt,
		"score": score,
		"max_score": max_score,
		"percentage": percentage,
		"passed": passed,
		"pending_review": bool(pending),
		"timed_out": timed_out,
		"results": results,
	}


def _after_grade(quiz, sub):
	if sub.passed and quiz.required_to_complete:
		progress.complete(sub.user, quiz.content, from_quiz=True)
	from vintraxo_tcd.core import courses

	courses.on_content_changed(sub.user, quiz.content)  # scores feed Minimum Score rules


def review(sub, reviews, reviewer: str) -> dict:
	"""Manual grading of the pending items of a submission."""
	if sub.status != "Pending Review":
		frappe.throw(_("Only submissions waiting for review can be reviewed."))
	quiz = frappe.get_doc("TCD Quiz", sub.quiz)
	if isinstance(reviews, str):
		reviews = json.loads(reviews)
	stored = json.loads(sub.review) if isinstance(sub.review, str) and sub.review else (sub.review or {})
	stored.update({str(k): v for k, v in (reviews or {}).items()})
	given = json.loads(sub.answers or "{}")
	score, max_score, _results, flags, pending = _grade_paper(quiz, sub, given, stored)
	percentage = flt(score * 100 / max_score, 2) if max_score else 0
	values = {
		"review": json.dumps(stored, ensure_ascii=False),
		"score": score,
		"percentage": percentage,
		"results": json.dumps(flags),
	}
	if not pending:
		values.update(
			status="Graded",
			passed=int(percentage >= flt(quiz.pass_percentage)),
			graded_by=reviewer,
			graded_on=now_datetime(),
		)
	sub.update(values)
	sub.flags.from_quiz = True
	sub.save(ignore_permissions=True)
	if not pending:
		_after_grade(quiz, sub)
	return {
		"status": sub.status,
		"score": score,
		"percentage": percentage,
		"passed": bool(sub.passed),
		"pending": pending,
	}
