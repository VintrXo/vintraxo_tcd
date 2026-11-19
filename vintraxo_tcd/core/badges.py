"""Badges (Phase 15, ADR-0023): awarded automatically when an event or a count is reached, or by an
admin (event "Manual"). Awarding never blocks the action that triggered it."""

import frappe
from frappe import _
from frappe.utils import now_datetime

COUNTERS = {
	"Lessons Completed": lambda u: frappe.db.count("TCD Progress", {"user": u, "status": "Completed"}),
	"Quizzes Passed": lambda u: len(
		set(frappe.get_all("TCD Quiz Submission", filters={"user": u, "passed": 1}, pluck="quiz"))
	),
	"Answers Accepted": lambda u: frappe.db.count(
		"TCD Discussion Post", {"user": u, "accepted": 1, "thread": ("is", "set")}
	),
	"Edits Accepted": lambda u: frappe.db.count("TCD Change Request", {"user": u, "status": "Accepted"}),
}


def check(user: str, event: str, course: str | None = None, learning_path: str | None = None):
	if not user or user in ("Guest", "Administrator"):
		return
	try:
		for badge in frappe.get_all(
			"TCD Badge",
			filters={"enabled": 1, "event": event},
			fields=["name", "threshold", "course", "learning_path"],
		):
			if frappe.db.exists("TCD Badge Award", {"user": user, "badge": badge.name}):
				continue
			if badge.course and badge.course != course:
				continue
			if badge.learning_path and badge.learning_path != learning_path:
				continue
			if event in COUNTERS and COUNTERS[event](user) < max(int(badge.threshold or 1), 1):
				continue
			award(user, badge.name, _(event))
	except Exception:
		frappe.log_error(title=f"TCD badges: {event} for {user}")


def award(user: str, badge: str, reason: str = ""):
	if frappe.db.exists("TCD Badge Award", {"user": user, "badge": badge}):
		return None
	doc = frappe.get_doc(
		{
			"doctype": "TCD Badge Award",
			"user": user,
			"badge": badge,
			"awarded_on": now_datetime(),
			"reason": reason,
		}
	).insert(ignore_permissions=True)
	from vintraxo_tcd.core import notify

	notify._send([user], _("You earned the badge: {0}").format(badge), "TCD Badge Award", doc.name)
	return doc


def validate_award(doc):
	doc.awarded_on = doc.awarded_on or now_datetime()
	if frappe.db.exists("TCD Badge Award", {"user": doc.user, "badge": doc.badge, "name": ("!=", doc.name)}):
		frappe.throw(_("{0} already has this badge.").format(frappe.bold(doc.user)))


def mine(user: str) -> list[dict]:
	out = []
	for a in frappe.get_all(
		"TCD Badge Award", filters={"user": user}, fields=["badge", "awarded_on"], order_by="awarded_on desc"
	):
		b = frappe.db.get_value("TCD Badge", a.badge, ["image", "description"], as_dict=True) or {}
		out.append(
			{
				"badge": a.badge,
				"image": b.get("image"),
				"description": b.get("description"),
				"awarded_on": a.awarded_on,
			}
		)
	return out
