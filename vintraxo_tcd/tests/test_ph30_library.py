import json
import os
import tempfile

import frappe

from vintraxo_tcd.core import authoring, library
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_ph1_courses import CLEAN

AR = """# @lesson t-intro
title: مقدمة
summary: أول درس
---
فقرة **مهمة**.

## عنوان فرعي

```html
<p>كود</p>
```

```try html
<h1>جرّب</h1>
```

:::tip ملاحظة
نص الملاحظة
:::

- أول
- ثاني

```exercise html
? أكمل الوسم
<___>عنوان</h1>
= h1
! الوسم الأكبر
```

```reference html
<p> | فقرة | <p>نص</p>
```

```quiz
? ما معنى HTML؟
- لغة برمجة
* لغة ترميز
> HTML لغة ترميز.

? الوسوم تُكتب بين < و >
= true

? اختر الوسوم الصحيحة
* p
* h1
- x

? أي وسم لعنوان التبويب؟
- <body>
* <title>
> <title> داخل <head>.
```

# @lesson t-next
title: التالي
---
درس ثانٍ.
"""

EN = AR.replace("title: مقدمة", "title: Intro").replace("title: التالي", "title: Next")

COURSE = {
	"key": "t",
	"spaces": {
		"ar": {"name": "lib-t-ar", "title": "تجربة"},
		"en": {"name": "lib-t-en", "title": "Trial"},
	},
	"course": {"ar": {"title": "دورة تجربة"}, "en": {"title": "Trial course"}},
	"chapters": [{"ar": "البداية", "en": "Start", "lessons": ["t-intro", "t-next"]}],
}


