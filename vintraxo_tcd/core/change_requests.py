"""Suggested edits (Phase 14, ADR-0022), like Frappe Wiki change requests.

Readers of a published page propose new text for its text blocks (structure stays the same). The page
does not change until a reviewer accepts; accepting writes a new approved version. If the page changed
after the proposal, the request becomes a Conflict instead of overwriting."""

import hashlib
import json

import frappe
from frappe import _
from frappe.utils import add_to_date, now_datetime

from vintraxo_tcd.core import content as svc
from vintraxo_tcd.core.permissions import can_access_content, is_admin

DOCTYPE = "TCD Change Request"
# block type -> text fields a reader may change
EDITABLE = {
	"heading": ("text",),
	"paragraph": ("text",),
	"callout": ("title", "text"),
	"list": ("items",),
	"markdown": ("text",),
	"code": ("code",),
}
PER_HOUR = 5


def enabled() -> bool:
	return bool(frappe.db.get_single_value("TCD Settings", "enable_change_requests"))


def _hash(blocks_json) -> str:
	blocks = svc.parse_blocks(blocks_json)
	return hashlib.sha256(json.dumps(blocks, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def is_reviewer(user: str) -> bool:
	return is_admin(user) or bool(set(frappe.get_roles(user)) & svc.REVIEW_ROLES)


def editable_fields(doc) -> list[dict]:
	"""What the portal editor shows: one entry per editable text field."""
	out = []
	for index, block in enumerate(svc.parse_blocks(doc.blocks)):
		for field in EDITABLE.get(block.get("type"), ()):
			value = block.get(field)
			if isinstance(value, list):
				value = "\n".join(str(v) for v in value)
			out.append({"index": index, "type": block["type"], "field": field, "value": value or ""})
	return out


def propose(content: str, edits, user: str, title: str | None = None, summary: str = "") -> str:
	if user == "Guest":
		raise frappe.PermissionError
	if not enabled():
		frappe.throw(_("Suggested edits are turned off."))
	doc = frappe.get_doc("TCD Content", content)
	if doc.status != "Published" or not can_access_content(doc, user):
		raise frappe.DoesNotExistError
	recent = frappe.db.count(
		DOCTYPE, {"user": user, "creation": (">=", add_to_date(now_datetime(), hours=-1))}
	)
	if recent >= PER_HOUR:
		frappe.throw(_("You suggested many edits in the last hour. Try again later."))
	if isinstance(edits, str):
		edits = json.loads(edits or "[]")
	blocks = svc.parse_blocks(doc.blocks)
	changed = False
	for edit in edits or []:
		index, field = int(edit.get("index", -1)), edit.get("field")
		if not 0 <= index < len(blocks) or field not in EDITABLE.get(blocks[index].get("type"), ()):
			frappe.throw(_("This part of the page cannot be edited."))
		value = str(edit.get("value") or "")
		if field == "items":
			value = [line.strip() for line in value.splitlines() if line.strip()]
		if blocks[index].get(field) != value:
			blocks[index][field] = value
			changed = True
	title = (title or doc.title).strip()[:140]
	if not changed and title == doc.title:
		frappe.throw(_("Nothing was changed."))
	blocks = svc.validate_blocks(blocks)  # same schema and sanitizing as the editor
	cr = frappe.get_doc(
		{
			"doctype": DOCTYPE,
			"content": doc.name,
			"user": user,
			"status": "Open",
			"summary": (summary or "").strip()[:1000],
			"proposed_title": title,
			"proposed_blocks": json.dumps(blocks, ensure_ascii=False),
			"base_hash": _hash(doc.blocks),
		}
	)
	cr.flags.from_service = True
	cr.insert(ignore_permissions=True)
	from vintraxo_tcd.core import notify

	owner = doc.get("content_owner") or doc.owner
	notify._send(
		[u for u in (owner,) if u != user],
		_("Suggested edit on {0}").format(doc.title),
		DOCTYPE,
		cr.name,
		cr.summary,
	)
	return cr.name


def diff(name: str) -> dict:
	import difflib

	from vintraxo_tcd.core.wiki import _lines

	cr = frappe.get_doc(DOCTYPE, name)
	doc = frappe.get_doc("TCD Content", cr.content)
	a = _lines(doc.title, doc.summary, doc.blocks, "[]")
	b = _lines(cr.proposed_title, doc.summary, cr.proposed_blocks, "[]")
	lines = list(
		difflib.unified_diff(a, b, fromfile=_("Current version"), tofile=_("Suggested"), lineterm="", n=2)
	)
	return {"diff": lines, "conflict": _hash(doc.blocks) != cr.base_hash}


def _decide(name: str, user: str):
	if not is_reviewer(user):
		frappe.throw(_("Only reviewers can accept or reject suggested edits."), frappe.PermissionError)
	cr = frappe.get_doc(DOCTYPE, name)
	if cr.status != "Open":
		frappe.throw(_("This suggestion is already closed."))
	return cr


def accept(name: str, user: str, comment: str = "") -> str:
	cr = _decide(name, user)
	doc = frappe.get_doc("TCD Content", cr.content)
	if _hash(doc.blocks) != cr.base_hash:
		cr.db_set(
			{"status": "Conflict", "reviewer": user, "reviewed_on": now_datetime(), "review_comment": comment}
		)
		frappe.db.commit()  # keep the Conflict status although the request fails
		frappe.throw(_("The page changed after this suggestion was made. Ask for a new suggestion."))
	doc.title = cr.proposed_title or doc.title
	doc.blocks = cr.proposed_blocks
	doc.flags.change_request = True  # an accepted suggestion is a reviewed change of a published page
	if doc.status in svc.LOCKED_STATUSES:
		doc.flags.snapshot = True
	doc.save()
	cr.db_set(
		{"status": "Accepted", "reviewer": user, "reviewed_on": now_datetime(), "review_comment": comment}
	)
	_tell(cr, _("Your suggested edit was accepted: {0}").format(doc.title))
	from vintraxo_tcd.core import badges

	badges.check(cr.user, "Edits Accepted")
	return doc.name


def reject(name: str, user: str, comment: str = ""):
	cr = _decide(name, user)
	cr.db_set(
		{"status": "Rejected", "reviewer": user, "reviewed_on": now_datetime(), "review_comment": comment}
	)
	title = frappe.db.get_value("TCD Content", cr.content, "title")
	_tell(cr, _("Your suggested edit was not accepted: {0}").format(title))


def _tell(cr, subject: str):
	from vintraxo_tcd.core import notify

	notify._send([cr.user], subject, DOCTYPE, cr.name, cr.review_comment or "")


def validate(doc):
	if doc.is_new() and not doc.flags.from_service:
		frappe.throw(_("Suggestions are made from the page in the portal."))
