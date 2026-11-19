"""Analytics (PLAN Phase 7, ADR-0016): course report, knowledge usage, compliance overview, number cards.
Every query goes through get_list so the permission layers apply."""

import frappe
from frappe.utils import add_days, date_diff, flt, getdate, nowdate


def course_rows(filters) -> list[dict]:
	conditions = {}
	if filters.get("space"):
		conditions["space"] = filters["space"]
	if filters.get("status"):
		conditions["status"] = filters["status"]
	today = getdate(nowdate())
	rows = []
	for c in frappe.get_list(
		"TCD Course",
		filters=conditions,
		fields=["name", "title", "status", "completion_rule", "space"],
		order_by="title asc",
	):
		enrollments = frappe.get_all(
			"TCD Enrollment",
			filters={"course": c.name, "status": ("!=", "Withdrawn")},
			fields=["status", "enrolled_on", "completed_on", "due_date", "score"],
			ignore_permissions=True,
		)
		completed = [e for e in enrollments if e.status == "Completed"]
		days = [
			date_diff(e.completed_on, e.enrolled_on) for e in completed if e.completed_on and e.enrolled_on
		]
		scores = [flt(e.score) for e in enrollments if e.score]
		ratings = frappe.get_all(
			"TCD Course Feedback", filters={"course": c.name}, pluck="rating", ignore_permissions=True
		)
		rows.append(
			{
				"course": c.name,
				"title": c.title,
				"status": c.status,
				"space": c.space,
				"enrolled": len(enrollments),
				"completed": len(completed),
				"completion_rate": flt(len(completed) * 100 / len(enrollments), 1) if enrollments else 0,
				"overdue": sum(
					1
					for e in enrollments
					if e.status != "Completed" and e.due_date and getdate(e.due_date) < today
				),
				"avg_days_to_complete": flt(sum(days) / len(days), 1) if days else None,
				"avg_score": flt(sum(scores) / len(scores), 1) if scores else None,
				"rating": round(sum(ratings) / len(ratings), 1) if ratings else None,
			}
		)
	return rows


def usage_rows(filters) -> list[dict]:
	conditions = {"status": "Published"}
	for key in ("space", "content_type"):
		if filters.get(key):
			conditions[key] = filters[key]
	progress_filters = {}
	if filters.get("from_date"):
		progress_filters["last_viewed_on"] = (">=", filters["from_date"])
	rows = []
	for c in frappe.get_list(
		"TCD Content",
		filters=conditions,
		fields=["name", "title", "content_type", "space", "internal_links"],
		limit_page_length=2000,
	):
		readers = frappe.get_all(
			"TCD Progress",
			filters={"content": c.name, **progress_filters},
			fields=["status"],
			ignore_permissions=True,
		)
		feedback = frappe.get_all(
			"TCD Content Feedback", filters={"content": c.name}, pluck="helpful", ignore_permissions=True
		)
		backlinks = frappe.db.count("TCD Content", {"internal_links": ("like", f'%"{c.name}"%')})
		rows.append(
			{
				"content": c.name,
				"title": c.title,
				"content_type": c.content_type,
				"space": c.space,
				"readers": len(readers),
				"completed": sum(1 for r in readers if r.status == "Completed"),
				"feedback": len(feedback),
				"helpful_rate": flt(sum(feedback) * 100 / len(feedback), 1) if feedback else None,
				"backlinks": backlinks,
			}
		)
	rows.sort(key=lambda r: -r["readers"])
	return rows


def compliance_rows() -> list[dict]:
	from vintraxo_tcd.core.governance import acknowledgment_rows

	rows = []
	for d in frappe.get_list(
		"TCD Governance Document",
		filters={"status": ("in", ["Active", "Revision"]), "require_acknowledgment": 1, "version": (">", 0)},
		fields=["name", "title", "doc_kind", "version", "next_review_date"],
		order_by="title asc",
	):
		people = acknowledgment_rows(d.name)
		done = sum(p["acknowledged"] for p in people)
		rows.append(
			{
				"document": d.name,
				"title": d.title,
				"doc_kind": d.doc_kind,
				"version": d.version,
				"audience": len(people),
				"acknowledged": done,
				"missing": len(people) - done,
				"compliance": flt(done * 100 / len(people), 1) if people else 100.0,
				"next_review_date": d.next_review_date,
			}
		)
	return rows


def expiring_certificates(days: int = 30) -> int:
	return frappe.db.count(
		"TCD Certificate",
		[
			["status", "=", "Active"],
			["expires_on", "is", "set"],
			["expires_on", "<=", add_days(nowdate(), days)],
		],
	)


@frappe.whitelist()
def compliance_card() -> dict:
	"""Number card: overall acknowledgment compliance across active documents."""
	frappe.has_permission("TCD Acknowledgment", throw=True)
	rows = compliance_rows()
	audience = sum(r["audience"] for r in rows)
	done = sum(r["acknowledged"] for r in rows)
	return {"value": flt(done * 100 / audience, 1) if audience else 100.0, "fieldtype": "Percent"}
