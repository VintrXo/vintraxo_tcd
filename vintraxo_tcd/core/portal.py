"""Context builders for the learner portal (/learn)."""

from urllib.parse import quote

import frappe
from frappe import _

from vintraxo_tcd.core import progress
from vintraxo_tcd.core.search import search

CONTENT_LIST_FIELDS = ["name", "title", "slug", "summary", "content_type", "language", "category", "modified"]


# ---------------------------------------------------------------- guards


def require_portal():
	"""Portal must be enabled and the visitor logged in."""
	if not frappe.db.get_single_value("TCD Settings", "enable_portal"):
		raise frappe.PageDoesNotExistError
	if frappe.session.user == "Guest":
		request = getattr(frappe.local, "request", None)
		path = request.full_path.rstrip("?") if request else "/learn"
		frappe.local.flags.redirect_location = "/login?redirect-to=" + quote(path)
		raise frappe.Redirect(302)  # never 301: browsers cache it and keep redirecting after login


def get_space(name: str):
	if not name or not frappe.db.exists("TCD Space", name):
		raise frappe.PageDoesNotExistError
	space = frappe.get_doc("TCD Space", name)
	if not frappe.has_permission("TCD Space", "read", space):
		raise frappe.PageDoesNotExistError  # do not reveal hidden spaces
	return space


def get_content_by_slug(space: str, slug: str):
	name = frappe.db.get_value("TCD Content", {"space": space, "slug": slug})
	if not name:
		raise frappe.PageDoesNotExistError
	doc = frappe.get_doc("TCD Content", name)
	if not frappe.has_permission("TCD Content", "read", doc):
		raise frappe.PageDoesNotExistError
	return doc


def content_url(space: str, slug: str, tutorial: str | None = None) -> str:
	url = f"/learn/{quote(space)}/{quote(slug)}"
	return f"{url}?tutorial={quote(tutorial)}" if tutorial else url


def direction(language: str | None) -> str:
	return "rtl" if (language or "ar") == "ar" else "ltr"


# ---------------------------------------------------------------- pages


def home_context(query: str | None = None) -> dict:
	user = frappe.session.user
	spaces = frappe.get_list(
		"TCD Space",
		filters={"is_active": 1},
		fields=["name", "title", "description", "visibility"],
		order_by="title asc",
	)
	ctx = {"spaces": spaces, "query": query or "", "results": None}

	in_progress = frappe.get_list(
		"TCD Progress",
		filters={"user": user, "status": "In Progress"},
		fields=["content", "percent", "last_viewed_on"],
		order_by="last_viewed_on desc",
		limit_page_length=6,
	)
	ctx["continue_learning"] = _attach_content(in_progress)

	if query:
		rows = search(query, limit=50)
		for row in rows:
			row.url = content_url(row.space, row.slug)
		ctx["results"] = rows
	return ctx


def _attach_content(rows) -> list:
	out = []
	for row in rows:
		if not frappe.has_permission("TCD Content", "read", row.content):
			continue
		c = frappe.db.get_value(
			"TCD Content", row.content, ["title", "slug", "space", "content_type"], as_dict=True
		)
		row.update(c)
		row.url = content_url(c.space, c.slug)
		out.append(row)
	return out


def space_context(space_name: str) -> dict:
	space = get_space(space_name)
	user = frappe.session.user
	rows = frappe.get_list(
		"TCD Content",
		filters={"space": space.name},
		fields=[*CONTENT_LIST_FIELDS, "status"],
		order_by="title asc",
		limit_page_length=500,
	)
	status = dict(
		frappe.get_all(
			"TCD Progress",
			filters={"user": user, "content": ("in", [r.name for r in rows] or [""])},
			fields=["content", "status"],
			as_list=True,
		)
	)
	categories = {
		c.name: c
		for c in frappe.get_list(
			"TCD Category",
			filters={"space": space.name},
			fields=["name", "category_name", "sort_order"],
		)
	}
	groups: dict[str, dict] = {}
	for row in rows:
		row.url = content_url(space.name, row.slug)
		row.progress = status.get(row.name, "Not Started")
		cat = categories.get(row.category)
		key = cat.name if cat else ""
		group = groups.setdefault(
			key,
			{
				"title": cat.category_name if cat else _("General"),
				"sort": (0 if cat else 1, cat.sort_order if cat else 0),
				"tutorials": [],
				"items": [],
			},
		)
		(group["tutorials"] if row.content_type == "Tutorial" else group["items"]).append(row)

	return {
		"space": space,
		"groups": sorted(groups.values(), key=lambda g: (g["sort"], g["title"])),
		"title": space.title,
		"parents": [{"route": "/learn", "title": _("Learning")}],
	}


