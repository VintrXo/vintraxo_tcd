import json
import re

import frappe

from vintraxo_tcd.core import content as svc
from vintraxo_tcd.core import github_sync, portal
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user, publish
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course

EXERCISE = {
	"type": "exercise",
	"prompt": "Print <b>x</b>",
	"language": "python",
	"code": "x = ___\n___(x)",
	"answers": [" 5 ", "print"],
	"hint": "Use the built-in function",
}


class TestPhase17Learning(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update({"enable_portal": 1, "enable_playgrounds": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in CLEAN:
			frappe.db.delete(dt)
		self.space = make_space("ph17-space").name

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_exercise_block_validation(self):
		cleaned = svc.validate_blocks([EXERCISE])[0]
		self.assertEqual(cleaned["answers"], ["5", "print"])  # trimmed
		for bad in (
			{**EXERCISE, "answers": ["5"]},  # 2 blanks, 1 answer
			{**EXERCISE, "answers": ["5", " "]},  # empty answer
			{**EXERCISE, "code": "no blanks", "answers": []},
		):
			with self.assertRaises(frappe.ValidationError):
				svc.validate_blocks([bad])
		self.assertIn("print", svc.build_search_text("t", "", [cleaned]))

	def test_exercise_renders_escaped_with_blanks(self):
		page = lesson(self.space, "Exercise page", blocks=json.dumps([EXERCISE]))
		status, html, _ = render(f"/learn/{self.space}/{page.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertEqual(html.count('class="tcd-blank-input"'), 2)
		self.assertIn("Print &lt;b&gt;x&lt;/b&gt;", html)
		self.assertNotIn("<b>x</b>", html)
		answers = re.search(r'<template class="tcd-exercise-answers">(.*?)</template>', html).group(1)
		self.assertEqual(json.loads(answers), ["5", "print"])
		self.assertIn("tcd_highlight.js", html)
		md = github_sync.to_markdown(frappe.get_doc("TCD Content", page.name))
		self.assertIn("x = ___", md)

	def test_course_outline_and_top_navigation(self):
		a = lesson(self.space, "First lesson")
		b = lesson(self.space, "Second lesson")
		hidden = publish(
			make_content(self.space, "Staff only", content_type="Lesson", visibility="Restricted")
		)
		course = make_course(self.space, "Outline course", [[a, b], [hidden]], rule="Required Sequence")
		status, html, _ = render(f"/learn/{self.space}/{a.slug}?course={course.name}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-with-outline", html)
		self.assertIn('class="tcd-outline-item is-open is-current"', html)
		self.assertIn("is-locked", html)  # second lesson waits for the first
		self.assertNotIn("Staff only", html)  # unreadable items are not listed
		self.assertIn('class="tcd-nav-top"', html)
		self.assertIn("tcd-next", html)

		doc = frappe.get_doc("TCD Content", a.name)
		self.assertIsNone(portal.lesson_outline(self.learner, doc, self.space, None, None))
		status, html, _ = render(f"/learn/{self.space}/{a.slug}", self.learner)
		self.assertNotIn("tcd-with-outline", html)  # no course or tutorial: no side menu

	def test_tutorial_outline(self):
		l1 = lesson(self.space, "Tut lesson one")
		l2 = lesson(self.space, "Tut lesson two")
		tut = publish(
			make_content(
				self.space,
				"Tutorial X",
				content_type="Tutorial",
				visibility="Public",
				lessons=[{"lesson": l1.name}, {"lesson": l2.name}],
			)
		)
		doc = frappe.get_doc("TCD Content", l2.name)
		frappe.set_user(self.learner)
		out = portal.lesson_outline(self.learner, doc, self.space, tut.name, None)
		self.assertEqual(out["title"], "Tutorial X")
		items = out["groups"][0]["items"]
		self.assertEqual([i["title"] for i in items], ["Tut lesson one", "Tut lesson two"])
		self.assertEqual([i["current"] for i in items], [False, True])
		self.assertIn(f"tutorial={tut.name}", items[0]["url"])

	def test_new_labels_present(self):
		labels = portal.js_labels()
		for key in ("copy", "copied", "full_screen", "exit_full_screen", "exercise_correct", "theme_dark"):
			self.assertTrue(labels.get(key))

	def test_reference_block(self):
		entries = [f"FN{i} | Does thing {i} | SELECT FN{i}(x) FROM t" for i in range(10)] + ["<b>bad</b> | x"]
		block = {
			"type": "reference",
			"title": "SQL functions",
			"language": "sql",
			"entries": [*entries, "  "],
		}
		cleaned = svc.validate_blocks([block])[0]
		self.assertEqual(len(cleaned["entries"]), 11)  # blank line dropped
		for bad in (
			{**block, "entries": []},
			{**block, "entries": [" | no name"]},
			{**block, "entries": [1]},
		):
			with self.assertRaises(frappe.ValidationError):
				svc.validate_blocks([bad])
		page = publish(
			make_content(
				self.space,
				"Reference page",
				content_type="Reference",
				visibility="Public",
				blocks=json.dumps([block]),
			)
		)
		status, html, _ = render(f"/learn/{self.space}/{page.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertEqual(html.count('<tr id="ref-'), 11)
		self.assertIn("tcd-reference-filter", html)  # more than 8 rows: filter box
		self.assertIn("&lt;b&gt;bad&lt;/b&gt;", html)
		self.assertNotIn("<b>bad</b>", html)
		self.assertIn("SELECT FN3(x) FROM t", html)
		md = github_sync.to_markdown(frappe.get_doc("TCD Content", page.name))
		self.assertIn("| FN0 | Does thing 0 | SELECT FN0(x) FROM t |", md)
