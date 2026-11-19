"""Knowledge freshness (Phase 12, ADR-0020): every published page has an owner and a review cycle.
Owners get a reminder before the review date; readers see a notice when a page is overdue."""

import frappe
from frappe import _
from frappe.utils import add_days, add_months, getdate, nowdate

DEFAULT_MONTHS = 12


def cycle_months(doc) -> int:
	"""Months between reviews: none when the page skips reviews, its own cycle when set (> 0), else the
	default in Learning Settings (0 there turns reviews off)."""
	if doc.get("skip_review"):
		return 0
	if int(doc.get("review_cycle_months") or 0) > 0:
		return int(doc.review_cycle_months)
	return int(frappe.db.get_single_value("TCD Settings", "default_review_months") or 0)


def schedule(doc, reviewed_on=None):
	reviewed_on = getdate(reviewed_on or nowdate())
	doc.last_reviewed_on = reviewed_on
	months = cycle_months(doc)
	doc.next_review_date = add_months(reviewed_on, months) if months else None


def on_validate(doc):
	"""Called from TCD Content.validate."""
	doc.content_owner = doc.content_owner or doc.owner or frappe.session.user
	before = doc.get_doc_before_save()
	just_published = doc.status == "Published" and (not before or before.status != "Published")
	if just_published:
		schedule(doc)  # publishing counts as a review
	elif (
		doc.status == "Published"
		and before
		and (
			int(before.review_cycle_months or 0) != int(doc.review_cycle_months or 0)
			or bool(before.skip_review) != bool(doc.skip_review)
		)
	):
		schedule(doc, doc.last_reviewed_on)
	elif doc.status in ("Draft", "Archived"):
		doc.next_review_date = None


def is_overdue(doc) -> bool:
	return bool(doc.get("next_review_date")) and getdate(doc.next_review_date) < getdate(nowdate())


def confirm_review(name: str):
	"""The owner or a staff member confirms the page is still accurate (no republish needed)."""
	doc = frappe.get_doc("TCD Content", name)
	doc.check_permission("write")
	if doc.status != "Published":
		frappe.throw(_("Only published pages have a review cycle."))
	schedule(doc)
	doc.db_set({"last_reviewed_on": doc.last_reviewed_on, "next_review_date": doc.next_review_date})
	doc.add_comment("Info", _("Reviewed: still accurate."))
	return {"last_reviewed_on": doc.last_reviewed_on, "next_review_date": doc.next_review_date}


def daily():
	"""Open one review ToDo per page and date for its owner, a week before the review date."""
	today = getdate(nowdate())
	for row in frappe.get_all(
		"TCD Content",
		# "is set" matters: Frappe compares NULL dates as a very old date
		filters=[
			["status", "=", "Published"],
			["next_review_date", "is", "set"],
			["next_review_date", "<=", add_days(today, 7)],
			["content_owner", "is", "set"],
		],
		fields=["name", "title", "content_owner", "next_review_date"],
	):
		description = _("Review this page by {0}: {1}").format(row.next_review_date, row.title)
		if frappe.db.exists(
			"ToDo",
			{
				"reference_type": "TCD Content",
				"reference_name": row.name,
				"allocated_to": row.content_owner,
				"description": description,
			},
		):
			continue
		frappe.get_doc(
			{
				"doctype": "ToDo",
				"allocated_to": row.content_owner,
				"reference_type": "TCD Content",
				"reference_name": row.name,
				"description": description,
				"date": row.next_review_date,
				"priority": "Medium",
			}
		).insert(ignore_permissions=True)


def rows(filters) -> list[dict]:
	today = getdate(nowdate())
	conditions = [["status", "=", "Published"]]
	if filters.get("space"):
		conditions.append(["space", "=", filters["space"]])
	if filters.get("only_overdue"):
		conditions += [["next_review_date", "is", "set"], ["next_review_date", "<", today]]
	out = []
	for r in frappe.get_list(
		"TCD Content",
		filters=conditions,
		fields=[
			"name",
			"title",
			"space",
			"content_type",
			"content_owner",
			"last_reviewed_on",
			"next_review_date",
		],
		order_by="next_review_date asc",
		limit_page_length=0,
	):
		r["days_overdue"] = max((today - getdate(r.next_review_date)).days, 0) if r.next_review_date else 0
		out.append(r)
	return out
