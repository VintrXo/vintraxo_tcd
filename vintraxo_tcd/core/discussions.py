"""Lesson discussions (Phase 12, ADR-0020): questions and replies under a page, plain text only.
Readers of the page can post; the page owner, instructors of courses using it, reviewers and admins
moderate (answer, accept, hide). Posts are created only through this service."""

import frappe
from frappe import _
from frappe.utils import add_to_date, now_datetime, pretty_date

from vintraxo_tcd.core.permissions import can_access_content, instructed, is_admin

DOCTYPE = "TCD Discussion Post"
MAX_CHARS = 2000
POSTS_PER_HOUR = 10


def enabled() -> bool:
	return bool(frappe.db.get_single_value("TCD Settings", "enable_discussions"))


def _content(name: str, user: str):
	doc = frappe.get_doc("TCD Content", name)
	if not can_access_content(doc, user) or (doc.status != "Published" and not can_moderate(doc, user)):
		raise frappe.DoesNotExistError
	return doc


def can_moderate(content, user: str) -> bool:
	if user == "Guest":
		return False
	if is_admin(user) or "TCD Content Reviewer" in frappe.get_roles(user):
		return True
	if content.get("content_owner") == user:
		return True
	from vintraxo_tcd.core.courses import courses_with_content

	return bool(set(courses_with_content(content.name)) & instructed(user, "TCD Course"))


def _name(user: str) -> str:
	return frappe.db.get_value("User", user, "full_name") or user


def _post_dict(p, user: str) -> dict:
	return {
		"name": p.name,
		"author": _name(p.user),
		"mine": p.user == user,
		"body": p.body,
		"when": pretty_date(p.creation),
		"staff": bool(p.is_staff_answer),
		"accepted": bool(p.accepted),
		"hidden": bool(p.hidden),
		"status": p.status,
	}


def list_for(content: str, user: str) -> dict:
	doc = _content(content, user)
	moderator = can_moderate(doc, user)
	fields = ["name", "user", "body", "creation", "is_staff_answer", "accepted", "hidden", "status", "thread"]
	filters = {"content": doc.name}
	if not moderator:
		filters["hidden"] = 0
	posts = frappe.get_all(DOCTYPE, filters=filters, fields=fields, order_by="creation asc")
	threads = [p for p in posts if not p.thread]
	threads.reverse()  # newest question first, replies oldest first
	out = []
	for t in threads:
		item = _post_dict(t, user)
		item["replies"] = [_post_dict(r, user) for r in posts if r.thread == t.name]
		out.append(item)
	return {"enabled": enabled(), "can_moderate": moderator, "threads": out}


def post(content: str, body: str, user: str, thread: str | None = None) -> dict:
	if user == "Guest":
		raise frappe.PermissionError
	if not enabled():
		frappe.throw(_("Discussions are turned off."))
	doc = _content(content, user)
	body = (body or "").strip()
	if len(body) < 2:
		frappe.throw(_("Write your question or reply."))
	if len(body) > MAX_CHARS:
		frappe.throw(_("Keep it under {0} characters.").format(MAX_CHARS))
	recent = frappe.db.count(
		DOCTYPE, {"user": user, "creation": (">=", add_to_date(now_datetime(), hours=-1))}
	)
	if recent >= POSTS_PER_HOUR:
		frappe.throw(_("You posted a lot in the last hour. Try again later."))
	parent = None
	if thread:
		parent = frappe.db.get_value(
			DOCTYPE, thread, ["name", "content", "thread", "hidden", "user"], as_dict=True
		)
		if not parent or parent.content != doc.name or parent.thread or parent.hidden:
			frappe.throw(_("This question is not available."))
	staff = can_moderate(doc, user)
	new = frappe.get_doc(
		{
			"doctype": DOCTYPE,
			"content": doc.name,
			"thread": parent.name if parent else None,
			"user": user,
			"body": body,
			"is_staff_answer": int(bool(parent and staff)),
			"status": None if parent else "Open",
		}
	)
	new.flags.from_service = True
	new.insert(ignore_permissions=True)
	_notify(doc, new, parent, user)
	if parent and staff:
		frappe.db.set_value(DOCTYPE, parent.name, "status", "Answered")
	return _post_dict(new, user)


def _notify(content, new, parent, user: str):
	from vintraxo_tcd.core import notify
	from vintraxo_tcd.core.courses import courses_with_content

	if parent:
		users = {parent.user}
		subject = _("New reply to your question on {0}").format(content.title)
	else:
		users = {content.get("content_owner")}
		for course in courses_with_content(content.name):
			users |= set(notify.course_instructors(course))
		subject = _("New question on {0}").format(content.title)
	notify._send([u for u in users if u and u != user], subject, DOCTYPE, new.name, new.body[:200])


def accept(name: str, user: str):
	p = frappe.get_doc(DOCTYPE, name)
	if not p.thread:
		frappe.throw(_("Only a reply can be the best answer."))
	thread = frappe.get_doc(DOCTYPE, p.thread)
	content = _content(p.content, user)
	if thread.user != user and not can_moderate(content, user):
		frappe.throw(
			_("Only the person who asked or a moderator can choose the best answer."), frappe.PermissionError
		)
	frappe.db.set_value(DOCTYPE, {"thread": thread.name, "accepted": 1}, "accepted", 0)
	frappe.db.set_value(DOCTYPE, p.name, "accepted", 1)
	from vintraxo_tcd.core import badges

	badges.check(p.user, "Answers Accepted")
	frappe.db.set_value(DOCTYPE, thread.name, "status", "Answered")


def set_hidden(name: str, hidden: int, user: str):
	p = frappe.get_doc(DOCTYPE, name)
	if not can_moderate(_content(p.content, user), user):
		frappe.throw(_("Only moderators can hide posts."), frappe.PermissionError)
	frappe.db.set_value(DOCTYPE, p.name, "hidden", 1 if int(hidden) else 0)


def validate(doc):
	"""Desk edits are limited to moderation (hidden); text and links come only from the service."""
	if doc.is_new():
		if not doc.flags.from_service:
			frappe.throw(_("Posts are created from the lesson page."))
		return
	before = doc.get_doc_before_save()
	for field in ("content", "thread", "user", "body"):
		if before and before.get(field) != doc.get(field):
			frappe.throw(_("Only moderation fields can be changed."))
