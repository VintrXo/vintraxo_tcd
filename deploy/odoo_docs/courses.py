"""One course per Odoo app (≥ 3 pages) in each Odoo docs space: chapters = the app's sections, lessons = the
section page and everything under it, in Odoo's own order (the order of the links on each parent page).
Run inside the site, after load.py:

    echo "exec(open('deploy/odoo_docs/courses.py').read(), {'__name__': '__main__'})" | bench --site <site> console

Idempotent: an app that already has a course (same title in the space) is skipped."""

import json
import re

import frappe

from vintraxo_tcd.core import studio

SPACES = {"odoo-en": "en", "odoo-ar": "ar"}
MIN_PAGES = 3
INTRO = {"en": "Introduction", "ar": "مقدمة"}
LESSONS = {"en": "Lessons", "ar": "الدروس"}
NOT_COURSES = {"finance-fiscal-localizations"}  # per-country reference, not a course
SUFFIX = {"en": " — Odoo 18 course", "ar": " — دورة أودو 18"}
LINK = re.compile(r"\[\[([^\[\]|]+)\|")


def tree(space):
	rows = frappe.get_all(
		"TCD Content",
		filters={"space": space, "status": "Published"},
		fields=["name", "title", "slug", "parent_content", "summary", "blocks"],
	)
	by_name = {r.name: r for r in rows}
	kids = {}
	for r in rows:
		kids.setdefault(r.parent_content, []).append(r)
	for parent, children in kids.items():  # Odoo's order: where the parent page links to each child
		text = by_name[parent].blocks if parent in by_name else ""
		order = {slug: i for i, slug in enumerate(LINK.findall(text or ""))}
		children.sort(key=lambda c: (order.get(c.slug, 10**6), c.title))
	return by_name, kids


def subtree(node, kids):
	out = [node]
	for child in kids.get(node.name, []):
		out.extend(subtree(child, kids))
	return out


def main():
	frappe.set_user("Administrator")
	if not getattr(frappe.local, "lang", None):
		frappe.local.lang = "en"
	for space, lang in SPACES.items():
		if not frappe.db.exists("TCD Space", space):
			continue
		by_name, kids = tree(space)
		roots = [r for r in by_name.values() if not r.parent_content]
		areas = [c for root in roots for c in kids.get(root.name, [])]  # Finance, Sales, ...
		made = skipped = 0
		for area in areas:
			for app in kids.get(area.name, []):  # Accounting, Invoicing, ...
				pages = subtree(app, kids)
				if len(pages) < MIN_PAGES or app.slug in NOT_COURSES:
					continue
				title = (app.title + SUFFIX[lang])[:140]
				if frappe.db.exists("TCD Course", {"space": space, "title": title}):
					skipped += 1
					continue
				sections = kids.get(app.name, [])
				if all(not kids.get(s.name) for s in sections):  # flat app: one chapter of lessons
					chapters = [
						{"title": INTRO[lang], "items": [{"content": app.name}]},
						{"title": LESSONS[lang], "items": [{"content": s.name} for s in sections]},
					]
				else:
					chapters = [{"title": INTRO[lang], "items": [{"content": app.name}]}]
					for section in sections:
						items = [{"content": p.name} for p in subtree(section, kids)]
						chapters.append({"title": section.title[:140], "items": items})
				if len(chapters) > studio.MAX_CHAPTERS or len(pages) > studio.MAX_ITEMS:
					print(f"  {space}: {app.title} too large ({len(chapters)} chapters, {len(pages)} pages), skipped")
					continue
				course = studio.save_course(
					{
						"space": space,
						"title": title,
						"language": lang,
						"visibility": "Public",
						"summary": (app.summary or "")[:300],
						"self_enrollment": 1,
						"completion_rule": "All Items",
						"access": "Open",
						"chapters": chapters,
					}
				)
				frappe.db.set_value("TCD Course", course["name"], "translation_key", f"odoo-course:{app.slug}")  # Phase 31
				studio.set_course_status(course["name"], "Published")
				frappe.db.commit()
				made += 1
		print(f"{space}: {made} courses created, {skipped} already there", flush=True)


main()
