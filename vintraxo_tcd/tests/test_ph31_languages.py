import os
import tempfile

import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import content_languages as cl
from vintraxo_tcd.core import library, portal, progress
from vintraxo_tcd.tests import test_ph30_library as ph30
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_user
from vintraxo_tcd.tests.test_ph1_courses import CLEAN

SPACES = ["lib-t-ar", "lib-t-en"]
SIMPLE = """# @lesson t-intro
title: {a}
---
{b}

# @lesson t-next
title: {c}
---
{d}
"""


class TestPhase31Languages(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))

	def setUp(self):
		frappe.set_user("Administrator")
		frappe.local.request = (
			None  # render() in another test leaves a request; the loader is command-line only
		)
		for dt in (*CLEAN, "TCD Certificate", "TCD Quiz Submission"):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Quiz", {"space": ("in", SPACES)})
		frappe.db.delete("TCD Space Nav Item", {"parent": ("in", SPACES)})
		frappe.db.delete("TCD Space", {"name": ("in", SPACES)})
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()
		with tempfile.TemporaryDirectory() as root:
			ph30.TestPhase30Library.write_course(
				self,
				root,
				ar=SIMPLE.format(a="مقدمة", b="درس أول.", c="التالي", d="درس ثانٍ."),
			)
			with open(os.path.join(root, "t", "en.md"), "w", encoding="utf-8") as f:
				f.write(SIMPLE.format(a="Intro", b="First lesson.", c="Next", d="Second lesson."))
			library.load_library(root=root)
		self.course_ar = frappe.db.get_value("TCD Course", {"space": "lib-t-ar"})
		self.course_en = frappe.db.get_value("TCD Course", {"space": "lib-t-en"})
		self.page = {
			(lang, slug): frappe.db.get_value("TCD Content", {"space": f"lib-t-{lang}", "slug": slug})
			for lang in ("ar", "en")
			for slug in ("t-intro", "t-next")
		}

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_one_card_in_the_learner_language(self):
		frappe.set_user(self.learner)
		cl.set_preferred("en")
		names = [s.name for s in portal.home_context()["spaces"]]
		self.assertIn("lib-t-en", names)
		self.assertNotIn("lib-t-ar", names)
		cl.set_preferred("ar")
		names = [s.name for s in portal.home_context()["spaces"]]
		self.assertEqual(("lib-t-ar" in names, "lib-t-en" in names), (True, False))
		both = [
			frappe._dict(name=self.page[("en", "t-intro")]),
			frappe._dict(name=self.page[("ar", "t-intro")]),
		]
		self.assertEqual([r.name for r in cl.collapse(both, "TCD Content")], [self.page[("ar", "t-intro")]])
		# a search word found only in the English page still finds it
		results = [r.name for r in portal.home_context(query="lesson")["results"] or []]
		self.assertIn(self.page[("en", "t-intro")], results)
		with self.assertRaises(frappe.ValidationError):
			cl.set_preferred("xx")

	def test_switcher_and_switching(self):
		frappe.set_user(self.learner)
		buttons = cl.switcher("TCD Content", self.page[("ar", "t-intro")], self.course_ar)
		self.assertEqual([(b["lang"], b["current"]) for b in buttons], [("ar", True), ("en", False)])
		url = cl.target_url("TCD Content", self.page[("ar", "t-intro")], "en", self.course_ar)
		self.assertEqual(url, f"/learn/lib-t-en/t-intro?course={self.course_en}")
		self.assertEqual(cl.preferred(self.learner), "en")
		self.assertEqual(cl.target_url("TCD Space", "lib-t-en", "ar"), "/learn/lib-t-ar")
		with self.assertRaises(frappe.PermissionError):
			cl.target_url("User", "Administrator", "en")
		# no other language: no buttons
		self.assertEqual(cl.switcher("TCD Space", "lib-t-ar") != [], True)
		frappe.set_user("Administrator")
		frappe.db.set_value("TCD Space", "lib-t-en", "translation_key", None)
		self.assertEqual(cl.switcher("TCD Space", "lib-t-ar"), [])

	def test_progress_enrollment_and_one_certificate(self):
		frappe.set_user(self.learner)
		api.enroll("Course", self.course_ar)
		progress.complete(self.learner, self.page[("ar", "t-intro")])
		# the English page counts as done too
		self.assertEqual(
			frappe.db.get_value(
				"TCD Progress", {"user": self.learner, "content": self.page[("en", "t-intro")]}, "status"
			),
			"Completed",
		)
		# switching mid-course: enrolled in the English course with the progress copied
		cl.target_url("TCD Course", self.course_ar, "en")
		en = frappe.get_doc("TCD Enrollment", {"user": self.learner, "course": self.course_en})
		self.assertEqual(en.percent, 50)
		self.assertEqual(len(portal.my_enrollments(self.learner)), 1)  # one row per course
		# finish in English: one certificate, not two
		progress.complete(self.learner, self.page[("en", "t-next")])
		self.assertEqual(
			frappe.db.get_value("TCD Enrollment", {"user": self.learner, "course": self.course_ar}, "status"),
			"Completed",
		)
		self.assertEqual(frappe.db.count("TCD Certificate", {"user": self.learner}), 1)

	def test_recommendations_one_per_course(self):
		from vintraxo_tcd.core import connect

		frappe.set_user(self.learner)
		cl.set_preferred("en")
		names = [r["name"] for r in connect.recommendations(self.learner, limit=50)]
		self.assertNotIn(self.course_ar, names)
		self.assertIn(self.course_en, names)
		api.enroll("Course", self.course_ar)  # enrolled in Arabic: the English one is not "popular" for them
		names = [
			r["name"] for r in connect.recommendations(self.learner, limit=50) if r["reason"] == "popular"
		]
		self.assertNotIn(self.course_en, names)

	def test_continue_learning_in_the_learner_language(self):
		from vintraxo_tcd.core.progress import _upsert

		frappe.set_user("Administrator")
		_upsert(self.learner, self.page[("en", "t-intro")], status="In Progress", percent=10)
		_upsert(self.learner, self.page[("ar", "t-intro")], status="In Progress", percent=10)
		_upsert(self.learner, self.page[("en", "t-next")], status="In Progress", percent=10)
		frappe.set_user(self.learner)
		cl.set_preferred("ar")
		shown = [r.content for r in portal.home_context()["continue_learning"]]
		# the same lesson read in both languages is one item, and English pages appear in Arabic
		self.assertEqual(sorted(shown), sorted([self.page[("ar", "t-intro")], self.page[("ar", "t-next")]]))

	def test_home_catalog_groups_by_category(self):
		frappe.set_user("Administrator")
		frappe.db.set_value("TCD Space", "lib-t-en", "category", "Programming")
		frappe.db.set_value("TCD Space", "lib-t-ar", "category", "Programming")
		frappe.set_user(self.learner)
		cl.set_preferred("en")
		groups = {g["key"]: g for g in portal.home_context()["catalog"]}
		mine = [s for s in groups["Programming"]["spaces"] if s.name in SPACES]
		self.assertEqual([s.name for s in mine], ["lib-t-en"])  # one card, in the learner's language
		self.assertEqual(mine[0].lessons, 2)
		self.assertEqual(mine[0].progress, 0)
		api.enroll("Course", self.course_ar)
		progress.complete(self.learner, self.page[("ar", "t-intro")])
		groups = {g["key"]: g for g in portal.home_context()["catalog"]}
		mine = [s for s in groups["Programming"]["spaces"] if s.name in SPACES]
		self.assertEqual(mine[0].progress, 50)  # progress made in Arabic shows on the English card

	def test_course_page_renders_buttons(self):
		from vintraxo_tcd.tests.test_p3 import render

		status, html, _ = render(
			"/learn/lib-t-ar/course/" + frappe.db.get_value("TCD Course", self.course_ar, "slug"),
			self.learner,
		)
		self.assertEqual(status, 200)
		self.assertIn("tcd-lang-switch", html)
		self.assertIn('data-lang="en"', html)
