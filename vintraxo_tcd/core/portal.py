"""Context builders for the learner portal (/learn)."""

from urllib.parse import quote

import frappe
from frappe import _

from vintraxo_tcd.core import governance, progress
from vintraxo_tcd.core.permissions import readable_list
from vintraxo_tcd.core.search import search

CONTENT_LIST_FIELDS = ["name", "title", "slug", "summary", "content_type", "language", "category", "modified"]


# ---------------------------------------------------------------- guards


def require_portal(allow_guest: bool = False):
	"""Portal must be enabled and the visitor logged in (or a reading page with visitors allowed)."""
	if not frappe.db.get_single_value("TCD Settings", "enable_portal"):
		raise frappe.PageDoesNotExistError
	if (
		frappe.session.user == "Guest"
		and allow_guest
		and frappe.db.get_single_value("TCD Settings", "enable_guest_access")
	):
		return
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


def course_url(space: str, slug: str) -> str:
	return f"/learn/{quote(space)}/course/{quote(slug)}"


def path_url(space: str, slug: str) -> str:
	return f"/learn/{quote(space)}/path/{quote(slug)}"


def direction(language: str | None) -> str:
	return "rtl" if (language or "ar") == "ar" else "ltr"


def portal_page(build):
	"""Wrap a www get_context: hidden/missing pages render our own 404 with a real 404 status.

	Frappe's generic 404 page can be replaced by other apps (e.g. Builder) without setting the
	status code, so we never rely on it.
	"""

	def get_context(context):
		try:
			build(context)
			_escape_breadcrumbs(context)
		except frappe.PageDoesNotExistError:
			context.http_status_code = 404
			context.title = _("Page not found")
			context.template = "templates/includes/tcd_not_found.html"
			context.show_sidebar = False

	return get_context


def _escape_breadcrumbs(context):
	"""Frappe's breadcrumb template prints the page and parent titles without escaping, and titles come
	from content (Frappe keeps harmless tags such as <b> in Data fields). Escape them once here."""
	from frappe.utils import escape_html

	if context.get("title"):
		context.title = escape_html(str(context.title))
	for parent in context.get("parents") or []:
		if parent.get("title"):
			parent["title"] = escape_html(str(parent["title"]))


# ---------------------------------------------------------------- pages


def home_context(
	query: str | None = None, types: str | None = None, space: str | None = None, tag: str | None = None
) -> dict:
	user = frappe.session.user
	spaces = frappe.get_list(
		"TCD Space",
		filters={"is_active": 1},
		fields=["name", "title", "description", "visibility"],
		order_by="title asc",
	)
	from vintraxo_tcd.core import content_languages

	spaces = content_languages.collapse(
		spaces, "TCD Space", user
	)  # one card per space, in the user's language
	ctx = {"spaces": spaces, "query": query or "", "results": None}
	from vintraxo_tcd.core import ai

	ctx["ai_enabled"] = ai.can_use(user)
	from vintraxo_tcd.core import teams

	ctx["is_manager"] = teams.is_manager(user)
	ctx["labels_json"] = json_for_script(js_labels())

	in_progress = readable_list(
		"TCD Progress",
		filters={"user": user, "status": "In Progress"},
		fields=["content", "percent", "last_viewed_on"],
		order_by="last_viewed_on desc",
		limit_page_length=12,
	)
	ctx["continue_learning"] = _attach_content(_in_language(in_progress, user))[:6]
	ctx["my_enrollments"] = my_enrollments(user)
	ctx["catalog"] = catalog(spaces, user)
	ctx["is_instructor"] = "TCD Instructor" in frappe.get_roles(
		user
	) or "TCD Administrator" in frappe.get_roles(user)

	from vintraxo_tcd.core.connect import SEARCH_TYPES, search_all

	selected = [t for t in (types or "").split(",") if t in SEARCH_TYPES]
	ctx["search_types"] = list(SEARCH_TYPES)
	ctx["selected_types"] = selected
	ctx["selected_space"] = space if space in {s.name for s in spaces} else ""
	if query:
		ctx["results"] = search_all(query, selected or None, ctx["selected_space"] or None, limit=50)
	if tag:
		from vintraxo_tcd.core import wiki
		from vintraxo_tcd.core.connect import _item

		ctx["tag"] = tag
		ctx["results"] = [i for i in (_item("TCD Content", n) for n in wiki.contents_with_tag(tag)) if i]
		ctx["query"] = ctx["query"] or ""
	return ctx


