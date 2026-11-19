"""Per-question results for one quiz: where learners struggle. Permission-aware."""

import json
from collections import Counter

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not filters.quiz:
		return columns(), [], _("Select a quiz."), None, []
	quiz = frappe.get_doc("TCD Quiz", filters.quiz)
	quiz.check_permission("read")
	submissions = get_submissions(filters)
	rows = question_rows(quiz, submissions)
	return columns(), rows, None, chart(rows), summary(submissions)


def columns():
	return [
		{"fieldname": "idx", "label": "#", "fieldtype": "Int", "width": 50},
		{"fieldname": "question", "label": _("Question"), "fieldtype": "Data", "width": 320},
		{"fieldname": "question_type", "label": _("Type"), "fieldtype": "Data", "width": 120},
		{"fieldname": "answered", "label": _("Answered"), "fieldtype": "Int", "width": 100},
		{"fieldname": "correct", "label": _("Correct"), "fieldtype": "Int", "width": 90},
		{"fieldname": "correct_rate", "label": _("Correct %"), "fieldtype": "Percent", "width": 100},
		{
			"fieldname": "common_wrong",
			"label": _("Most Common Wrong Answer"),
			"fieldtype": "Data",
			"width": 240,
		},
	]


def get_submissions(filters):
	conditions = {"quiz": filters.quiz, "status": ("!=", "In Progress")}
	if filters.from_date and filters.to_date:
		conditions["creation"] = ("between", [filters.from_date, filters.to_date])
	return frappe.get_list(
		"TCD Quiz Submission",
		filters=conditions,
		fields=["user", "attempt", "percentage", "passed", "answers", "results", "paper", "status"],
		limit_page_length=50000,
	)


def _load(value) -> dict:
	try:
		return json.loads(value or "{}") or {}
	except ValueError:
		return {}


def _as_list(value):
	if value is None or value == "":
		return []
	return value if isinstance(value, list) else [value]


def question_rows(quiz, submissions):
	from vintraxo_tcd.core import assessment

	keys, items = [], {}
	for q in quiz.questions:
		keys.append(q.name)
		items[q.name] = assessment.item_from_inline(q)
	for sub in submissions:
		for ref in _load(sub.get("paper")) or []:
			if ref["key"] not in items:
				item = assessment.load_item(ref["key"], ref["source"], quiz)
				if item:
					keys.append(ref["key"])
					items[ref["key"]] = item
	rows = []
	for idx, key in enumerate(keys, start=1):
		item = items[key]
		choice = item["type"] in assessment.CHOICE
		options = assessment.options_of(item) if choice else []
		answered = correct = 0
		wrong = Counter()
		for sub in submissions:
			given = _load(sub.answers)
			if key not in given or given[key] in (None, "", [], {}):
				continue
			graded = _load(sub.results)
			if key not in graded:
				continue  # pending manual review
			answered += 1
			if graded[key]:
				correct += 1
			elif choice:
				wrong[tuple(sorted(int(v) for v in _as_list(given[key]) if str(v).isdigit()))] += 1
		common = ""
		if wrong:
			choice_key = wrong.most_common(1)[0][0]
			common = ", ".join(options[i - 1] for i in choice_key if 0 < i <= len(options))
		rows.append(
			{
				"idx": idx,
				"question": item["question"],
				"question_type": _(item["type"]),
				"answered": answered,
				"correct": correct,
				"correct_rate": flt(correct * 100 / answered, 1) if answered else None,
				"common_wrong": common,
			}
		)
	return rows


def chart(rows):
	if not any(r["answered"] for r in rows):
		return None
	return {
		"data": {
			"labels": [f"#{r['idx']}" for r in rows],
			"datasets": [{"name": _("Correct %"), "values": [r["correct_rate"] or 0 for r in rows]}],
		},
		"type": "bar",
		"height": 220,
		"colors": ["#16a34a"],
	}


def summary(submissions):
	learners = {s.user for s in submissions}
	passed_learners = {s.user for s in submissions if s.passed}
	avg = flt(sum(flt(s.percentage) for s in submissions) / len(submissions), 1) if submissions else 0
	return [
		{"label": _("Attempts"), "value": len(submissions), "datatype": "Int", "indicator": "Blue"},
		{"label": _("Learners"), "value": len(learners), "datatype": "Int"},
		{
			"label": _("Learners Passed"),
			"value": flt(len(passed_learners) * 100 / len(learners), 1) if learners else 0,
			"datatype": "Percent",
			"indicator": "Green",
		},
		{"label": _("Average Score"), "value": avg, "datatype": "Percent"},
	]
