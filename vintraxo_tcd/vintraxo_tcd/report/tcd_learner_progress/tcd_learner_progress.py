"""Learner progress per content item, with best quiz score. Permission-aware (get_list)."""

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	rows = get_rows(filters)
	return columns(), rows, None, chart(rows), summary(rows)


def columns():
	return [
		{"fieldname": "user", "label": _("Learner"), "fieldtype": "Link", "options": "User", "width": 200},
		{"fieldname": "full_name", "label": _("Name"), "fieldtype": "Data", "width": 160},
		{
			"fieldname": "content",
			"label": _("Content"),
			"fieldtype": "Link",
			"options": "TCD Content",
			"width": 220,
		},
		{"fieldname": "content_type", "label": _("Type"), "fieldtype": "Data", "width": 90},
		{
			"fieldname": "space",
			"label": _("Space"),
			"fieldtype": "Link",
			"options": "TCD Space",
			"width": 140,
		},
		{"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 110},
		{"fieldname": "percent", "label": _("Percent"), "fieldtype": "Percent", "width": 90},
		{"fieldname": "best_score", "label": _("Best Quiz Score"), "fieldtype": "Percent", "width": 120},
		{"fieldname": "quiz_attempts", "label": _("Quiz Attempts"), "fieldtype": "Int", "width": 110},
		{"fieldname": "started_on", "label": _("Started On"), "fieldtype": "Datetime", "width": 150},
		{"fieldname": "last_viewed_on", "label": _("Last Viewed On"), "fieldtype": "Datetime", "width": 150},
		{"fieldname": "completed_on", "label": _("Completed On"), "fieldtype": "Datetime", "width": 150},
	]


def get_rows(filters) -> list[dict]:
	conditions = {}
	for key in ("space", "content", "user", "status", "content_type"):
		if filters.get(key):
			conditions[key] = filters[key]
	rows = frappe.get_list(
		"TCD Progress",
		filters=conditions,
		fields=[
			"user",
			"content",
			"content_type",
			"space",
			"status",
			"percent",
			"started_on",
			"last_viewed_on",
			"completed_on",
		],
		order_by="last_viewed_on desc",
		limit_page_length=5000,
	)
	if not rows:
		return []

	names = dict(
		frappe.get_all(
			"User",
			filters={"name": ("in", list({r.user for r in rows}))},
			fields=["name", "full_name"],
			as_list=True,
		)
	)
	quiz = {}
	for sub in frappe.get_list(
		"TCD Quiz Submission",
		filters={"content": ("in", list({r.content for r in rows}))},
		fields=["user", "content", "percentage"],
		limit_page_length=50000,
	):
		best, count = quiz.get((sub.user, sub.content), (0.0, 0))
		quiz[(sub.user, sub.content)] = (max(best, flt(sub.percentage)), count + 1)

	for r in rows:
		r.full_name = names.get(r.user)
		best, count = quiz.get((r.user, r.content), (None, 0))
		r.best_score, r.quiz_attempts = best, count
	return rows


def chart(rows):
	if not rows:
		return None
	statuses = ["In Progress", "Completed"]
	return {
		"data": {
			"labels": [_(s, context="TCD") for s in statuses],
			"datasets": [
				{"name": _("Learners"), "values": [sum(r.status == s for r in rows) for s in statuses]}
			],
		},
		"type": "donut",
		"height": 220,
	}


def summary(rows):
	learners = len({r.user for r in rows})
	completed = sum(r.status == "Completed" for r in rows)
	rate = flt(completed * 100 / len(rows), 1) if rows else 0
	return [
		{"label": _("Learners"), "value": learners, "datatype": "Int", "indicator": "Blue"},
		{"label": _("Progress Records"), "value": len(rows), "datatype": "Int"},
		{"label": _("Completed", context="TCD"), "value": completed, "datatype": "Int", "indicator": "Green"},
		{"label": _("Completion Rate"), "value": rate, "datatype": "Percent", "indicator": "Green"},
	]
