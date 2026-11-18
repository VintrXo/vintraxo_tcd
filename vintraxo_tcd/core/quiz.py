"""Quiz definition checks, learner-safe payloads and server-side grading."""

import json
import random

import frappe
from frappe import _
from frappe.utils import flt

from vintraxo_tcd.core import progress

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
	if not doc.questions:
		frappe.throw(_("Add at least one question."))
	if not 0 < flt(doc.pass_percentage) <= 100:
		frappe.throw(_("Pass percentage must be between 1 and 100."))
	if (doc.max_attempts or 0) < 0:
		frappe.throw(_("Max attempts cannot be negative."))
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


def attempts_used(quiz: str, user: str) -> int:
	return frappe.db.count("TCD Quiz Submission", {"quiz": quiz, "user": user})


def learner_payload(quiz, user: str) -> dict:
	"""Questions without answers."""
	questions = [
		{
			"id": q.name,
			"question": q.question,
			"type": q.question_type,
			"options": options_of(q),
			"points": q.points,
		}
		for q in quiz.questions
	]
	if quiz.shuffle_questions:
		random.shuffle(questions)
	used = attempts_used(quiz.name, user)
	return {
		"name": quiz.name,
		"title": quiz.title,
		"content": quiz.content,
		"pass_percentage": quiz.pass_percentage,
		"max_attempts": quiz.max_attempts or 0,
		"attempts_used": used,
		"attempts_left": None if not quiz.max_attempts else max(quiz.max_attempts - used, 0),
		"passed": progress.has_passed(user, quiz.name),
		"questions": questions,
	}


def _normalize_answers(answers) -> dict[str, set[int]]:
	if isinstance(answers, str):
		try:
			answers = json.loads(answers)
		except ValueError:
			frappe.throw(_("Answers must be valid JSON."))
	if not isinstance(answers, dict):
		frappe.throw(_("Answers must be an object of question id -> option numbers."))
	out = {}
	for key, val in answers.items():
		vals = val if isinstance(val, list) else [val]
		try:
			out[str(key)] = {int(v) for v in vals if v not in (None, "")}
		except (TypeError, ValueError):
			frappe.throw(_("Answers must be option numbers."))
	return out


def grade(quiz, user: str, answers) -> dict:
	if not quiz.is_active:
		frappe.throw(_("This quiz is not active."))
	used = attempts_used(quiz.name, user)
	if quiz.max_attempts and used >= quiz.max_attempts:
		frappe.throw(_("No attempts left for this quiz."))

	given = _normalize_answers(answers)
	score = max_score = 0
	results = []
	for q in quiz.questions:
		correct = correct_of(q)
		chosen = given.get(q.name, set())
		ok = chosen == correct
		max_score += q.points or 1
		score += (q.points or 1) if ok else 0
		item = {"id": q.name, "chosen": sorted(chosen), "is_correct": ok}
		if quiz.show_answers_after_submit:
			item.update(correct=sorted(correct), explanation=q.explanation)
		results.append(item)

	percentage = flt(score * 100 / max_score, 2) if max_score else 0
	passed = percentage >= flt(quiz.pass_percentage)

	sub = frappe.get_doc(
		{
			"doctype": "TCD Quiz Submission",
			"quiz": quiz.name,
			"content": quiz.content,
			"user": user,
			"attempt": used + 1,
			"answers": json.dumps({k: sorted(v) for k, v in given.items()}),
			"score": score,
			"max_score": max_score,
			"percentage": percentage,
			"passed": int(passed),
			"results": json.dumps({r["id"]: r["is_correct"] for r in results}),
		}
	)
	sub.flags.from_quiz = True
	sub.insert(ignore_permissions=True)

	if passed and quiz.required_to_complete:
		progress.complete(user, quiz.content, from_quiz=True)
	from vintraxo_tcd.core import courses

	courses.on_content_changed(user, quiz.content)  # scores feed Minimum Score rules

	return {
		"submission": sub.name,
		"attempt": sub.attempt,
		"score": score,
		"max_score": max_score,
		"percentage": percentage,
		"passed": passed,
		"results": results,
	}
