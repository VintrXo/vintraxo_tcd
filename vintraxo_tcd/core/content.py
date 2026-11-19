"""Content rules: block schema, slugs, search text and the review/publish workflow."""

import json
import re

import frappe
from frappe import _
from frappe.query_builder.functions import Max

from vintraxo_tcd.core.search import normalize_text

# ---------------------------------------------------------------- blocks

PLAYGROUND_LANGUAGES = ("python", "sql", "html", "javascript", "java", "cpp", "c", "go", "csharp", "bash")
# the last six run only when the code runner (Phase 10) is enabled for them
CALLOUT_VARIANTS = ("info", "tip", "warning", "danger")

# type -> {field: (python type, required)}
BLOCK_SCHEMA = {
	"heading": {"text": (str, True), "level": (int, False)},
	"paragraph": {"text": (str, True)},
	"code": {"code": (str, True), "language": (str, False)},
	"callout": {"text": (str, True), "variant": (str, False), "title": (str, False)},
	"list": {"items": (list, True), "ordered": (bool, False)},
	"image": {"url": (str, True), "alt": (str, False), "caption": (str, False)},
	"playground": {"language": (str, True), "code": (str, True), "expected_output": (str, False)},
	"video": {
		"url": (str, True),
		"title": (str, False),
		"caption": (str, False),
		"provider": (str, False),
		"embed_url": (str, False),
	},
	"link": {"url": (str, True), "title": (str, True), "description": (str, False)},
	"markdown": {"text": (str, True)},
	"file": {"url": (str, True), "title": (str, True)},
	# practice exercise (Phase 17): code with ___ blanks, one answer per blank ("a | b" accepts either)
	"exercise": {
		"prompt": (str, True),
		"code": (str, True),
		"answers": (list, True),
		"language": (str, False),
		"hint": (str, False),
	},
}
BLANK = "___"

# fields whose text goes into search_text, per block type
SEARCHABLE = {
	"heading": ("text",),
	"paragraph": ("text",),
	"code": ("code",),
	"callout": ("title", "text"),
	"list": ("items",),
	"image": ("alt", "caption"),
	"playground": ("code",),
	"video": ("title", "caption"),
	"link": ("title", "description"),
	"markdown": ("text",),
	"file": ("title",),
	"exercise": ("prompt", "code"),
}


def parse_blocks(value) -> list:
	if value in (None, ""):
		return []
	if isinstance(value, str):
		try:
			value = json.loads(value)
		except ValueError:
			frappe.throw(_("Blocks must be valid JSON."))
	if not isinstance(value, list):
		frappe.throw(_("Blocks must be a JSON list."))
	return value


def validate_blocks(blocks: list) -> list:
	"""Validate blocks against BLOCK_SCHEMA. Unknown keys are dropped. Returns cleaned blocks."""
	cleaned = []
	for idx, block in enumerate(blocks, start=1):
		if not isinstance(block, dict):
			frappe.throw(_("Block {0} must be an object.").format(idx))
		btype = block.get("type")
		schema = BLOCK_SCHEMA.get(btype)
		if not schema:
			frappe.throw(_("Block {0}: unknown type {1}.").format(idx, frappe.bold(btype)))

		out = {"type": btype}
		for field, (ftype, required) in schema.items():
			val = block.get(field)
			if val is None:
				if required:
					frappe.throw(_("Block {0} ({1}): {2} is required.").format(idx, btype, field))
				continue
			# bool is a subclass of int; keep them strict
			if not isinstance(val, ftype) or (ftype is int and isinstance(val, bool)):
				frappe.throw(_("Block {0} ({1}): {2} has the wrong type.").format(idx, btype, field))
			out[field] = val

		_validate_block_values(idx, out)
		cleaned.append(out)
	return cleaned