CATALOG_ORDER = ("Programming", "Web", "Data", "Mathematics", "Marketing", "Business", "")
# short label shown on the course card icon, by translation key (others show their category icon)
COURSE_BADGES = {
	"intro-programming": "</>", "python": "Py", "java": "Java", "cpp": "C++", "c": "C", "csharp": "C#",
	"go": "Go", "rust": "Rs", "kotlin": "Kt", "php": "PHP", "bash": "$_", "dsa": "DSA", "git": "Git",
	"html": "HTML", "css": "CSS", "javascript": "JS", "bootstrap": "BS", "react": "Re", "vue": "Vue",
	"jquery": "jQ", "typescript": "TS", "json-xml": "{ }", "sql": "SQL", "numpy": "NP", "pandas": "pd",
	"r": "R", "odoo": "Odoo",
}  # fmt: skip


def catalog(spaces: list, user: str) -> list:
	"""Spaces grouped by category for the learner home page: [{key, label, spaces}], each space with its
	number of published pages and the learner's progress in its course (0 when not enrolled)."""
	names = [s.name for s in spaces]
	if not names:
		return []
	meta = {
		r.name: r
		for r in frappe.get_all(
			"TCD Space",
			filters={"name": ("in", names)},
			fields=["name", "category", "language", "translation_key"],
		)
	}
	counts = dict(
		frappe.get_all(
			"TCD Content",
			filters={"space": ("in", names), "status": "Published"},
			fields=["space", {"COUNT": "*", "as": "n"}],
			group_by="space",
			as_list=True,
		)
	)
	progress = {}
	if user != "Guest":
		from vintraxo_tcd.core import content_languages

		for e in frappe.get_all(
			"TCD Enrollment",
			filters={"user": user, "status": ("!=", "Withdrawn"), "course": ("is", "set")},
			fields=["course", "percent"],
		):
			for sib in content_languages.siblings("TCD Course", e.course):  # progress shows in any language
				space = frappe.db.get_value("TCD Course", sib["name"], "space")
				progress[space] = max(progress.get(space, 0), int(e.percent or 0))
	groups = {}
	for s in spaces:
		m = meta.get(s.name) or frappe._dict()
		key = m.category if m.category in CATALOG_ORDER else ""
		s.category = key
		s.lessons = counts.get(s.name, 0)
		s.progress = progress.get(s.name, 0)
		s.language = m.language
		s.short = COURSE_BADGES.get(m.translation_key or "")
		groups.setdefault(key, []).append(s)
	labels = {
		"Programming": _("Programming"),
		"Web": _("Web development"),
		"Data": _("Data and databases"),
		"Mathematics": _("Mathematics"),
		"Marketing": _("Marketing"),
		"Business": _("Business systems"),
		"": _("More to explore"),
	}
	return [
		{"key": k or "other", "label": labels[k], "spaces": groups[k]} for k in CATALOG_ORDER if k in groups
	]


