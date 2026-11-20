"""Authoring studio in the learning portal (Phase 18, ADR-0026).

Authors, reviewers and instructors write pages and courses without the Desk. Every save goes through the
normal DocType permissions and validations (doc.save without ignore_permissions), so the studio adds no
new way to change content: it is another screen over the same rules (review workflow, locked fields,
block schema, course chapter lock)."""

import json

import frappe
from frappe import _

from vintraxo_tcd.core import content as svc
from vintraxo_tcd.core.permissions import is_admin

CONTENT_FIELDS = ("title", "content_type", "language", "visibility", "summary", "category")
COURSE_FIELDS = (
	"title",
	"language",
	"visibility",
	"summary",
	"category",
	"completion_rule",
	"minimum_score",
	"self_enrollment",
	"access",
	"issue_certificate",
	"requires_evaluation",
	"evaluation_minutes",
	"intro_video",
	"cover_image",
)
MAX_CHAPTERS = 100
MAX_ITEMS = 300


def block_spec() -> dict:
	"""The block editor form, translated on the server (same labels as the Desk editor)."""

	def t(text):
		return _(text, context="TCD Block")

	langs = list(svc.PLAYGROUND_LANGUAGES)
	return {
		"heading": {
			"label": t("Heading"),
			"fields": [["text", "data", t("Text")], ["level", "select", t("Level"), ["1", "2", "3", "4"]]],
		},
		"paragraph": {"label": t("Paragraph"), "fields": [["text", "text", t("Text")]]},
		"markdown": {
			"label": t("Markdown"),
			"fields": [["text", "text", t("Markdown (links: [[page-slug]])")]],
		},
		"code": {
			"label": t("Code"),
			"fields": [["language", "data", t("Language"), None, "ltr"], ["code", "code", t("Code")]],
		},
		"callout": {
			"label": t("Callout"),
			"fields": [
				["variant", "select", t("Variant"), list(svc.CALLOUT_VARIANTS)],
				["title", "data", t("Title")],
				["text", "text", t("Text")],
			],
		},
		"list": {
			"label": t("List"),
			"fields": [["ordered", "check", t("Numbered")], ["items", "lines", t("Items (one per line)")]],
		},
		"image": {
			"label": t("Image"),
			"fields": [
				["url", "upload", t("Image URL"), "image/*", "ltr"],
				["alt", "data", t("Alt Text")],
				["caption", "data", t("Caption")],
			],
		},
		"playground": {
			"label": t("Playground"),
			"fields": [
				["language", "select", t("Language"), langs],
				["code", "code", t("Starter Code")],
				["expected_output", "code", t("Expected Output (optional)")],
			],
		},
		"exercise": {
			"label": t("Exercise"),
			"fields": [
				["prompt", "text", t("Question")],
				["language", "data", t("Language"), None, "ltr"],
				["code", "code", t("Code (write ___ for each blank)")],
				["answers", "lines", t("Answers (one per blank, in order; a | b accepts either)")],
				["hint", "text", t("Hint (optional)")],
			],
		},
		"reference": {
			"label": t("Reference Table"),
			"fields": [
				["title", "data", t("Title")],
				["language", "data", t("Language"), None, "ltr"],
				["entries", "lines", t("Entries (one per line: name | description | example)")],
			],
		},
		"video": {
			"label": t("Video"),
			"fields": [
				["url", "upload", t("Video URL (YouTube, Vimeo or upload)"), ".mp4,.webm", "ltr"],
				["title", "data", t("Title")],
				["caption", "data", t("Caption")],
			],
		},
		"link": {
			"label": t("External Link"),
			"fields": [
				["url", "data", t("Link URL (https)"), None, "ltr"],
				["title", "data", t("Title")],
				["description", "text", t("Description")],
			],
		},
		"file": {
			"label": t("File"),
			"fields": [["url", "upload", t("File"), "", "ltr"], ["title", "data", t("Title")]],
		},
	}


# ---------------------------------------------------------------- access


def can_author(user: str | None = None) -> bool:
	user = user or frappe.session.user
	if user == "Guest":
		return False
	return bool(
		frappe.has_permission("TCD Content", "create", user=user)
		or frappe.has_permission("TCD Content", "write", user=user)
		or frappe.has_permission("TCD Course", "write", user=user)
	)


def require_author():
	if not can_author():
		raise frappe.PermissionError(_("The studio is for content authors, reviewers and administrators."))


def _writable(doctype: str, name: str) -> bool:
	return bool(frappe.has_permission(doctype, "write", name))


# ---------------------------------------------------------------- dashboard


