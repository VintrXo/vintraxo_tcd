"""Programming library (Phase 30, ADR-0038): courses written as source files in `library/<course>/` become spaces.

    bench --site <site> execute vintraxo_tcd.core.library.load_library
    bench --site <site> execute vintraxo_tcd.core.library.load_library --kwargs "{'only': ['html']}"

Each course folder holds `course.json` and one source file per language (`ar.md`, `en.md`, see core/authoring.py).
Per language it builds one space (pages in course order, a menu per chapter, a quiz per lesson that has questions,
one course with a certificate) as a space bundle and imports it with the space importer. A space that already
exists is not rebuilt: its pages get the new text instead (`update_pages`), so learners keep their progress.
Command line only."""

import html
import json
import os

import frappe

from vintraxo_tcd.core import authoring, content, transfer

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "library")
QUIZ = {"ar": "اختبار: {0}", "en": "Quiz: {0}"}


def course_dirs(root: str = ROOT, only: list | None = None) -> list[str]:
	names = sorted(d for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, "course.json")))
	return [os.path.join(root, d) for d in names if not only or d in only]


def read_course(path: str) -> dict:
	with open(os.path.join(path, "course.json"), encoding="utf-8") as f:
		meta = json.load(f)

	def resolve(value):  # "@file.sql" -> that file's text
		if isinstance(value, str) and value.startswith("@"):
			with open(os.path.join(path, value[1:]), encoding="utf-8") as f:
				return f.read().strip()
		return value

	for key, value in (meta.get("setups") or {}).items():  # one text, or {"ar": ..., "en": ...}
		meta["setups"][key] = (
			{lang: resolve(v) for lang, v in value.items()} if isinstance(value, dict) else resolve(value)
		)
	meta["lessons"] = {}
	for lang in meta["spaces"]:
		with open(os.path.join(path, f"{lang}.md"), encoding="utf-8") as f:
			meta["lessons"][lang] = {ls["slug"]: ls for ls in authoring.split_lessons(f.read())}
	listed = [s for ch in meta["chapters"] for s in ch["lessons"]]
	for lang, lessons in meta["lessons"].items():
		missing = [s for s in listed if s not in lessons]
		extra = [s for s in lessons if s not in listed]
		if missing or extra:
			raise authoring.SourceError(
				f"{path} [{lang}]: missing lessons {missing}, not in a chapter {extra}"
			)
	return meta


def build_bundle(meta: dict, lang: str) -> dict:
	"""Space bundle (transfer format) for one language."""
	space = meta["spaces"][lang]
	contents, quizzes, navigation = [], [], []
	for chapter in meta["chapters"]:
		for slug in chapter["lessons"]:
			ls = meta["lessons"][lang][slug]
			setups = {
				k: (v.get(lang) if isinstance(v, dict) else v) for k, v in (meta.get("setups") or {}).items()
			}
			blocks, questions = authoring.to_blocks(ls["body"], setups)
			contents.append(
				{
					"_id": slug,
					"title": ls["title"],
					"slug": slug,
					"content_type": ls["type"],
					"language": lang,
					"visibility": "Public",
					"status": "Published",
					"summary": ls["summary"],
					"blocks": json.dumps(blocks, ensure_ascii=False),
					"skip_review": 1,
					"translation_key": f"{meta['key']}:{slug}",  # Phase 31: same page in every language
				}
			)
			for q in (
				questions
			):  # stored as entities: Frappe's XSS filter would mangle "<title>" (see assessment._text)
				for key in ("question", "options", "explanation"):
					if q.get(key):
						q[key] = html.escape(q[key], quote=False)
			if questions:
				quizzes.append(
					{
						"_id": f"quiz-{slug}",
						"title": QUIZ[lang].format(ls["title"])[:140],
						"content": slug,
						"pass_percentage": 60,
						"max_attempts": 0,
						"required_to_complete": 1,
						"show_answers_after_submit": 1,
						"shuffle_options": 1,
						"is_active": 1,
						"questions": questions,
						"bank_items": [],
					}
				)
			navigation.append({"group_title": chapter[lang][:140], "link_type": "Page", "content": slug})
	course = meta["course"][lang]
	return {
		"format": transfer.FORMAT,
		"version": transfer.VERSION,
		"space": {
			"_id": space["name"],
			"space_name": space["name"],
			"title": space["title"],
			"description": space.get("description", ""),
			"visibility": "Public",
			"is_active": 1,
			"language": lang,
			"translation_key": meta["key"],
			"navigation": navigation,
		},
		"contents": contents,
		"quizzes": quizzes,
		"courses": [
			{
				"_id": f"course-{meta['key']}",
				"title": course["title"],
				"summary": course.get("summary", ""),
				"status": "Published",
				"language": lang,
				"visibility": "Public",
				"completion_rule": "All Items",
				"self_enrollment": 1,
				"access": "Open",
				"issue_certificate": 1 if meta.get("certificate", True) else 0,
				"certificate_validity_months": 0,
				"translation_key": meta["key"],
			}
		],
		"chapters": [
			{
				"_id": f"chapter-{n}",
				"title": ch[lang][:140],
				"course": f"course-{meta['key']}",
				"sort_order": n,
				"items": [{"content": slug, "is_optional": 0} for slug in ch["lessons"]],
			}
			for n, ch in enumerate(meta["chapters"], 1)
		],
	}


