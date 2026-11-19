"""Personal lesson notes (Phase 14): private to their author. The DocType has no role permissions; notes
are read and written only through this service, always for the current user."""

import frappe
from frappe import _

MAX_CHARS = 10000


def get(content: str, user: str) -> str:
	return frappe.db.get_value("TCD Lesson Note", {"user": user, "content": content}, "note") or ""


def save(content: str, note: str, user: str) -> dict:
	if user == "Guest":
		raise frappe.PermissionError
	note = (note or "").strip()
	if len(note) > MAX_CHARS:
		frappe.throw(_("Notes are limited to {0} characters.").format(MAX_CHARS))
	name = frappe.db.get_value("TCD Lesson Note", {"user": user, "content": content})
	if not note:
		if name:
			frappe.delete_doc("TCD Lesson Note", name, ignore_permissions=True)
		return {"saved": True}
	if name:
		frappe.db.set_value("TCD Lesson Note", name, "note", note)
	else:
		frappe.get_doc({"doctype": "TCD Lesson Note", "user": user, "content": content, "note": note}).insert(
			ignore_permissions=True
		)
	return {"saved": True}


def mine(user: str, limit: int = 50) -> list[dict]:
	from vintraxo_tcd.core.portal import content_url

	out = []
	for n in frappe.get_all(
		"TCD Lesson Note",
		filters={"user": user},
		fields=["content", "note", "modified"],
		order_by="modified desc",
		limit=limit,
	):
		c = frappe.db.get_value("TCD Content", n.content, ["title", "space", "slug", "status"], as_dict=True)
		if not c or c.status != "Published" or not frappe.has_permission("TCD Content", "read", n.content):
			continue
		out.append(
			{
				"title": c.title,
				"url": content_url(c.space, c.slug),
				"note": n.note[:160],
				"modified": n.modified,
			}
		)
	return out