def _in_language(rows, user: str) -> list:
	"""Show each lesson in the learner's content language, once (a lesson read in two languages is one item)."""
	from vintraxo_tcd.core import content_languages

	lang = content_languages.preferred(user)
	out, seen = [], set()
	for row in rows:
		other = content_languages.counterpart("TCD Content", row.content, lang)
		if other and other != row.content and frappe.has_permission("TCD Content", "read", other):
			row.content = other
		if row.content not in seen:
			seen.add(row.content)
			out.append(row)
	return out


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
	from vintraxo_tcd.core import navigation

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

	offerings = []
	for doctype, kind, url in (("TCD Learning Path", "path", path_url), ("TCD Course", "course", course_url)):
		extra = ["coming_soon"] if kind == "course" else []
		rows_o = frappe.get_list(
			doctype,
			filters={"space": space.name},
			fields=["name", "title", "slug", "summary", "language", "status", "cover_image", *extra],
			order_by="title asc",
			limit_page_length=200,
		)
		field = "learning_path" if kind == "path" else "course"
		mine = dict(
			frappe.get_all(
				"TCD Enrollment",
				filters={"user": user, field: ("in", [r.name for r in rows_o] or [""])},
				fields=[field, "status"],
				as_list=True,
			)
		)
		for r in rows_o:
			r.kind = kind
			r.url = url(space.name, r.slug)
			r.enrollment = mine.get(r.name)
			offerings.append(r)

	from vintraxo_tcd.core import content_languages, wiki

	return {
		"lang_switcher": content_languages.switcher("TCD Space", space.name),
		"space": space,
		"page_tree": wiki.page_tree(space.name),
		"outline": navigation.outline(space.name),
		"offerings": offerings,
		"groups": sorted(groups.values(), key=lambda g: (g["sort"], g["title"])),
		"title": space.title,
		"parents": [{"route": "/learn", "title": _("Learning")}],
	}


def content_context(
	space_name: str, slug: str, tutorial: str | None = None, course: str | None = None
) -> dict:
	from vintraxo_tcd import api
	from vintraxo_tcd.core import courses as course_svc

	space = get_space(space_name)
	doc = get_content_by_slug(space.name, slug)
	lesson = api.get_lesson(doc.name, tutorial=tutorial)
	user = frappe.session.user
	from vintraxo_tcd.core import wiki

	lesson["blocks"] = wiki.prepare_blocks(lesson["blocks"], space.name)
	lesson["toc"] = wiki.table_of_contents(lesson["blocks"])
	parents = [
		{"route": "/learn", "title": _("Learning")},
		{"route": content_url(space.name, ""), "title": space.title},
	]
	if not tutorial and not course:
		parents += [
			{"route": content_url(a.space, a.slug), "title": a.title} for a in wiki.ancestors(doc.name)
		]

	nav = {}
	if tutorial and ("prev" in lesson or "next" in lesson):
		tut = frappe.db.get_value("TCD Content", tutorial, ["title", "slug"], as_dict=True)
		parents.append({"route": content_url(space.name, tut.slug), "title": tut.title})
		for key in ("prev", "next"):
			if lesson.get(key):
				target = frappe.db.get_value("TCD Content", lesson[key], ["title", "slug"], as_dict=True)
				nav[key] = {"title": target.title, "url": content_url(space.name, target.slug, tutorial)}

	if (
		course
		and frappe.db.exists("TCD Course", course)
		and frappe.has_permission("TCD Course", "read", course)
	):
		c = frappe.db.get_value("TCD Course", course, ["title", "slug"], as_dict=True)
		parents.append({"route": course_url(space.name, c.slug), "title": c.title})
	blockers = course_svc.sequence_blockers(user, doc.name)
	from vintraxo_tcd.core import connect

	related = connect.related_for_content(user, doc.name)
	unmet = connect.unmet_prerequisites(user, doc.name)
	if course and not nav:
		cnav = connect.course_navigation(user, course, doc.name)
		for key, item in cnav.items():
			nav[key] = {"title": item["title"], "url": item["url"] + "?course=" + quote(course)}

	if lesson.get("tutorial"):
		for item in lesson["tutorial"]["lessons"]:
			item["url"] = content_url(space.name, item["slug"], doc.name)

	outline = lesson_outline(user, doc, space.name, tutorial, course)
	quiz_required = bool(progress.required_quiz(doc.name))
	from vintraxo_tcd.core import change_requests, content_languages, freshness, notes

	return {
		"lang_switcher": content_languages.switcher("TCD Content", doc.name, course),
		"outdated": doc.status == "Published" and freshness.is_overdue(doc),
		"my_note": notes.get(doc.name, user) if user != "Guest" else None,
		"suggest_fields": change_requests.editable_fields(doc)
		if user != "Guest" and doc.status == "Published" and change_requests.enabled()
		else None,
		"discussions_enabled": bool(frappe.db.get_single_value("TCD Settings", "enable_discussions"))
		and user != "Guest",
		"space": space,
		"doc": doc,
		"lesson": lesson,
		"nav": nav,
		"outline": outline,
		"dir": direction(doc.language),
		"title": doc.title,
		"parents": [{**p, "route": p["route"].rstrip("/")} for p in parents],
		"can_complete": doc.content_type != "Tutorial"
		and lesson["progress"] != "Completed"
		and not (quiz_required and not (lesson["quiz"] or {}).get("passed"))
		and not blockers
		and not unmet
		and not lesson.get("opens_on"),
		"quiz_required": quiz_required,
		"sequence_blockers": blockers,
		"unmet_prerequisites": unmet,
		"related": related,
		"backlinks": wiki.backlinks(doc.name),
		"policies": governance.related_for_content(doc.name, user),
		"children": [
			c
			for c in frappe.get_list(
				"TCD Content",
				filters={"parent_content": doc.name},
				fields=["name", "title", "slug", "content_type"],
				order_by="title asc",
			)
		],
		"tags": wiki.tags_of(doc.name),
		"feedback": wiki.feedback_stats(doc.name),
		"my_feedback": frappe.db.get_value(
			"TCD Content Feedback", {"content": doc.name, "user": user}, ["helpful", "comment"], as_dict=True
		),
		"is_staff_preview": doc.status != "Published",
		"user": user,
		"js_labels": js_labels(),
	}


