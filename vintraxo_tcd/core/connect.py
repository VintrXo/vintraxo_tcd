"""Phase 2 - the pillars connect: relations, prerequisites, "used in", navigation, unified search,
recommendations (ADR-0010, ADR-0011). Everything returned to a user is permission-filtered."""

import frappe
from frappe import _

from vintraxo_tcd.core import courses as course_svc
from vintraxo_tcd.core.permissions import is_staff, readable_list
from vintraxo_tcd.core.search import _like, _score, normalize_text, snippet, tokenize

TARGET_FIELD = {"Content": "to_content", "Course": "to_course", "Learning Path": "to_learning_path"}
TARGET_DOCTYPE = {"Content": "TCD Content", "Course": "TCD Course", "Learning Path": "TCD Learning Path"}
RELATION_ORDER = ("Prerequisite", "Next", "Related", "See Also")


# ---------------------------------------------------------------- urls


def url_for(doctype: str, name: str) -> str | None:
	from vintraxo_tcd.core.portal import content_url, course_url, path_url

	row = frappe.db.get_value(doctype, name, ["space", "slug"], as_dict=True)
	if not row:
		return None
	if doctype == "TCD Course":
		return course_url(row.space, row.slug)
	if doctype == "TCD Learning Path":
		return path_url(row.space, row.slug)
	return content_url(row.space, row.slug)


def _item(doctype: str, name: str, **extra) -> dict | None:
	if not frappe.has_permission(doctype, "read", name):
		return None
	row = frappe.db.get_value(doctype, name, ["title"], as_dict=True)
	kind = {"TCD Course": "Course", "TCD Learning Path": "Learning Path"}.get(doctype)
	if not kind:
		kind = frappe.db.get_value("TCD Content", name, "content_type")
	return {
		"doctype": doctype,
		"name": name,
		"title": row.title,
		"kind": kind,
		"url": url_for(doctype, name),
		**extra,
	}


# ---------------------------------------------------------------- relations


def relation_target(rel) -> tuple[str, str]:
	field = TARGET_FIELD[rel.target_type or "Content"]
	return TARGET_DOCTYPE[rel.target_type or "Content"], rel.get(field)


def validate_relation(doc):
	doc.target_type = doc.target_type or "Content"
	field = TARGET_FIELD[doc.target_type]
	for f in TARGET_FIELD.values():
		if f != field:
			doc.set(f, None)
	target = doc.get(field)
	if not target:
		frappe.throw(_("Choose the target of the relation."))
	if doc.target_type == "Content" and target == doc.from_content:
		frappe.throw(_("Content cannot be related to itself."))
	filters = {
		"from_content": doc.from_content,
		"target_type": doc.target_type,
		field: target,
		"relation_type": doc.relation_type,
		"name": ("!=", doc.name),
	}
	if frappe.db.exists("TCD Content Relation", filters):
		frappe.throw(_("This relation already exists."))
	if (
		doc.target_type == "Content"
		and doc.relation_type in ("Prerequisite", "Next")
		and frappe.db.exists(
			"TCD Content Relation",
			{
				"from_content": target,
				"target_type": "Content",
				"to_content": doc.from_content,
				"relation_type": doc.relation_type,
			},
		)
	):
		frappe.throw(_("The reverse {0} relation already exists.").format(_(doc.relation_type)))


def _relations_from(content: str) -> list:
	return frappe.get_all(
		"TCD Content Relation",
		filters={"from_content": content},
		fields=[
			"name",
			"relation_type",
			"target_type",
			"to_content",
			"to_course",
			"to_learning_path",
			"sort_order",
		],
		order_by="sort_order asc, creation asc",
		ignore_permissions=True,
	)


# ---------------------------------------------------------------- prerequisites


def is_satisfied(user: str, doctype: str, name: str) -> bool:
	if doctype == "TCD Content":
		return bool(frappe.db.exists("TCD Progress", {"user": user, "content": name, "status": "Completed"}))
	field = "course" if doctype == "TCD Course" else "learning_path"
	return bool(frappe.db.exists("TCD Enrollment", {"user": user, field: name, "status": "Completed"}))


def prerequisites(user: str, content: str) -> list[dict]:
	"""Prerequisites of a content item with their state (only those the user can see)."""
	out = []
	for rel in _relations_from(content):
		if rel.relation_type != "Prerequisite":
			continue
		doctype, name = relation_target(rel)
		item = _item(doctype, name, satisfied=is_satisfied(user, doctype, name))
		if item:
			out.append(item)
	return out