def content_context(space_name: str, slug: str, tutorial: str | None = None) -> dict:
	from vintraxo_tcd import api

	space = get_space(space_name)
	doc = get_content_by_slug(space.name, slug)
	lesson = api.get_lesson(doc.name, tutorial=tutorial)
	user = frappe.session.user
	parents = [
		{"route": "/learn", "title": _("Learning")},
		{"route": content_url(space.name, ""), "title": space.title},
	]

	nav = {}
	if tutorial and ("prev" in lesson or "next" in lesson):
		tut = frappe.db.get_value("TCD Content", tutorial, ["title", "slug"], as_dict=True)
		parents.append({"route": content_url(space.name, tut.slug), "title": tut.title})
		for key in ("prev", "next"):
			if lesson.get(key):
				target = frappe.db.get_value("TCD Content", lesson[key], ["title", "slug"], as_dict=True)
				nav[key] = {"title": target.title, "url": content_url(space.name, target.slug, tutorial)}

	if lesson.get("tutorial"):
		for item in lesson["tutorial"]["lessons"]:
			item["url"] = content_url(space.name, item["slug"], doc.name)

	quiz_required = bool(progress.required_quiz(doc.name))
	return {
		"space": space,
		"doc": doc,
		"lesson": lesson,
		"nav": nav,
		"dir": direction(doc.language),
		"title": doc.title,
		"parents": [{**p, "route": p["route"].rstrip("/")} for p in parents],
		"can_complete": doc.content_type != "Tutorial"
		and lesson["progress"] != "Completed"
		and not (quiz_required and not (lesson["quiz"] or {}).get("passed")),
		"quiz_required": quiz_required,
		"is_staff_preview": doc.status != "Published",
		"user": user,
		"js_labels": js_labels(),
	}


def js_labels() -> dict:
	"""UI strings for portal JS, translated on the server."""
	return {
		"run": _("Run"),
		"stop": _("Stop"),
		"reset": _("Reset"),
		"running": _("Running..."),
		"loading_runtime": _("Loading runtime (first run can take a few seconds)..."),
		"done_in": _("Done in {0} ms"),
		"timeout": _("Stopped: time limit of {0} seconds reached."),
		"stopped": _("Stopped."),
		"no_output": _("(no output)"),
		"output_matches": _("Output matches the expected result."),
		"output_differs": _("Output differs from the expected result."),
		"error": _("Error"),
		"completed": _("Completed", context="TCD"),
		"mark_complete": _("Mark as complete"),
		"submit": _("Submit answers"),
		"score": _("Score: {0} / {1} ({2}%)"),
		"passed": _("Passed"),
		"failed": _("Not passed yet"),
		"attempts_left": _("Attempts left: {0}"),
		"no_attempts": _("No attempts left."),
		"correct": _("Correct"),
		"wrong": _("Wrong"),
		"correct_answer": _("Correct answer"),
		"try_again": _("Try again"),
		"true": _("True"),
		"false": _("False"),
		"preview": _("Preview"),
	}


def json_for_script(data) -> str:
	"""JSON safe to embed inside <script type="application/json">."""
	return (
		frappe.as_json(data, indent=None)
		.replace("<", "\\u003c")
		.replace(">", "\\u003e")
		.replace("&", "\\u0026")
	)
