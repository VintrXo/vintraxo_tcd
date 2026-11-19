"""Phase 11 security review: guest surface, stored HTML, Markdown sanitizing, code-answer trust,
cross-user data isolation."""

import json

import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import wiki
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course
from vintraxo_tcd.tests.test_ph4_assessment import question

OWN_ROWS = (
	"TCD Progress",
	"TCD Enrollment",
	"TCD Quiz Submission",
	"TCD Certificate",
	"TCD User Skill",
	"TCD Assignment Submission",
	"TCD Acknowledgment",
)


class TestPhase11Hardening(TCDTestCase):
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
		for dt in ("TCD Certificate", "TCD Question", "TCD Quiz Bank Item", *CLEAN):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		self.space = make_space("ph11-space").name
		self.l1 = lesson(self.space, "Hardening lesson")

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ API surface

	def test_guest_surface(self):
		import vintraxo_tcd.api

		ours = [f for f in frappe.guest_methods if f.__module__.startswith("vintraxo_tcd")]
		self.assertEqual([f.__name__ for f in ours], ["verify_certificate"])
		frappe.set_user("Guest")
		checked = 0
		for fn in frappe.whitelisted:
			if fn.__module__.startswith("vintraxo_tcd") and fn not in ours:
				with self.assertRaises(frappe.PermissionError, msg=fn.__name__):
					frappe.is_whitelisted(fn)
				checked += 1
		self.assertGreater(checked, 40)

	# ------------------------------------------------------------ XSS

	def test_stored_html_is_never_rendered(self):
		evil = "<script>alert(1)</script>"
		page = lesson(
			self.space,
			"Injected",
			blocks=json.dumps([{"type": "paragraph", "text": "hello", "html": evil}]),
		)
		self.assertNotIn("html", json.loads(page.blocks)[0])  # dropped on save
		self.assertNotIn(
			"html", wiki.prepare_blocks([{"type": "paragraph", "text": "x", "html": evil}], self.space)[0]
		)
		status, html, _ = render(f"/learn/{self.space}/{page.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertNotIn(evil, html)

	def test_markdown_is_sanitized(self):
		html = wiki.render_markdown(
			"[x](javascript:alert(1)) <img src=x onerror=alert(2)> <script>alert(3)</script> **ok**",
			self.space,
		)
		for bad in ("javascript:", "onerror", "<script"):
			self.assertNotIn(bad, html)
		self.assertIn("<strong>ok</strong>", html)

	# ------------------------------------------------------------ trust in code answers

	def test_instructor_reviews_code_answers(self):
		course = make_course(self.space, "Exam course", [[self.l1]], instructors=[self.vip])
		code = question("Code", code_language="python", expected_output="1", points=2)
		quiz = {
			"doctype": "TCD Quiz",
			"title": "Exam",
			"content": self.l1.name,
			"pass_percentage": 50,
			"bank_items": [{"question": code.name}],
		}
		practice = frappe.get_doc(dict(quiz)).insert()
		exam = frappe.get_doc({**quiz, "title": "Exam 2", "review_code_answers": 1}).insert()
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		forged = {code.name: {"code": "print(2)", "output": "1"}}  # output reported by the device
		self.assertTrue(api.submit_quiz(practice.name, forged)["passed"])  # practice: device result trusted
		res = api.submit_quiz(exam.name, forged)
		self.assertTrue(res["pending_review"])  # exam: an instructor confirms
		self.assertFalse(res["passed"])

	# ------------------------------------------------------------ data isolation

	def test_learners_only_see_their_own_records(self):
		course = make_course(self.space, "Shared course", [[self.l1]], issue_certificate=1)
		for user in (self.learner, self.other):
			frappe.set_user(user)
			api.enroll("Course", course.name)
			api.complete_lesson(self.l1.name)
		frappe.set_user(self.learner)
		for dt in OWN_ROWS:
			users = {r.user for r in frappe.get_list(dt, fields=["user"], limit_page_length=0)}
			self.assertTrue(users <= {self.learner}, f"{dt} leaks {users - {self.learner}}")
		cert = frappe.db.get_value("TCD Certificate", {"user": self.other})
		self.assertFalse(frappe.has_permission("TCD Certificate", "read", cert))
		for dt in ("TCD Connector", "TCD Integration Event", "TCD AI Usage Log", "TCD AI Settings"):
			self.assertFalse(frappe.has_permission(dt, "read"), dt)

	# ------------------------------------------------------------ staff without the learner role

	def test_staff_roles_can_open_portal_pages(self):
		page = lesson(self.space, "Staff page")
		for user in (self.author, self.reviewer):
			for path in ("/learn", "/learn/my", f"/learn/{self.space}", f"/learn/{self.space}/{page.slug}"):
				status, _, _ = render(path, user)
				self.assertEqual(status, 200, f"{user} {path}")