def link_translations(meta: dict, lang: str):
	"""Spaces loaded before Phase 31: give the space, its course and pages their translation keys."""
	space = meta["spaces"][lang]["name"]
	frappe.db.set_value(
		"TCD Space", space, {"language": lang, "translation_key": meta["key"]}, update_modified=False
	)
	for course in frappe.get_all("TCD Course", filters={"space": space}, pluck="name"):
		frappe.db.set_value("TCD Course", course, "translation_key", meta["key"], update_modified=False)
	for name, slug in frappe.get_all(
		"TCD Content", filters={"space": space}, fields=["name", "slug"], as_list=True
	):
		frappe.db.set_value(
			"TCD Content", name, "translation_key", f"{meta['key']}:{slug}", update_modified=False
		)


def update_pages(meta: dict, lang: str) -> int:
	"""Existing space: refresh the text of its pages (title, summary, blocks) by slug; returns pages changed."""
	bundle = build_bundle(meta, lang)
	space = bundle["space"]["space_name"]
	changed = 0
	for row in bundle["contents"]:
		name = frappe.db.get_value("TCD Content", {"space": space, "slug": row["slug"]})
		if not name:
			continue
		doc = frappe.get_doc("TCD Content", name)
		new_blocks = content.validate_blocks(content.parse_blocks(row["blocks"]))
		if (doc.title, doc.summary or "", content.parse_blocks(doc.blocks)) == (
			row["title"],
			row["summary"],
			new_blocks,
		):
			continue  # compared as saved (validated), not as raw JSON text
		doc.update({"title": row["title"], "summary": row["summary"], "blocks": row["blocks"]})
		# like an accepted suggested edit (core.change_requests.accept): the source file in git is the review,
		# the page stays published and gets a new version in its history
		doc.flags.change_request = True
		if doc.status in content.LOCKED_STATUSES:
			doc.flags.snapshot = True
		doc.save(ignore_permissions=True)
		changed += 1
	return changed


def load_library(only: list | None = None, root: str = ROOT) -> dict:
	from vintraxo_tcd.core.server_keys import cli_setup

	cli_setup()
	report = {}
	for path in course_dirs(root, only):
		meta = read_course(path)
		for lang in meta["spaces"]:
			space = meta["spaces"][lang]["name"]
			if frappe.db.exists("TCD Space", space):
				link_translations(meta, lang)
				report[space] = f"updated {update_pages(meta, lang)} pages"
			else:
				result = transfer.import_bundle(build_bundle(meta, lang))
				report[space] = ", ".join(f"{k}: {v}" for k, v in sorted(result["created"].items()))
			frappe.db.commit()
			print(f"[LIBRARY] {space}: {report[space]}", flush=True)
	return report
