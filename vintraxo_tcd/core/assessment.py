"""Assessment engine (PLAN Phase 4, ADR-0013).

An *item* is a plain dict describing one question, built either from an inline quiz row
(TCD Quiz Question) or from a bank question (TCD Question). Papers, payloads and grading all work
on items, so both sources behave the same.
"""

import random
import re

import frappe
from frappe import _
from frappe.utils import flt

from vintraxo_tcd.core.search import normalize_text

CHOICE = ("Single Choice", "Multiple Choice", "True False")
MANUAL_ALWAYS = ("Essay", "File")
TRUE_FALSE = ("True", "False")
BLANK = re.compile(r"_{3,}")


def _lines(text) -> list[str]:
	return [line.strip() for line in (text or "").splitlines() if line.strip()]


def options_of(item) -> list[str]:
	if item["type"] == "True False":
		return [_(o) for o in TRUE_FALSE]
	return _lines(item.get("options"))


def correct_of(item) -> set[int]:
	try:
		return {int(x) for x in str(item.get("correct_answers") or "").replace(" ", "").split(",") if x}
	except ValueError:
		frappe.throw(
			_("Question {0}: correct answers must be numbers like 1 or 1,3.").format(item.get("label"))
		)


def pairs_of(item) -> list[tuple[str, str]]:
	out = []
	for line in _lines(item.get("pairs")):
		if "=>" not in line:
			frappe.throw(_("Matching pairs must look like: left => right"))
		left, right = line.split("=>", 1)
		out.append((left.strip(), right.strip()))
	return out


def blanks_of(item) -> list[list[str]]:
	return [
		[alt.strip() for alt in line.split("|") if alt.strip()]
		for line in _lines(item.get("accepted_answers"))
	]


# ---------------------------------------------------------------- items


def item_from_inline(row) -> dict:
	return {
		"key": row.name,
		"source": "inline",
		"label": row.idx,
		"type": row.question_type,
		"question": row.question,
		"scenario": None,
		"options": row.options,
		"correct_answers": row.correct_answers,
		"points": flt(row.points) or 1,
		"explanation": row.explanation,
		"manual_review": 0,
		"rubric": [],
	}


def item_from_bank(q) -> dict:
	return {
		"key": q.name,
		"source": "bank",
		"label": (q.question or "")[:40],
		"type": q.question_type,
		"question": q.question,
		"scenario": q.scenario,
		"options": q.options,
		"correct_answers": q.correct_answers,
		"accepted_answers": q.accepted_answers,
		"pairs": q.pairs,
		"code_language": q.code_language,
		"starter_code": q.starter_code,
		"setup_code": q.setup_code,
		"expected_output": q.expected_output,
		"allowed_extensions": q.allowed_extensions,
		"points": flt(q.points) or 1,
		"explanation": q.explanation,
		"manual_review": int(q.manual_review or 0),
		"rubric": [{"criterion": r.criterion, "max_points": flt(r.max_points)} for r in q.rubric],
	}


def load_item(key: str, source: str, quiz=None) -> dict | None:
	if source == "bank":
		if not frappe.db.exists("TCD Question", key):
			return None
		return item_from_bank(frappe.get_doc("TCD Question", key))
	row = next((r for r in (quiz.questions if quiz else []) if r.name == key), None)
	return item_from_inline(row) if row else None


def is_manual(item) -> bool:
	t = item["type"]
	if t in MANUAL_ALWAYS:
		return True
	if t == "Short Answer" and not _lines(item.get("accepted_answers")):
		return True
	return bool(item.get("manual_review")) and t in ("Code", "SQL", "Short Answer")


# ---------------------------------------------------------------- validation of bank questions


def validate_question(doc):
	item = item_from_bank(doc)
	t = item["type"]
	if flt(doc.points) <= 0:
		frappe.throw(_("Points must be greater than zero."))
	if t in CHOICE:
		opts, correct = options_of(item), correct_of(item)
		if len(opts) < 2:
			frappe.throw(_("Add at least two options."))
		if not correct or not all(1 <= c <= len(opts) for c in correct):
			frappe.throw(_("Correct answers must be between 1 and {0}.").format(len(opts)))
		if t != "Multiple Choice" and len(correct) != 1:
			frappe.throw(_("Exactly one correct answer is allowed."))
		doc.correct_answers = ",".join(str(c) for c in sorted(correct))
	elif t == "Ordering" and len(options_of(item)) < 2:
		frappe.throw(_("Add at least two items in the correct order."))
	elif t == "Matching" and len(pairs_of(item)) < 2:
		frappe.throw(_("Add at least two pairs."))
	elif t == "Fill Blank":
		blanks = blanks_of(item)
		if not blanks:
			frappe.throw(_("Add one accepted answer line per blank."))
		marks = len(BLANK.findall(doc.question or ""))
		if marks and marks != len(blanks):
			frappe.throw(_("The question has {0} blanks but {1} answer lines.").format(marks, len(blanks)))
	elif t in ("Code", "SQL"):
		if t == "Code" and not doc.code_language:
			frappe.throw(_("Choose the code language."))
		if not (doc.expected_output or "").strip() and not doc.manual_review:
			frappe.throw(_("Add the expected output, or tick Requires Manual Review."))
	if is_manual(item) and doc.rubric and sum(r.max_points for r in doc.rubric) <= 0:
		frappe.throw(_("Rubric points must add up to more than zero."))


# ---------------------------------------------------------------- paper