def lesson_outline(user: str, doc, space: str, tutorial: str | None, course: str | None) -> dict | None:
	"""Side menu of the lesson page (Phase 17): every item of the course or tutorial being followed,
	with its state. Only items the user can read are listed."""
	if (
		course
		and frappe.db.exists("TCD Course", course)
		and frappe.has_permission("TCD Course", "read", course)
	):
		from vintraxo_tcd.core import courses as course_svc

		c = frappe.db.get_value("TCD Course", course, ["title", "slug", "space"], as_dict=True)
		status = course_svc.course_status(user, course)
		groups = []
		for ch in status["chapters"]:
			items = []
			for it in ch["items"]:
				if it["content"] != doc.name and not frappe.has_permission(
					"TCD Content", "read", it["content"]
				):
					continue
				t = frappe.db.get_value(
					"TCD Content", it["content"], ["title", "slug", "space"], as_dict=True
				)
				items.append(
					{
						"title": t.title,
						"url": content_url(t.space, t.slug) + "?course=" + quote(course),
						"state": "completed" if it["completed"] else ("locked" if it["locked"] else "open"),
						"current": it["content"] == doc.name,
					}
				)
			if items:
				groups.append({"title": ch["title"], "items": items})
		return {
			"title": c.title,
			"url": course_url(c.space, c.slug),
			"percent": status["percent"],
			"groups": groups,
		}
	owner = tutorial or (doc.name if doc.content_type == "Tutorial" else None)
	if (
		owner
		and frappe.db.exists("TCD Content", owner)
		and frappe.has_permission("TCD Content", "read", owner)
	):
		summary = progress.tutorial_summary(user, owner)
		t = frappe.db.get_value("TCD Content", owner, ["title", "slug"], as_dict=True)
		items = [
			{
				"title": item["title"],
				"url": content_url(space, item["slug"], owner),
				"state": "completed" if item["status"] == "Completed" else "open",
				"current": item["lesson"] == doc.name,
			}
			for item in summary["lessons"]
		]
		return {
			"title": t.title,
			"url": content_url(space, t.slug),
			"percent": summary["percent"],
			"groups": [{"title": None, "items": items}],
		}
	from vintraxo_tcd.core import navigation

	return navigation.outline(space, doc.name)  # wiki pages: the space menu, if the admin set one