def unmet_prerequisites(user: str, content: str) -> list[str]:
	"""Titles of unmet prerequisites; staff are never blocked. Hidden targets still count."""
	if is_staff(user):
		return []
	missing = []
	for rel in _relations_from(content):
		if rel.relation_type != "Prerequisite":
			continue
		doctype, name = relation_target(rel)
		if name and not is_satisfied(user, doctype, name):
			missing.append(frappe.db.get_value(doctype, name, "title") or name)
	return missing


def unmet_course_prerequisites(user: str, course: str) -> list[str]:
	rows = frappe.get_all(
		"TCD Course Prerequisite",
		filters={"parent": course, "parenttype": "TCD Course"},
		pluck="course",
		ignore_permissions=True,
	)
	return [
		frappe.db.get_value("TCD Course", c, "title") or c
		for c in rows
		if not is_satisfied(user, "TCD Course", c)
	]


def validate_course_prerequisites(doc):
	seen = set()
	for row in doc.get("prerequisites") or []:
		if row.course == doc.name:
			frappe.throw(_("A course cannot be its own prerequisite."))
		if row.course in seen:
			frappe.throw(
				_("Row {0}: {1} is listed twice.").format(
					row.idx, frappe.bold(row.course_title or row.course)
				)
			)
		seen.add(row.course)


# ---------------------------------------------------------------- related and used in


def related_for_content(user: str, content: str) -> dict:
	groups = {k: [] for k in RELATION_ORDER}
	for rel in _relations_from(content):
		doctype, name = relation_target(rel)
		if rel.relation_type == "Prerequisite":
			continue  # shown separately with state
		item = _item(doctype, name)
		if item:
			groups[rel.relation_type].append(item)
	referenced_by = []
	for rel in frappe.get_all(
		"TCD Content Relation",
		filters={
			"target_type": "Content",
			"to_content": content,
			"relation_type": ("in", ["Related", "See Also"]),
		},
		fields=["from_content"],
		ignore_permissions=True,
	):
		item = _item("TCD Content", rel.from_content)
		if item and all(item["name"] != r["name"] for r in groups["Related"] + groups["See Also"]):
			referenced_by.append(item)
	return {
		"prerequisites": prerequisites(user, content),
		"next": groups["Next"],
		"related": groups["Related"] + groups["See Also"],
		"referenced_by": referenced_by,
		"used_in": used_in(content),
	}


def used_in(content: str) -> list[dict]:
	"""Tutorials, courses and learning paths that contain this content (readable ones)."""
	out = []
	from vintraxo_tcd.core.content import tutorials_for_lesson

	for tut in tutorials_for_lesson(content):
		item = _item("TCD Content", tut)
		if item:
			out.append(item)
	for course in course_svc.courses_with_content(content):
		item = _item("TCD Course", course)
		if item:
			out.append(item)
			for path in course_svc.paths_with_course(course):
				p = _item("TCD Learning Path", path)
				if p and all(p["name"] != o["name"] for o in out):
					out.append(p)
	return out


def related_for_course(course: str) -> list[dict]:
	"""Content that points to this course (any relation type), readable ones only."""
	out = []
	for rel in frappe.get_all(
		"TCD Content Relation",
		filters={"target_type": "Course", "to_course": course},
		fields=["from_content", "relation_type"],
		ignore_permissions=True,
	):
		item = _item("TCD Content", rel.from_content, relation_type=rel.relation_type)
		if item:
			out.append(item)
	return out


def course_navigation(user: str, course: str, content: str) -> dict:
	"""Previous / next readable item around `content` inside `course`."""
	items = [i["content"] for i in course_svc.course_items(course)]
	items = [c for c in items if c == content or frappe.has_permission("TCD Content", "read", c)]
	if content not in items:
		return {}
	i = items.index(content)
	nav = {}
	if i > 0:
		nav["prev"] = _item("TCD Content", items[i - 1])
	if i + 1 < len(items):
		nav["next"] = _item("TCD Content", items[i + 1])
	return {k: v for k, v in nav.items() if v}


# ---------------------------------------------------------------- unified search


def course_search_text(doc) -> str:
	parts = [doc.title, doc.summary]
	if doc.doctype == "TCD Course" and not doc.is_new():
		parts += frappe.get_all(
			"TCD Chapter", filters={"course": doc.name}, pluck="title", ignore_permissions=True
		)
	if doc.doctype == "TCD Learning Path":
		parts += [frappe.db.get_value("TCD Course", r.course, "title") or "" for r in doc.items]
	return normalize_text(" ".join(p for p in parts if p))