def build_paper(quiz) -> list[dict]:
	"""Fix the questions (and option order) of one attempt."""
	refs = [{"key": r.name, "source": "inline"} for r in quiz.questions]
	seen = {r["key"] for r in refs}
	for row in quiz.get("bank_items") or []:
		if row.question:
			if row.question not in seen:
				refs.append({"key": row.question, "source": "bank"})
				seen.add(row.question)
			continue
		pool = [
			q
			for q in frappe.get_all(
				"TCD Question", filters={"category": row.category}, pluck="name", ignore_permissions=True
			)
			if q not in seen
		]
		for q in random.sample(pool, min(int(row.pick_count or 1), len(pool))):
			refs.append({"key": q, "source": "bank"})
			seen.add(q)
	if quiz.shuffle_questions:
		random.shuffle(refs)
	for ref in refs:
		item = load_item(ref["key"], ref["source"], quiz)
		if not item:
			continue
		n = (
			len(options_of(item))
			if item["type"] in (*CHOICE, "Ordering")
			else len(pairs_of(item))
			if item["type"] == "Matching"
			else 0
		)
		order = list(range(1, n + 1))
		if n and (quiz.shuffle_options or item["type"] in ("Ordering", "Matching")):
			random.shuffle(order)
		ref["order"] = order
	return refs


def payload(item, ref) -> dict:
	"""What the learner sees: never the answers."""
	t = item["type"]
	out = {
		"id": item["key"],
		"type": t,
		"question": item["question"],
		"scenario": item.get("scenario"),
		"points": item["points"],
		"manual": is_manual(item),
		"rubric": item.get("rubric") or [],
	}
	order = ref.get("order") or []
	if t in CHOICE:
		opts = options_of(item)
		out["options"] = [{"value": i, "label": opts[i - 1]} for i in (order or range(1, len(opts) + 1))]
	elif t == "Ordering":
		opts = options_of(item)
		out["items"] = [{"value": i, "label": opts[i - 1]} for i in order]
	elif t == "Matching":
		pairs = pairs_of(item)
		out["lefts"] = [p[0] for p in pairs]
		out["rights"] = [pairs[i - 1][1] for i in order]
	elif t == "Fill Blank":
		out["blanks"] = len(blanks_of(item))
	elif t in ("Code", "SQL"):
		out["language"] = "sql" if t == "SQL" else item.get("code_language")
		out["starter_code"] = item.get("starter_code") or ""
		out["setup_code"] = item.get("setup_code") or ""
	elif t == "File":
		out["allowed_extensions"] = item.get("allowed_extensions")
	return out


# ---------------------------------------------------------------- grading


def _norm_output(text) -> list[str]:
	return [line.rstrip() for line in str(text or "").replace("\r", "").strip().splitlines()]


def grade_item(item, answer) -> dict:
	"""Return {earned, max, correct, manual} for one answer. earned is None when manual."""
	t, pts = item["type"], item["points"]
	result = {"earned": 0.0, "max": pts, "correct": False, "manual": False}
	if is_manual(item):
		result.update(earned=None, manual=True)
		if t in ("Code", "SQL") and isinstance(answer, dict):
			result["auto_hint"] = _norm_output(answer.get("output")) == _norm_output(
				item.get("expected_output")
			)
		return result

	fraction = 0.0
	if t in CHOICE:
		chosen = answer if isinstance(answer, list) else [answer]
		try:
			chosen = {int(v) for v in chosen if v not in (None, "")}
		except (TypeError, ValueError):
			chosen = set()
		fraction = 1.0 if chosen == correct_of(item) else 0.0
	elif t == "Fill Blank":
		blanks = blanks_of(item)
		given = answer if isinstance(answer, list) else [answer]
		hits = sum(
			1
			for i, alts in enumerate(blanks)
			if i < len(given) and normalize_text(str(given[i] or "")) in {normalize_text(a) for a in alts}
		)
		fraction = hits / len(blanks) if blanks else 0
	elif t == "Matching":
		pairs = pairs_of(item)
		given = answer if isinstance(answer, dict) else {}
		hits = sum(
			1
			for i, (_l, right) in enumerate(pairs)
			if normalize_text(str(given.get(str(i), ""))) == normalize_text(right)
		)
		fraction = hits / len(pairs) if pairs else 0
	elif t == "Ordering":
		n = len(options_of(item))
		given = answer if isinstance(answer, list) else []
		try:
			given = [int(v) for v in given]
		except (TypeError, ValueError):
			given = []
		hits = sum(1 for pos, v in enumerate(given[:n], start=1) if v == pos)
		fraction = hits / n if n else 0
	elif t == "Short Answer":
		accepted = {normalize_text(a) for a in _lines(item.get("accepted_answers"))}
		fraction = 1.0 if normalize_text(str(answer or "")) in accepted else 0.0
	elif t in ("Code", "SQL"):
		output = answer.get("output") if isinstance(answer, dict) else None
		fraction = (
			1.0
			if output is not None and _norm_output(output) == _norm_output(item.get("expected_output"))
			else 0.0
		)
	result["earned"] = round(pts * fraction, 2)
	result["correct"] = fraction == 1.0
	return result


def review_points(item, review: dict) -> float:
	"""Points from a manual review: rubric scores when a rubric exists, else a single number."""
	rubric = item.get("rubric") or []
	if rubric:
		scores = review.get("rubric") or {}
		total = 0.0
		for r in rubric:
			value = flt(scores.get(r["criterion"]))
			if not 0 <= value <= r["max_points"]:
				frappe.throw(
					_("{0}: points must be between 0 and {1}.").format(r["criterion"], r["max_points"])
				)
			total += value
		max_total = sum(r["max_points"] for r in rubric)
		return round(item["points"] * total / max_total, 2) if max_total else 0.0
	value = flt(review.get("points"))
	if not 0 <= value <= item["points"]:
		frappe.throw(_("Points must be between 0 and {0}.").format(item["points"]))
	return value