def js_labels() -> dict:
	"""UI strings for portal JS, translated on the server."""
	return {
		"run": _("Run"),
		"stop": _("Stop"),
		"reset": _("Reset"),
		"running": _("Running..."),
		"loading_runtime": _("Loading runtime (first run can take a few seconds)..."),
		"runner_off": _(
			"This example runs once the code runner is enabled. You can still read and edit the code."
		),
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
		"booked": _("Booked. The evaluator has been notified."),
		"interest_on": _("We will notify you when it opens."),
		"confirm_cancel_evaluation": _("Cancel this evaluation?"),
		"result_saved": _("Result saved."),
		"md_bold": _("Bold"),
		"md_italic": _("Italic"),
		"md_heading": _("Heading", context="TCD Block"),
		"md_list": _("List", context="TCD Block"),
		"md_link": _("Link"),
		"md_code": _("Code", context="TCD Block"),
		"copy": _("Copy", context="TCD"),
		"copied": _("Copied", context="TCD"),
		"full_screen": _("Full screen", context="TCD"),
		"exit_full_screen": _("Exit full screen", context="TCD"),
		"exercise_correct": _("Well done! All blanks are correct."),
		"exercise_partly": _("{0} of {1} blanks are correct. Try again."),
		"theme_dark": _("Dark mode"),
		"theme_light": _("Light mode"),
		"enrolled": _("Enrolled"),
		"uploading": _("Uploading..."),
		"saved": _("Saved."),
		"choose_rating": _("Choose a rating."),
		"thanks": _("Thank you for your feedback."),
		"pending_review": _("Some answers are waiting for review by your instructor."),
		"waiting_review": _("Waiting for review"),
		"time_limit": _("Time limit: {0} minutes"),
		"time_left": _("Time left: {0}"),
		"time_over": _("Time is over"),
		"start_quiz": _("Start the quiz"),
		"blank_n": _("Blank {0}"),
		"move_up": _("Move up"),
		"move_down": _("Move down"),
		"code_note": _("Run your code before submitting; the output is checked."),
		"manual_note": _("An instructor reviews this answer."),
		"thinking": _("Looking in the pages you can access..."),
		"running_on_server": _("Running on the code runner..."),
		"ask": _("Ask", context="TCD"),
		"reply": _("Reply"),
		"no_questions": _("No questions yet. Be the first to ask."),
		"staff_answer": _("Staff answer"),
		"best_answer": _("Best answer"),
		"mark_best": _("Mark as best answer"),
		"hide": _("Hide"),
		"show": _("Show", context="TCD"),
		"hidden_post": _("Hidden"),
		"your_question": _("Your question about this page"),
		"your_reply": _("Your reply"),
		"suggestion_sent": _("Thank you. A reviewer will check your suggestion."),
		"proctor_note": _(
			"This quiz is proctored: leaving this page or pasting text counts as a violation ({0} allowed)."
		),
		"proctor_warning": _(
			"Warning: you left the quiz or pasted text ({0} of {1}). At the limit the quiz is submitted."
		),
		"negative_note": _(
			"Wrong answers to choice questions take points away. You can leave a question blank."
		),
		"examples": _("Examples"),
		"input": _("Input"),
		"expected": _("Expected output"),
		"cases_passed": _("Test cases passed: {0} of {1}"),
		"runner_compilation_error": _("Compilation error"),
		"runner_runtime_error": _("Runtime error"),
		"runner_time_limit": _("Stopped: time limit reached."),
		"runner_error": _("The code runner could not run the code."),
		"sources": _("Sources"),
		"no_results": _("Nothing found. Try a shorter word."),
		"related_terms": _("Also searched for: {0}"),
	}


def json_for_script(data) -> str:
	"""JSON safe to embed inside <script type="application/json">."""
	return (
		frappe.as_json(data, indent=None)
		.replace("<", "\\u003c")
		.replace(">", "\\u003e")
		.replace("&", "\\u0026")
	)


# ---------------------------------------------------------------- courses and paths (Phase 1)