def home() -> dict:
	require_author()
	user = frappe.session.user
	pages = frappe.get_list(
		"TCD Content",
		filters={"status": ("!=", "Archived")},
		fields=["name", "title", "status", "content_type", "space", "modified", "owner", "slug"],
		order_by="modified desc",
		limit_page_length=200,
	)
	pages = [p for p in pages if _writable("TCD Content", p.name)]
	courses = frappe.get_list(
		"TCD Course",
		filters={"status": ("!=", "Archived")},
		fields=["name", "title", "status", "space", "modified", "slug"],
		order_by="modified desc",
		limit_page_length=100,
	)
	courses = [c for c in courses if _writable("TCD Course", c.name)]
	groups = {"Draft": [], "In Review": [], "Approved": [], "Published": []}
	for p in pages:
		groups.setdefault(p.status, []).append(p)
	return {
		"mine": [p for p in groups["Draft"] if p.owner == user],
		"drafts": [p for p in groups["Draft"] if p.owner != user],
		"in_review": groups["In Review"],
		"approved": groups["Approved"],
		"published": groups["Published"][:30],
		"courses": courses,
		"can_create_content": bool(frappe.has_permission("TCD Content", "create")),
		"can_create_course": bool(frappe.has_permission("TCD Course", "create")),
		"spaces": spaces_for_authoring(),
	}


def spaces_for_authoring() -> list[dict]:
	return frappe.get_list(
		"TCD Space",
		filters={"is_active": 1},
		fields=["name", "title"],
		order_by="title asc",
		limit_page_length=500,
	)


# ---------------------------------------------------------------- pages


def page_data(name: str | None) -> dict:
	require_author()
	if not name:
		if not frappe.has_permission("TCD Content", "create"):
			raise frappe.PermissionError
		return {
			"doc": {"status": "Draft", "content_type": "Lesson", "language": "ar", "blocks": []},
			"new": True,
		}
	doc = frappe.get_doc("TCD Content", name)
	doc.check_permission("write")
	out = {f: doc.get(f) for f in ("name", "space", "slug", "status", *CONTENT_FIELDS)}
	out["blocks"] = svc.parse_blocks(doc.blocks)
	return {"doc": out, "new": False, "locked": doc.status in ("Approved", "Published")}


def save_page(data) -> dict:
	"""Create or update a page. Status changes go through api.set_content_status."""
	require_author()
	if isinstance(data, str):
		data = json.loads(data or "{}")
	blocks = svc.validate_blocks(svc.parse_blocks(data.get("blocks") or []))
	if data.get("name"):
		doc = frappe.get_doc("TCD Content", data["name"])
		doc.check_permission("write")
	else:
		if not data.get("space"):
			frappe.throw(_("Choose a space for the page."))
		frappe.has_permission("TCD Space", "read", data["space"], throw=True)
		doc = frappe.new_doc("TCD Content")
		doc.space = data["space"]
		doc.status = "Draft"
	for f in CONTENT_FIELDS:
		if f in data:
			doc.set(f, data.get(f) or None)
	doc.blocks = svc.dump_blocks(blocks)
	doc.save()  # normal permissions and validations
	return {"name": doc.name, "slug": doc.slug, "space": doc.space, "status": doc.status}


# ---------------------------------------------------------------- courses


def course_data(name: str | None) -> dict:
	require_author()
	if not name:
		if not frappe.has_permission("TCD Course", "create"):
			raise frappe.PermissionError
		return {
			"doc": {"status": "Draft", "completion_rule": "All Items", "access": "Open", "language": "ar"},
			"chapters": [],
			"new": True,
		}
	doc = frappe.get_doc("TCD Course", name)
	doc.check_permission("write")
	from vintraxo_tcd.core import courses

	chapters = []
	for ch in frappe.get_all(
		"TCD Chapter",
		filters={"course": name},
		fields=["name", "title"],
		order_by="sort_order asc, creation asc",
	):
		items = frappe.get_all(
			"TCD Learning Item",
			filters={"parent": ch.name, "parenttype": "TCD Chapter"},
			fields=["content", "is_optional"],
			order_by="idx asc",
		)
		for it in items:
			it["title"] = frappe.db.get_value("TCD Content", it.content, "title")
		chapters.append({"name": ch.name, "title": ch.title, "items": items})
	out = {f: doc.get(f) for f in ("name", "space", "slug", "status", *COURSE_FIELDS)}
	return {
		"doc": out,
		"chapters": chapters,
		"new": False,
		"locked": doc.status != "Draft",
		"items_total": len(courses.course_items(name)),
	}


