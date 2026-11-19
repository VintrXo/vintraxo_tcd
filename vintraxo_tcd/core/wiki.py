"""Wiki features (PLAN Phase 3, ADR-0012): internal links, Markdown, page tree, backlinks,
version compare/restore, page feedback, templates, tags."""

import difflib
import json
import re

import frappe
from frappe import _
from frappe.utils import escape_html

from vintraxo_tcd.core import content as svc

LINK_RE = re.compile(r"\[\[([^\[\]|]{1,200})(?:\|([^\[\]]{1,200}))?\]\]")
TEXT_FIELDS = {"paragraph": ("text",), "callout": ("text",), "markdown": ("text",)}
DISALLOWED_TAGS = [
	"link",
	"meta",
	"style",
	"iframe",
	"frame",
	"object",
	"embed",
	"form",
	"input",
	"button",
	"html",
	"head",
	"body",
	"base",
]


# ---------------------------------------------------------------- internal links


def resolve_link(target: str, space: str) -> str | None:
	"""`slug` (same space) or `space/slug` -> content name, or None."""
	target = target.strip()
	if "/" in target:
		target_space, slug = target.split("/", 1)
	else:
		target_space, slug = space, target
	slug = svc.slugify(slug)
	return frappe.db.get_value("TCD Content", {"space": target_space.strip(), "slug": slug})


def extract_links(blocks: list, space: str, own_name: str | None = None) -> list[str]:
	found = []
	for block in blocks:
		for field in TEXT_FIELDS.get(block.get("type"), ()):
			for target, _label in LINK_RE.findall(block.get(field) or ""):
				name = resolve_link(target, space)
				if name and name != own_name and name not in found:
					found.append(name)
	return found


def _link_html(target: str, label: str | None, space: str) -> str:
	"""Escaped label; an <a> only when the target is readable."""
	from vintraxo_tcd.core.connect import url_for

	name = resolve_link(target, space)
	text = (label or "").strip()
	if name and frappe.has_permission("TCD Content", "read", name):
		title = frappe.db.get_value("TCD Content", name, "title")
		return f'<a class="tcd-wikilink" href="{escape_html(url_for("TCD Content", name))}">{escape_html(text or title)}</a>'
	return escape_html(text or target)


def render_inline(text: str, space: str) -> str:
	"""Plain text with [[links]] -> safe HTML (everything escaped except our own anchors)."""
	out, last = [], 0
	for m in LINK_RE.finditer(text or ""):
		out.append(escape_html(text[last : m.start()]))
		out.append(_link_html(m.group(1), m.group(2), space))
		last = m.end()
	out.append(escape_html((text or "")[last:]))
	return "".join(out)


def render_markdown(text: str, space: str) -> str:
	from frappe.utils import md_to_html
	from frappe.utils.html_utils import sanitize_html

	def to_md(m):
		from vintraxo_tcd.core.connect import url_for

		name = resolve_link(m.group(1), space)
		label = (m.group(2) or "").strip()
		if name and frappe.has_permission("TCD Content", "read", name):
			title = label or frappe.db.get_value("TCD Content", name, "title")
			safe = title.replace("[", "").replace("]", "")
			return f"[{safe}]({url_for('TCD Content', name)})"
		return label or m.group(1)

	html = md_to_html(LINK_RE.sub(to_md, text or "")) or ""
	return sanitize_html(str(html), always_sanitize=True, disallowed_tags=DISALLOWED_TAGS)


def prepare_blocks(blocks: list, space: str) -> list:
	"""Add a safe `html` key to text blocks for the portal renderer."""
	out = []
	for block in blocks:
		b = dict(block)
		if b.get("type") == "markdown":
			b["html"] = render_markdown(b.get("text"), space)
		elif b.get("type") in ("paragraph", "callout") and LINK_RE.search(b.get("text") or ""):
			b["html"] = render_inline(b.get("text"), space)
		out.append(b)
	return out


def backlinks(content: str) -> list[dict]:
	from vintraxo_tcd.core.connect import _item

	rows = frappe.get_all(
		"TCD Content",
		filters={"internal_links": ("like", f'%"{content}"%')},
		pluck="name",
		ignore_permissions=True,
	)
	return [i for i in (_item("TCD Content", n) for n in rows if n != content) if i]


# ---------------------------------------------------------------- page tree


def validate_parent(doc):
	if not doc.parent_content:
		return
	if doc.parent_content == doc.name:
		frappe.throw(_("A page cannot be its own parent."))
	seen = {doc.name}
	parent = doc.parent_content
	first = True
	while parent:
		if parent in seen:
			frappe.throw(_("Parent Page would create a loop."))
		seen.add(parent)
		row = frappe.db.get_value(
			"TCD Content", parent, ["space", "parent_content", "content_type"], as_dict=True
		)
		if not row:
			return
		if first:
			if row.space != doc.space:
				frappe.throw(_("Parent Page must be in the same space."))
			if row.content_type == "Tutorial" or doc.content_type == "Tutorial":
				frappe.throw(_("Tutorials are organized by their lessons, not by parent pages."))
			first = False
		parent = row.parent_content