def my_enrollments(user: str) -> list:
	rows = readable_list(
		"TCD Enrollment",
		filters={"user": user, "status": ("!=", "Withdrawn")},
		fields=["name", "enrollment_for", "course", "learning_path", "status", "percent", "due_date"],
		order_by="modified desc",
		limit_page_length=20,
	)
	out = []
	for r in rows:
		doctype = "TCD Course" if r.course else "TCD Learning Path"
		target = r.course or r.learning_path
		if not frappe.has_permission(doctype, "read", target):
			continue
		t = frappe.db.get_value(doctype, target, ["title", "slug", "space"], as_dict=True)
		r.title = t.title
		r.url = (course_url if r.course else path_url)(t.space, t.slug)
		out.append(r)
	from vintraxo_tcd.core import content_languages

	courses = content_languages.collapse(
		[r for r in out if r.course], "TCD Course", user, name_field="course"
	)
	return [r for r in out if not r.course or r in courses]  # one row per course, in the learner's language


def _offering_by_slug(doctype: str, space: str, slug: str):
	name = frappe.db.get_value(doctype, {"space": space, "slug": slug})
	if not name or not frappe.has_permission(doctype, "read", name):
		raise frappe.PageDoesNotExistError
	return frappe.get_doc(doctype, name)


def course_context(space_name: str, slug: str) -> dict:
	from vintraxo_tcd import api
	from vintraxo_tcd.core import courses as course_svc
	from vintraxo_tcd.core import evaluations

	space = get_space(space_name)
	course = _offering_by_slug("TCD Course", space.name, slug)
	data = api.get_course(course.name)
	for ch in data["chapters"]:
		for item in ch["items"]:
			item["url"] = content_url(space.name, item["slug"]) + "?course=" + quote(course.name)
	from vintraxo_tcd.core import connect

	user = frappe.session.user
	prereqs = []
	for row in course.get("prerequisites") or []:
		item = connect._item(
			"TCD Course", row.course, satisfied=connect.is_satisfied(user, "TCD Course", row.course)
		)
		if item:
			prereqs.append(item)
	from vintraxo_tcd.core import content_languages, sessions

	return {
		"lang_switcher": content_languages.switcher("TCD Course", course.name),
		"sessions": sessions.for_course(course.name, user),
		"space": space,
		"doc": course,
		"data": data,
		"dir": direction(course.language),
		"title": course.title,
		"parents": [
			{"route": "/learn", "title": _("Learning")},
			{"route": content_url(space.name, "").rstrip("/"), "title": space.title},
		],
		"is_staff_preview": course.status != "Published",
		"prerequisites": prereqs,
		"unmet_prerequisites": [p["title"] for p in prereqs if not p["satisfied"]],
		"referenced_by": connect.related_for_course(course.name),
		"policies": governance.related_for_course(course.name, user),
		"certificate": frappe.db.get_value(
			"TCD Certificate",
			{"user": user, "course": course.name, "status": ("in", ["Active", "Expired"])},
			["name", "verification_code", "status"],
			as_dict=True,
		),
		"evaluation": evaluations.state(user, course.name),
		"interested": user != "Guest"
		and course.get("coming_soon")
		and course_svc.is_interested(user, course.name),
		"js_labels": js_labels(),
	}


def path_context(space_name: str, slug: str) -> dict:
	from vintraxo_tcd import api

	space = get_space(space_name)
	path = _offering_by_slug("TCD Learning Path", space.name, slug)
	data = api.get_learning_path(path.name)
	for c in data["courses"]:
		c["url"] = course_url(space.name, c["slug"])
	return {
		"space": space,
		"doc": path,
		"data": data,
		"dir": direction(path.language),
		"title": path.title,
		"parents": [
			{"route": "/learn", "title": _("Learning")},
			{"route": content_url(space.name, "").rstrip("/"), "title": space.title},
		],
		"is_staff_preview": path.status != "Published",
		"js_labels": js_labels(),
	}


# ---------------------------------------------------------------- static asset versions


def asset_version() -> str:
	"""Cache-busting token for the app's own portal JS/CSS (they are served with a 12-hour cache).
	Changes whenever one of the files changes, without needing a bench build."""
	import os

	base = frappe.get_app_path("vintraxo_tcd", "public")
	latest = 0.0
	for folder in ("js", "css"):
		path = os.path.join(base, folder)
		if os.path.isdir(path):
			for name in os.listdir(path):
				latest = max(latest, os.path.getmtime(os.path.join(path, name)))
	return str(int(latest))