class TestPhase30Library(TCDTestCase):
	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (*CLEAN, "TCD Quiz Submission"):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Quiz", {"space": ("in", ["lib-t-ar", "lib-t-en"])})
		frappe.db.delete("TCD Space Nav Item", {"parent": ("in", ["lib-t-ar", "lib-t-en"])})
		frappe.db.delete("TCD Space", {"name": ("in", ["lib-t-ar", "lib-t-en"])})

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_parser(self):
		lessons = authoring.split_lessons(AR)
		self.assertEqual([ls["slug"] for ls in lessons], ["t-intro", "t-next"])
		blocks, questions = authoring.to_blocks(lessons[0]["body"])
		types = [b["type"] for b in blocks]
		self.assertEqual(
			types,
			["paragraph", "heading", "code", "playground", "callout", "markdown", "exercise", "reference"],
		)
		self.assertEqual(blocks[3], {"type": "playground", "language": "html", "code": "<h1>جرّب</h1>"})
		self.assertEqual(blocks[4]["title"], "ملاحظة")
		self.assertEqual(blocks[6]["answers"], ["h1"])
		self.assertEqual(blocks[6]["hint"], "الوسم الأكبر")
		self.assertEqual(
			[(q["question_type"], q.get("correct_answers")) for q in questions],
			[("Single Choice", "2"), ("True False", "1"), ("Multiple Choice", "1,2"), ("Single Choice", "2")],
		)
		from vintraxo_tcd.core import content

		content.validate_blocks(blocks)  # every block passes the page validation

	def test_try_block_with_setup(self):
		body = "```try sql shop\nSELECT * FROM t;\n```"
		blocks, _ = authoring.to_blocks(body, {"shop": "CREATE TABLE t (a);"})
		self.assertEqual(
			blocks[0],
			{
				"type": "playground",
				"language": "sql",
				"code": "SELECT * FROM t;",
				"setup": "CREATE TABLE t (a);",
			},
		)
		from vintraxo_tcd.core import content, wiki

		content.validate_blocks(blocks)
		with self.assertRaises(authoring.SourceError):
			authoring.to_blocks(body, {})
		html = frappe.render_template(
			"{% from 'templates/includes/tcd_blocks.html' import render_blocks %}{{ render_blocks(blocks, pg) }}",
			{"blocks": wiki.prepare_blocks(blocks, ""), "pg": {"enabled": 1}},
		)
		self.assertIn('<template class="tcd-setup">CREATE TABLE t (a);</template>', html)

	def test_setup_files_stay_inside_the_library(self):
		with tempfile.TemporaryDirectory() as outer:
			root = os.path.join(outer, "library")
			os.makedirs(root)
			with open(os.path.join(outer, "secret.txt"), "w") as f:
				f.write("password")
			self.write_course(root)
			os.makedirs(os.path.join(root, "other"))
			with open(os.path.join(root, "other", "shared.html"), "w") as f:
				f.write("<p>shared</p>")
			course_json = os.path.join(root, "t", "course.json")
			meta = dict(COURSE, setups={"s": "@../other/shared.html"})
			with open(course_json, "w", encoding="utf-8") as f:
				json.dump(meta, f)
			# a sibling course folder is fine
			self.assertEqual(library.read_course(os.path.join(root, "t"))["setups"]["s"], "<p>shared</p>")
			meta["setups"] = {"s": "@../../secret.txt"}
			with open(course_json, "w", encoding="utf-8") as f:
				json.dump(meta, f)
			with self.assertRaises(frappe.ValidationError):
				library.read_course(os.path.join(root, "t"))

	def test_reference_with_pipes(self):
		from vintraxo_tcd.core import content, wiki

		blocks = content.validate_blocks(
			[{"type": "reference", "entries": ["|| | or | a || b", "x|plain|old style"]}]
		)
		self.assertEqual(content.reference_parts("|| | or | a || b"), ["||", "or", "a || b"])
		with self.assertRaises(frappe.ValidationError):
			content.validate_blocks([{"type": "reference", "entries": ["| no name"]}])
		html = frappe.render_template(
			"{% from 'templates/includes/tcd_blocks.html' import render_blocks %}{{ render_blocks(blocks, pg) }}",
			{"blocks": wiki.prepare_blocks(blocks, ""), "pg": {"enabled": 1}},
		)
		self.assertIn('<code class="nohighlight">||</code>', html)
		self.assertIn("a || b</code>", html)
		self.assertIn('<code class="nohighlight">x</code>', html)
		self.assertIn("<td>plain</td>", html)

	def test_source_errors(self):
		with self.assertRaises(authoring.SourceError):
			authoring.split_lessons("# @lesson x\ntitle: X\nno separator")
		with self.assertRaises(authoring.SourceError):
			authoring.to_blocks("```html\nnot closed")
		with self.assertRaises(authoring.SourceError):
			authoring.parse_quiz(["? no answer marked", "- a", "- b"])

	def write_course(self, root, ar=AR):
		folder = os.path.join(root, "t")
		os.makedirs(folder)
		for name, text in (
			("ar.md", ar),
			("en.md", EN),
			("course.json", json.dumps(COURSE, ensure_ascii=False)),
		):
			with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
				f.write(text)

	def test_load_and_update(self):
		with tempfile.TemporaryDirectory() as root:
			self.write_course(root)
			report = library.load_library(root=root)
			self.assertIn("TCD Course: 1", report["lib-t-ar"])
			course = frappe.get_doc("TCD Course", {"space": "lib-t-ar"})
			self.assertEqual(
				(course.status, course.issue_certificate, course.self_enrollment), ("Published", 1, 1)
			)
			intro = frappe.get_doc("TCD Content", {"space": "lib-t-ar", "slug": "t-intro"})
			self.assertEqual(intro.translation_key, "t:t-intro")  # Phase 31: linked to the English lesson
			self.assertEqual(
				frappe.db.get_value("TCD Space", "lib-t-en", ["language", "translation_key"]), ("en", "t")
			)
			quiz = frappe.get_doc("TCD Quiz", {"content": intro.name})
			self.assertEqual((len(quiz.questions), quiz.required_to_complete), (4, 1))
			# text that looks like HTML survives Frappe's XSS filter and reaches the learner as plain text
			from vintraxo_tcd.core import assessment

			row = quiz.questions[3]
			self.assertNotIn("<title>", row.options)  # stored as entities
			item = assessment.item_from_inline(row)
			self.assertEqual(assessment.options_of(item), ["<body>", "<title>"])
			self.assertEqual(item["explanation"], "<title> داخل <head>.")
			from vintraxo_tcd.core import wiki

			self.assertEqual(wiki.backlinks(intro.name), [])
			space = frappe.get_doc("TCD Space", "lib-t-ar")
			self.assertEqual([r.group_title for r in space.navigation], ["البداية", "البداية"])

			# second run: same pages, new text; nothing is recreated
		with tempfile.TemporaryDirectory() as root:
			self.write_course(root, ar=AR.replace("درس ثانٍ.", "درس ثانٍ معدّل."))
			report = library.load_library(root=root)
			self.assertEqual(report["lib-t-ar"], "updated 1 pages")
			self.assertEqual(report["lib-t-en"], "updated 0 pages")
			self.assertEqual(frappe.db.count("TCD Course", {"space": "lib-t-ar"}), 1)

	def test_mismatched_lessons_are_refused(self):
		with tempfile.TemporaryDirectory() as root:
			self.write_course(root, ar=AR.split("# @lesson t-next")[0])
			with self.assertRaises(authoring.SourceError):
				library.read_course(os.path.join(root, "t"))