def _validate_block_values(idx: int, block: dict):
	btype = block["type"]
	if btype == "heading" and not 1 <= block.get("level", 2) <= 4:
		frappe.throw(_("Block {0}: heading level must be between 1 and 4.").format(idx))
	if btype == "callout" and block.get("variant", "info") not in CALLOUT_VARIANTS:
		frappe.throw(
			_("Block {0}: callout variant must be one of {1}.").format(idx, ", ".join(CALLOUT_VARIANTS))
		)
	if btype == "list" and not all(isinstance(i, str) for i in block["items"]):
		frappe.throw(_("Block {0}: list items must be text.").format(idx))
	if btype == "playground" and block["language"] not in PLAYGROUND_LANGUAGES:
		frappe.throw(
			_("Block {0}: playground language must be one of {1}.").format(
				idx, ", ".join(PLAYGROUND_LANGUAGES)
			)
		)
	if btype == "exercise":
		answers = block["answers"]
		if not answers or not all(isinstance(a, str) and a.strip() for a in answers):
			frappe.throw(_("Block {0}: every exercise answer must be filled in.").format(idx))
		blanks = block["code"].count(BLANK)
		if blanks != len(answers):
			frappe.throw(
				_("Block {0}: the code has {1} blanks (___) but {2} answers.").format(
					idx, blanks, len(answers)
				)
			)
		block["answers"] = [a.strip()[:200] for a in answers]
	if btype == "image" and not re.match(r"^(https?://|/)", block["url"]):
		frappe.throw(_("Block {0}: image URL must be absolute (http/https) or start with /.").format(idx))
	if btype in ("video", "link", "file"):
		from vintraxo_tcd.core import media

		if btype == "video":
			block["provider"], block["embed_url"] = media.parse_video(block["url"])
		elif btype == "link":
			media.validate_link(block["url"])
		else:
			media.validate_file_url(block["url"], public_only=True)


def dump_blocks(blocks: list) -> str:
	return json.dumps(blocks, ensure_ascii=False)


def build_search_text(title: str | None, summary: str | None, blocks: list) -> str:
	parts = [title or "", summary or ""]
	for block in blocks:
		for field in SEARCHABLE.get(block.get("type"), ()):
			val = block.get(field)
			if isinstance(val, list):
				parts.extend(val)
			elif val:
				parts.append(val)
	return normalize_text(" ".join(parts))


# ---------------------------------------------------------------- slugs


def slugify(text: str) -> str:
	"""URL slug that keeps Arabic letters: 'مقدمة في بايثون' -> 'مقدمه-في-بايثون'."""
	text = normalize_text(text)
	text = re.sub(r"[^\w]+", "-", text, flags=re.UNICODE).strip("-_")
	return text[:140] or "content"


def ensure_unique_slug(doc):
	if not doc.slug:
		base = slugify(doc.title)
		slug, n = base, 1
		while _slug_taken(doc, slug):
			n += 1
			slug = f"{base}-{n}"
		doc.slug = slug
		return

	doc.slug = slugify(doc.slug)
	if _slug_taken(doc, doc.slug):
		frappe.throw(_("Slug {0} is already used in this space.").format(frappe.bold(doc.slug)))


def _slug_taken(doc, slug) -> bool:
	return bool(
		frappe.db.exists(doc.doctype, {"space": doc.space, "slug": slug, "name": ("!=", doc.name or "")})
	)


# ---------------------------------------------------------------- tutorials


def lesson_list(doc) -> list[dict]:
	return [{"lesson": r.lesson, "is_optional": int(r.is_optional or 0)} for r in doc.get("lessons") or []]


def validate_lessons(doc):
	"""Tutorial lessons: TCD Content of type Lesson, same space, no duplicates."""
	if doc.content_type != "Tutorial":
		doc.set("lessons", [])
		return
	seen = set()
	for row in doc.lessons:
		if row.lesson in seen:
			frappe.throw(
				_("Row {0}: lesson {1} is listed twice.").format(row.idx, frappe.bold(row.lesson_title))
			)
		seen.add(row.lesson)
		lesson = frappe.db.get_value(
			"TCD Content", row.lesson, ["content_type", "space", "title"], as_dict=True
		)
		if not lesson:
			continue  # link validation reports it
		if lesson.content_type != "Lesson":
			frappe.throw(_("Row {0}: {1} is not a Lesson.").format(row.idx, frappe.bold(lesson.title)))
		if lesson.space != doc.space:
			frappe.throw(
				_("Row {0}: lesson {1} must be in the same space.").format(row.idx, frappe.bold(lesson.title))
			)
		row.lesson_title = lesson.title