def save_course(data) -> dict:
	"""Create or update a course and (while it is a draft) its chapters and items."""
	require_author()
	if isinstance(data, str):
		data = json.loads(data or "{}")
	if data.get("name"):
		doc = frappe.get_doc("TCD Course", data["name"])
		doc.check_permission("write")
	else:
		if not data.get("space"):
			frappe.throw(_("Choose a space for the course."))
		frappe.has_permission("TCD Space", "read", data["space"], throw=True)
		doc = frappe.new_doc("TCD Course")
		doc.space = data["space"]
		doc.status = "Draft"
	for f in COURSE_FIELDS:
		if f in data:
			value = data.get(f)
			doc.set(f, value if value not in ("", None) else None)
	doc.save()
	if "chapters" in data:
		_save_chapters(doc, data.get("chapters") or [])
	return {"name": doc.name, "slug": doc.slug, "space": doc.space, "status": doc.status}


def _save_chapters(course, chapters: list):
	if course.status != "Draft":
		frappe.throw(_("Move the course back to Draft to change its chapters."))
	if len(chapters) > MAX_CHAPTERS:
		frappe.throw(_("A course can have at most {0} chapters.").format(MAX_CHAPTERS))
	if sum(len(ch.get("items") or []) for ch in chapters) > MAX_ITEMS:
		frappe.throw(_("A course can have at most {0} items.").format(MAX_ITEMS))
	existing = set(frappe.get_all("TCD Chapter", filters={"course": course.name}, pluck="name"))
	kept = set()
	for order, ch in enumerate(chapters):
		title = (ch.get("title") or "").strip()
		if not title:
			frappe.throw(_("Every chapter needs a title."))
		rows = []
		for it in ch.get("items") or []:
			content = it.get("content")
			if not content or not frappe.db.exists("TCD Content", content):
				frappe.throw(_("A course item points to a page that does not exist."))
			frappe.has_permission("TCD Content", "read", content, throw=True)
			rows.append({"content": content, "is_optional": 1 if it.get("is_optional") else 0})
		name = ch.get("name")
		if name and name in existing:
			chapter = frappe.get_doc("TCD Chapter", name)
			chapter.check_permission("write")
			chapter.title = title
			chapter.sort_order = order
			chapter.set("items", rows)
			chapter.save()
		else:
			chapter = frappe.get_doc(
				{
					"doctype": "TCD Chapter",
					"course": course.name,
					"title": title,
					"sort_order": order,
					"items": rows,
				}
			)
			chapter.insert()
		kept.add(chapter.name)
	for name in existing - kept:
		frappe.delete_doc("TCD Chapter", name)  # permission checked by delete_doc


def set_course_status(name: str, status: str) -> dict:
	require_author()
	if status not in ("Draft", "Published", "Archived"):
		frappe.throw(_("Unknown status."))
	doc = frappe.get_doc("TCD Course", name)
	doc.check_permission("write")
	doc.status = status
	doc.save()
	return {"name": doc.name, "status": doc.status}


def find_pages(query: str = "", space: str | None = None) -> list[dict]:
	"""Pages an author can add to a course (readable, not archived)."""
	require_author()
	filters = {"status": ("!=", "Archived"), "content_type": ("!=", "Tutorial")}
	if space:
		filters["space"] = space
	or_filters = {"title": ("like", f"%{query.strip()}%")} if (query or "").strip() else None
	return frappe.get_list(
		"TCD Content",
		filters=filters,
		or_filters=or_filters,
		fields=["name", "title", "status", "content_type"],
		order_by="title asc",
		limit_page_length=30,
	)


def is_reviewer(user: str | None = None) -> bool:
	user = user or frappe.session.user
	return is_admin(user) or "TCD Content Reviewer" in frappe.get_roles(user)


def labels() -> dict:
	"""UI strings for the studio JS, translated on the server."""
	return {
		"add_block": _("Add block"),
		"remove": _("Remove"),
		"move_up": _("Move up"),
		"move_down": _("Move down"),
		"duplicate": _("Duplicate"),
		"upload": _("Upload"),
		"uploading": _("Uploading..."),
		"saving": _("Saving..."),
		"saved": _("Saved."),
		"unsaved": _("You have unsaved changes."),
		"empty": _("No blocks yet. Add the first one below."),
		"add_chapter": _("Add chapter"),
		"chapter_title": _("Chapter title"),
		"add_page": _("Add a page"),
		"search_pages": _("Search pages by title"),
		"optional": _("Optional"),
		"no_results": _("Nothing found. Try a shorter word."),
		"confirm_remove": _("Remove this item?"),
		"status_changed": _("Status changed to {0}."),
	}