def refresh_course_search_text(course: str):
	doc = frappe.get_doc("TCD Course", course)
	doc.db_set("search_text", course_search_text(doc), update_modified=False)


SEARCH_TYPES = {
	"Lesson": ("TCD Content", {"content_type": "Lesson"}),
	"Article": ("TCD Content", {"content_type": "Article"}),
	"Tutorial": ("TCD Content", {"content_type": "Tutorial"}),
	"Reference": ("TCD Content", {"content_type": "Reference"}),
	"Course": ("TCD Course", {}),
	"Learning Path": ("TCD Learning Path", {}),
}


def search_all(
	query: str | None, types: list[str] | None = None, space: str | None = None, limit: int = 30
) -> list:
	terms = tokenize(query)
	if not terms:
		return []
	wanted = [t for t in (types or SEARCH_TYPES) if t in SEARCH_TYPES]
	phrase = " ".join(terms)
	results = []
	by_doctype: dict[str, list] = {}
	for t in wanted:
		doctype, extra = SEARCH_TYPES[t]
		by_doctype.setdefault(doctype, []).append(extra)
	for doctype, extras in by_doctype.items():
		filters = [[doctype, "search_text", "like", _like(term)] for term in terms]
		if space:
			filters.append([doctype, "space", "=", space])
		if doctype == "TCD Content" and len(extras) < 4:
			filters.append([doctype, "content_type", "in", [e["content_type"] for e in extras]])
		fields = ["name", "title", "summary", "space", "slug", "language", "modified", "search_text"]
		if doctype == "TCD Content":
			fields.append("content_type")
		for row in frappe.get_list(doctype, filters=filters, fields=fields, limit_page_length=200):
			row.doctype = doctype
			row.kind = row.get("content_type") or ("Course" if doctype == "TCD Course" else "Learning Path")
			row.content_type = row.kind
			row.score = _score(row, terms, phrase) + (2 if doctype != "TCD Content" else 0)
			row.snippet = snippet(row.search_text, terms)
			row.url = url_for(doctype, row.name)
			del row["search_text"]
			results.append(row)
	results.sort(key=lambda r: (-r.score, -r.modified.timestamp()))
	return results[: max(1, min(int(limit or 30), 100))]


# ---------------------------------------------------------------- recommendations


def recommendations(user: str, limit: int = 6) -> list[dict]:
	"""Simple and explainable: continue, follow-ups of completed content, popular courses."""
	out, seen = [], set()

	def add(item, reason):
		if item and item["name"] not in seen:
			seen.add(item["name"])
			out.append({**item, "reason": reason})

	# 1. next unlocked item of active course enrollments
	for e in readable_list(
		"TCD Enrollment", filters={"user": user, "status": "Active", "course": ("is", "set")}, pluck="course"
	):
		state = course_svc.course_status(user, e)
		for it in state["items"]:
			if not it["completed"] and not it["locked"]:
				add(_item("TCD Content", it["content"]), "continue")
				break

	# 2. Next / Related targets of completed content
	done = readable_list(
		"TCD Progress",
		filters={"user": user, "status": "Completed"},
		pluck="content",
		order_by="completed_on desc",
		limit_page_length=20,
	)
	for content in done:
		for rel in _relations_from(content):
			if rel.relation_type not in ("Next", "Related"):
				continue
			doctype, name = relation_target(rel)
			if doctype == "TCD Content" and name in done:
				continue
			if doctype != "TCD Content" and is_satisfied(user, doctype, name):
				continue
			add(_item(doctype, name), "follow_up")

	# 3. popular self-enrollable courses the user can read and is not enrolled in
	enrolled = set(
		frappe.get_all("TCD Enrollment", filters={"user": user}, pluck="course", ignore_permissions=True)
	)
	popular = frappe.get_all(
		"TCD Enrollment",
		filters={"course": ("is", "set")},
		fields=["course", {"COUNT": "*", "as": "n"}],
		group_by="course",
		order_by="n desc",
		limit_page_length=20,
		ignore_permissions=True,
	)
	candidates = [p.course for p in popular] + frappe.get_list(
		"TCD Course",
		filters={"status": "Published", "self_enrollment": 1},
		pluck="name",
		limit_page_length=20,
	)
	for course in candidates:
		if course in enrolled or not frappe.db.get_value("TCD Course", course, "self_enrollment"):
			continue
		if frappe.db.get_value("TCD Course", course, "status") != "Published":
			continue
		add(_item("TCD Course", course), "popular")
	return out[:limit]