def tutorials_for_lesson(lesson: str) -> list[str]:
	return frappe.get_all(
		"TCD Tutorial Lesson",
		filters={"parenttype": "TCD Content", "lesson": lesson},
		pluck="parent",
		distinct=True,
		ignore_permissions=True,
	)


# ---------------------------------------------------------------- workflow

REVIEW_ROLES = {"TCD Content Reviewer", "TCD Administrator", "System Manager"}
LOCKED_STATUSES = ("Approved", "Published")
LOCKED_FIELDS = ("title", "summary", "blocks", "language", "lessons")

# from -> allowed targets
TRANSITIONS = {
	"Draft": {"In Review", "Published"},  # direct publish only when approval is not required
	"In Review": {"Draft", "Approved"},
	"Approved": {"Draft", "Published"},
	"Published": {"Draft", "Archived"},
	"Archived": {"Draft"},
}


def require_approval() -> bool:
	return bool(frappe.db.get_single_value("TCD Settings", "require_approval_before_publish"))


def validate_transition(doc, old_status: str | None, new_status: str):
	"""Throw if old -> new is not allowed for the current user. Sets doc.flags.snapshot when needed."""
	user_roles = set(frappe.get_roles())
	is_reviewer = bool(user_roles & REVIEW_ROLES)
	approval = require_approval()

	if old_status is None:
		if new_status not in ("Draft", "In Review"):
			frappe.throw(_("New content must start as Draft or In Review."))
		return

	if new_status not in TRANSITIONS.get(old_status, set()):
		frappe.throw(_("Cannot move content from {0} to {1}.").format(_(old_status), _(new_status)))

	if old_status == "Draft" and new_status == "Published" and approval:
		frappe.throw(_("Content must be reviewed and approved before publishing."))

	if new_status == "Approved":
		if not is_reviewer:
			frappe.throw(_("Only a reviewer can approve content."), frappe.PermissionError)
		doc.flags.snapshot = True

	if new_status == "Published":
		if approval and not is_reviewer:
			frappe.throw(_("Only a reviewer can publish content."), frappe.PermissionError)
		if not approval and old_status == "Draft":
			# no review step: publishing is the approval
			doc.flags.snapshot = True


def validate_locked_fields(doc, before):
	"""Approved/Published content is frozen; move it back to Draft to edit."""
	if before.status not in LOCKED_STATUSES or doc.status != before.status:
		return
	if doc.flags.change_request:  # a suggested edit a reviewer accepted (core.change_requests.accept)
		return
	for field in LOCKED_FIELDS:
		old, new = before.get(field), doc.get(field)
		if field == "blocks":
			old, new = parse_blocks(old), parse_blocks(new)
		if field == "lessons":
			old, new = lesson_list(before), lesson_list(doc)
		if (old or None) != (new or None):
			frappe.throw(
				_("{0} content cannot be edited. Move it back to Draft first.").format(_(before.status))
			)


def create_snapshot(doc) -> str:
	"""Store an immutable approved version and point the content at it."""
	V = frappe.qb.DocType("TCD Content Version")
	last = frappe.qb.from_(V).select(Max(V.version_number)).where(V.content == doc.name).run()[0][0] or 0
	version = frappe.get_doc(
		{
			"doctype": "TCD Content Version",
			"content": doc.name,
			"version_number": int(last) + 1,
			"title": doc.title,
			"language": doc.language,
			"summary": doc.summary,
			"blocks": doc.blocks,
			"search_text": doc.search_text,
			"lessons": json.dumps(lesson_list(doc)) if doc.content_type == "Tutorial" else None,
			"approved_by": frappe.session.user,
			"approved_on": frappe.utils.now_datetime(),
		}
	)
	version.flags.from_content = True
	version.insert(ignore_permissions=True)
	return version.name
