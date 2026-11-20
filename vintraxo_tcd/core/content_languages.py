"""One item, several languages (Phase 31, ADR-0039).

Spaces, courses and pages that are translations of each other share a `translation_key`. Learners see one of
them (in their content language) and switch language with the buttons above the page; progress, enrollment and
the certificate follow them across languages.

- content language of a user: a user default ("tcd_content_language"), else their interface language.
- `collapse(rows, …)`: keep one row per translation group, the user's language first.
- `switcher(doctype, name)`: the language buttons for a page.
- `switch` (api): remember the language and go to the same place in it.
- `mirror_completion`: a completed lesson counts for its translations too.
- `sync_course`: switching to another language of an enrolled course enrolls there and copies progress.
"""

from urllib.parse import quote

import frappe
from frappe import _

LANGUAGE_NAMES = {"ar": "العربية", "en": "English"}
DEFAULT_KEY = "tcd_content_language"
DOCTYPES = ("TCD Space", "TCD Course", "TCD Content")


def preferred(user: str | None = None) -> str:
	user = user or frappe.session.user
	lang = frappe.defaults.get_user_default(DEFAULT_KEY, user) if user != "Guest" else None
	return lang or (frappe.local.lang or "ar")[:2]


def set_preferred(lang: str, user: str | None = None):
	if lang not in LANGUAGE_NAMES:
		frappe.throw(_("Unknown language."))
	user = user or frappe.session.user
	if user != "Guest":
		frappe.defaults.set_user_default(DEFAULT_KEY, lang, user)


def siblings(doctype: str, name: str) -> list[dict]:
	"""Every language version of an item (itself included): [{name, language}]."""
	key = frappe.db.get_value(doctype, name, "translation_key")
	if not key:
		return [{"name": name, "language": frappe.db.get_value(doctype, name, "language")}]
	return frappe.get_all(doctype, filters={"translation_key": key}, fields=["name", "language"])


def counterpart(doctype: str, name: str, lang: str) -> str | None:
	return next((s["name"] for s in siblings(doctype, name) if s["language"] == lang), None)


def collapse(rows: list, doctype: str, user: str | None = None, name_field: str = "name") -> list:
	"""Keep one row per translation group (the user's language if present), in the original order."""
	lang = preferred(user)
	names = [r.get(name_field) for r in rows if r.get(name_field)]
	if not names:
		return rows
	info = {
		r.name: r
		for r in frappe.get_all(
			doctype, filters={"name": ("in", names)}, fields=["name", "translation_key", "language"]
		)
	}
	best = {}
	for r in rows:
		meta = info.get(r.get(name_field))
		key = meta and meta.translation_key
		if not key:
			continue
		current = best.get(key)
		if current is None or (meta.language == lang and info[current.get(name_field)].language != lang):
			best[key] = r
	out = []
	for r in rows:
		meta = info.get(r.get(name_field))
		if not meta or not meta.translation_key or best.get(meta.translation_key) is r:
			out.append(r)
	return out


def switcher(doctype: str, name: str, course: str | None = None) -> list[dict]:
	"""Language buttons for a page; empty when the item has no other language."""
	versions = [s for s in siblings(doctype, name) if s["language"] in LANGUAGE_NAMES]
	if len(versions) < 2:
		return []
	current = frappe.db.get_value(doctype, name, "language")
	out = []
	for s in sorted(versions, key=lambda s: list(LANGUAGE_NAMES).index(s["language"])):
		if not frappe.has_permission(doctype, "read", s["name"]):
			continue
		out.append(
			{
				"lang": s["language"],
				"label": LANGUAGE_NAMES[s["language"]],
				"url": resolve_url(doctype, name, s["language"], course),  # works without JavaScript
				"current": s["language"] == current,
				"doctype": doctype,
				"name": name,
				"course": course or "",
			}
		)
	return out if len(out) > 1 else []


