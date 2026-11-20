"""Space navigation (Phase 22, ADR-0030): a side menu the administrator arranges per space, like the
Frappe Wiki sidebar. Groups keep the order of their first row; learners only see items they can open."""

import frappe
from frappe import _

TARGETS = {
	"Page": ("content", "TCD Content"),
	"Course": ("course", "TCD Course"),
	"Learning Path": ("learning_path", "TCD Learning Path"),
}
MAX_ITEMS = 200


def validate(space):
	rows = space.get("navigation") or []
	if len(rows) > MAX_ITEMS:
		frappe.throw(_("The navigation can have at most {0} items.").format(MAX_ITEMS))
	for row in rows:
		row.group_title = (row.group_title or "").strip()
		if row.link_type == "External Link":
			row.content = row.course = row.learning_path = None
			if not (row.url or "").startswith(("https://", "/")):
				frappe.throw(_("Row {0}: the link must start with https:// or /.").format(row.idx))
			if not row.label:
				frappe.throw(_("Row {0}: an external link needs a label.").format(row.idx))
			continue
		field, doctype = TARGETS[row.link_type]
		for other, _dt in TARGETS.values():
			if other != field:
				row.set(other, None)
		row.url = None
		target = row.get(field)
		if not target:
			frappe.throw(_("Row {0}: choose the {1}.").format(row.idx, _(row.link_type, context="TCD")))
		if frappe.db.get_value(doctype, target, "space") != space.name:
			frappe.throw(_("Row {0}: {1} belongs to another space.").format(row.idx, frappe.bold(target)))


def outline(space_name: str, current: str | None = None) -> dict | None:
	"""The space menu for the current user, in the same shape as the lesson side menu."""
	from vintraxo_tcd.core.portal import content_url, course_url, path_url

	rows = frappe.get_all(
		"TCD Space Nav Item",
		filters={"parent": space_name, "parenttype": "TCD Space"},
		fields=["group_title", "link_type", "content", "course", "learning_path", "url", "label"],
		order_by="idx asc",
	)
	if not rows:
		return None
	groups: dict[str, list] = {}
	for r in rows:
		item = None
		if r.link_type == "External Link":
			item = {
				"title": r.label,
				"url": r.url,
				"state": "open",
				"current": False,
				"external": r.url.startswith("https://"),
			}
		else:
			field, doctype = TARGETS[r.link_type]
			name = r.get(field)
			if (
				not name
				or not frappe.db.exists(doctype, name)
				or not frappe.has_permission(doctype, "read", name)
			):
				continue
			t = frappe.db.get_value(doctype, name, ["title", "slug", "space", "status"], as_dict=True)
			if t.status != "Published" and not frappe.has_permission(doctype, "write", name):
				continue
			url = {"Page": content_url, "Course": course_url, "Learning Path": path_url}[r.link_type](
				t.space, t.slug
			)
			item = {
				"title": r.label or t.title,
				"url": url,
				"state": "open",
				"current": r.link_type == "Page" and name == current,
			}
		groups.setdefault(r.group_title, []).append(item)
	if not any(groups.values()):
		return None
	space = frappe.db.get_value("TCD Space", space_name, "title")
	return {
		"title": space,
		"url": content_url(space_name, "").rstrip("/"),
		"percent": None,
		"groups": [{"title": g, "items": items} for g, items in groups.items() if items],
	}