def page_tree(space: str) -> list[dict]:
	"""Nested readable pages (non-tutorial) of a space, ordered by title."""
	from vintraxo_tcd.core.portal import content_url

	rows = frappe.get_list(
		"TCD Content",
		filters={"space": space, "content_type": ("!=", "Tutorial")},
		fields=["name", "title", "slug", "parent_content", "content_type"],
		order_by="title asc",
		limit_page_length=1000,
	)
	by_name = {r.name: {**r, "url": content_url(space, r.slug), "children": []} for r in rows}
	roots = []
	for node in by_name.values():
		parent = by_name.get(node["parent_content"])
		(parent["children"] if parent else roots).append(node)
	return roots


def ancestors(content: str) -> list[dict]:
	"""Readable ancestors from the root down."""
	chain, seen = [], set()
	parent = frappe.db.get_value("TCD Content", content, "parent_content")
	while parent and parent not in seen:
		seen.add(parent)
		if frappe.has_permission("TCD Content", "read", parent):
			row = frappe.db.get_value("TCD Content", parent, ["name", "title", "slug", "space"], as_dict=True)
			chain.insert(0, row)
		parent = frappe.db.get_value("TCD Content", parent, "parent_content")
	return chain


# ---------------------------------------------------------------- versions


def _lines(title, summary, blocks_json, lessons_json=None) -> list[str]:
	lines = [f"# {title or ''}"]
	if summary:
		lines += ["", summary]
	for i, block in enumerate(svc.parse_blocks(blocks_json), start=1):
		lines.append("")
		lines.append(f"[{i}] {block.get('type')}")
		for key, value in block.items():
			if key in ("type", "embed_url", "provider"):
				continue
			if isinstance(value, list):
				value = "\n".join(str(v) for v in value)
			lines += [f"  {line}" for line in str(value).splitlines() or [""]]
	lessons = json.loads(lessons_json) if isinstance(lessons_json, str) else lessons_json
	if lessons:
		lines.append("")
		lines += [f"- {row['lesson']}" for row in lessons]
	return lines


def snapshot_lines(name: str) -> tuple[str, list[str]]:
	"""Lines for a version name or the current state of a content name."""
	if frappe.db.exists("TCD Content Version", name):
		v = frappe.get_doc("TCD Content Version", name)
		return f"v{v.version_number}", _lines(v.title, v.summary, v.blocks, v.lessons)
	c = frappe.get_doc("TCD Content", name)
	return _("Current version"), _lines(c.title, c.summary, c.blocks, json.dumps(svc.lesson_list(c)))


def compare(old: str, new: str) -> dict:
	old_label, a = snapshot_lines(old)
	new_label, b = snapshot_lines(new)
	diff = list(difflib.unified_diff(a, b, fromfile=old_label, tofile=new_label, lineterm="", n=2))
	return {
		"from": old_label,
		"to": new_label,
		"diff": diff,
		"added": sum(1 for d in diff if d.startswith("+") and not d.startswith("+++")),
		"removed": sum(1 for d in diff if d.startswith("-") and not d.startswith("---")),
	}


def restore(version_name: str):
	version = frappe.get_doc("TCD Content Version", version_name)
	doc = frappe.get_doc("TCD Content", version.content)
	doc.check_permission("write")
	if doc.status != "Draft":
		doc.status = "Draft"
		doc.save()
	doc.reload()
	doc.title = version.title
	doc.summary = version.summary
	doc.blocks = version.blocks
	if version.lessons and doc.content_type == "Tutorial":
		doc.set(
			"lessons",
			[
				{"lesson": r["lesson"], "is_optional": r.get("is_optional", 0)}
				for r in json.loads(version.lessons)
			],
		)
	doc.add_comment("Info", _("Restored from version {0}").format(version.version_number))
	doc.save()
	return doc


# ---------------------------------------------------------------- feedback


def give_feedback(content: str, user: str, helpful: bool, comment: str | None = None):
	name = frappe.db.get_value("TCD Content Feedback", {"content": content, "user": user})
	doc = frappe.get_doc("TCD Content Feedback", name) if name else frappe.new_doc("TCD Content Feedback")
	doc.update(
		{
			"content": content,
			"user": user,
			"helpful": int(bool(helpful)),
			"comment": (comment or "").strip()[:2000],
		}
	)
	doc.flags.from_api = True
	doc.save(ignore_permissions=True)
	return doc


def feedback_stats(content: str) -> dict:
	rows = frappe.get_all(
		"TCD Content Feedback", filters={"content": content}, pluck="helpful", ignore_permissions=True
	)
	return {"helpful": sum(rows), "total": len(rows)}


# ---------------------------------------------------------------- tags


def tags_of(content: str) -> list[str]:
	return frappe.get_all(
		"Tag Link",
		filters={"document_type": "TCD Content", "document_name": content},
		pluck="tag",
		order_by="tag asc",
		ignore_permissions=True,
	)


def contents_with_tag(tag: str) -> list[str]:
	names = frappe.get_all(
		"Tag Link",
		filters={"document_type": "TCD Content", "tag": tag},
		pluck="document_name",
		ignore_permissions=True,
	)
	if not names:
		return []
	return frappe.get_list("TCD Content", filters={"name": ("in", names)}, pluck="name")


# ---------------------------------------------------------------- templates


def validate_template(doc):
	doc.blocks = svc.dump_blocks(svc.validate_blocks(svc.parse_blocks(doc.blocks)))
	if doc.content_type != "Lesson":
		doc.lesson_type = None