def resolve_url(doctype: str, name: str, lang: str, course: str | None = None) -> str:
	"""URL of the same space / course / page in `lang` (no side effects)."""
	from vintraxo_tcd.core.portal import content_url, course_url

	target = counterpart(doctype, name, lang) or name
	if doctype == "TCD Space":
		return f"/learn/{quote(target)}"
	if doctype == "TCD Course":
		space, slug = frappe.db.get_value("TCD Course", target, ["space", "slug"])
		return course_url(space, slug)
	space, slug = frappe.db.get_value("TCD Content", target, ["space", "slug"])
	url = content_url(space, slug)
	other_course = counterpart("TCD Course", course, lang) if course else None
	if other_course and frappe.has_permission("TCD Course", "read", other_course):
		url += "?course=" + quote(other_course)
	return url


def target_url(doctype: str, name: str, lang: str, course: str | None = None) -> str:
	"""Remember `lang`, follow the learner's course into it, and return the URL of the same item in it."""
	if doctype not in DOCTYPES:
		raise frappe.PermissionError
	frappe.has_permission(doctype, "read", name, throw=True)
	target = counterpart(doctype, name, lang) or name
	frappe.has_permission(doctype, "read", target, throw=True)
	set_preferred(lang)
	user = frappe.session.user
	if doctype == "TCD Course":
		sync_course(user, name, target)
	elif doctype == "TCD Content" and course:
		other_course = counterpart("TCD Course", course, lang)
		if other_course and frappe.has_permission("TCD Course", "read", other_course):
			sync_course(user, course, other_course)
	return resolve_url(doctype, name, lang, course)


# ---------------------------------------------------------------- progress follows the learner


def mirror_completion(user: str, content: str):
	"""A completed page counts for its other-language versions (no second quiz, no second completion)."""
	if frappe.flags.tcd_mirroring:
		return
	from vintraxo_tcd.core import courses
	from vintraxo_tcd.core.progress import _upsert

	frappe.flags.tcd_mirroring = True
	try:
		for s in siblings("TCD Content", content):
			if s["name"] == content:
				continue
			doc = _upsert(user, s["name"], status="Completed", percent=100)
			if not doc.completed_on:
				doc.db_set("completed_on", frappe.utils.now_datetime(), update_modified=False)
			courses.on_content_changed(user, s["name"])
	finally:
		frappe.flags.tcd_mirroring = False


def sync_course(user: str, source: str, target: str):
	"""Learner enrolled in `source` moves to its translation `target`: enroll there and copy completions."""
	if user == "Guest" or source == target:
		return
	from vintraxo_tcd.core import courses
	from vintraxo_tcd.core.progress import _upsert

	enrolled = frappe.db.get_value(
		"TCD Enrollment", {"user": user, "course": source, "status": ("!=", "Withdrawn")}, "name"
	)
	if not enrolled:
		return
	if not frappe.db.exists(
		"TCD Enrollment", {"user": user, "course": target, "status": ("!=", "Withdrawn")}
	):
		courses.enroll(user, "Course", target)
	done = set(frappe.get_all("TCD Progress", filters={"user": user, "status": "Completed"}, pluck="content"))
	frappe.flags.tcd_mirroring = True
	try:
		for item in courses.course_items(target):
			content = item.get("content")
			if not content or content in done:
				continue
			if any(s["name"] in done for s in siblings("TCD Content", content)):
				doc = _upsert(user, content, status="Completed", percent=100)
				if not doc.completed_on:
					doc.db_set("completed_on", frappe.utils.now_datetime(), update_modified=False)
		courses.refresh_course(user, target)
	finally:
		frappe.flags.tcd_mirroring = False


def has_sibling_certificate(user: str, course: str) -> bool:
	"""A learner gets one certificate for a course, whatever language they finished it in."""
	others = [s["name"] for s in siblings("TCD Course", course) if s["name"] != course]
	return bool(
		others
		and frappe.db.exists("TCD Certificate", {"user": user, "course": ("in", others), "status": "Active"})
	)
