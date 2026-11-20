import json

import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import community, credentials
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course


class TestPhase25Community(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		cls.other = make_user("tcd-other@test.local", ["TCD Learner"])
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (*CLEAN, "TCD Certificate", "TCD Learner Profile"):
			frappe.db.delete(dt)
		self.space = make_space("ph25-space").name
		self.course = make_course(
			self.space, "Cert course", [[lesson(self.space, "Cert lesson")]], issue_certificate=1
		)

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_only_opted_in_learners_are_listed(self):
		credentials.issue_certificate(self.learner, "Course", self.course.name)
		credentials.issue_certificate(self.other, "Course", self.course.name)
		frappe.set_user(self.learner)
		api.save_profile(json.dumps({"headline": "x", "public_profile": 1}))
		frappe.set_user("Administrator")
		rows = community.certified()
		self.assertEqual([r.user for r in rows], [self.learner])  # the other learner did not opt in
		self.assertEqual(community.certified(self.course.name)[0].title, "Cert course")
		s = community.stats()
		self.assertEqual(s["certificates"], 2)
		self.assertGreaterEqual(s["courses"], 1)

		status, html, _ = render("/learn/certified", self.vip)
		self.assertEqual(status, 200)
		self.assertIn(f"/learn/profile?user={self.learner}", html.replace("%40", "@"))
		self.assertNotIn(self.other, html.replace("%40", "@"))
		self.assertEqual(render("/learn/certified", "Guest")[0], 302)  # login needed

	def test_markdown_preview_is_sanitized(self):
		frappe.set_user(self.learner)
		html = api.preview_markdown("**bold** <script>alert(1)</script> [x](javascript:alert(1))")
		self.assertIn("<strong>bold</strong>", html)
		self.assertNotIn("<script", html)
		self.assertNotIn("javascript:", html)
		frappe.set_user("Guest")
		with self.assertRaises(frappe.PermissionError):
			api.preview_markdown("x")
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.ValidationError):
			api.preview_markdown("x" * 20001)
