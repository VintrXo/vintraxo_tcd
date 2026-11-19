import json

import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import change_requests, notes, progress
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course

BLOCKS = [
	{"type": "heading", "text": "Intro", "level": 2},
	{"type": "paragraph", "text": "Python is a language."},
	{"type": "video", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "title": "Clip"},
	{"type": "heading", "text": "Variables", "level": 2},
	{"type": "markdown", "text": "## Types & values\n\nint, str"},
	{"type": "list", "items": ["one", "two"]},
]


class TestPhase14(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		cls.other = make_user("tcd-other@test.local", ["TCD Learner"])
		frappe.get_single("TCD Settings").update(
			{"enable_portal": 1, "enable_change_requests": 1, "require_approval_before_publish": 1}
		).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Change Request", "TCD Lesson Note", *CLEAN):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		self.space = make_space("ph14-space").name
		self.page = lesson(self.space, "Rich page", blocks=json.dumps(BLOCKS))

	def tearDown(self):
		frappe.set_user("Administrator")

	def url(self):
		return f"/learn/{self.space}/{self.page.slug}"

	# ------------------------------------------------------------ table of contents

	def test_table_of_contents(self):
		status, html, _ = render(self.url(), self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-toc", html)
		self.assertIn('id="sec-1"', html)  # heading block anchor
		self.assertIn('<h2 id="sec-3">Types &amp; values</h2>', html)  # markdown heading anchor
		self.assertIn('href="#sec-3"', html)
		self.assertNotIn("&amp;amp;", html)

	# ------------------------------------------------------------ cover and intro video

	def test_cover_and_intro(self):
		course = make_course(self.space, "Covered", [[self.page]], intro_video="https://youtu.be/dQw4w9WgXcQ")
		with self.assertRaises(frappe.ValidationError):
			course.intro_video = "https://evil.example.com/v.mp4"
			course.save()
		course.reload()
		frappe.set_user(self.learner)
		data = api.get_course(course.name)
		self.assertEqual(data["intro"]["embed_url"], "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ")
		_, html, _ = render(f"/learn/{self.space}/course/{course.slug}", self.learner)
		self.assertIn("tcd-intro", html)

	# ------------------------------------------------------------ video watching

	def test_video_watch_rule(self):
		frappe.db.set_value("TCD Content", self.page.name, "min_video_percent", 80)
		frappe.set_user(self.learner)
		_, html, _ = render(self.url(), self.learner)
		self.assertIn('data-video-index="0"', html)
		self.assertIn("enablejsapi=1", html)
		with self.assertRaises(frappe.ValidationError):
			api.complete_lesson(self.page.name)
		self.assertEqual(api.video_progress(self.page.name, 0, 50, 100)["video_percent"], 50)
		self.assertEqual(api.video_progress(self.page.name, 0, 30, 100)["video_percent"], 50)  # keeps the max
		self.assertEqual(api.video_progress(self.page.name, 0, 500, 100)["video_percent"], 100)  # capped
		with self.assertRaises(frappe.ValidationError):
			api.video_progress(self.page.name, 5, 10, 100)
		api.complete_lesson(self.page.name)
		self.assertEqual(progress.get_progress(self.learner, self.page.name).status, "Completed")

	# ------------------------------------------------------------ notes

	def test_notes_are_private(self):
		frappe.set_user(self.learner)
		api.save_note(self.page.name, "remember: <b>slices</b>")
		self.assertEqual(notes.get(self.page.name, self.learner), "remember: <b>slices</b>")
		_, html, _ = render(self.url(), self.learner)
		self.assertIn("remember: &lt;b&gt;slices&lt;/b&gt;", html)  # escaped
		_, html, _ = render("/learn/my", self.learner)
		self.assertIn("Rich page", html)
		frappe.set_user(self.other)
		self.assertEqual(notes.get(self.page.name, self.other), "")
		_, html, _ = render(self.url(), self.other)
		self.assertNotIn("slices", html)
		for user in (self.other, self.reviewer, self.author):
			frappe.set_user(user)
			self.assertFalse(frappe.has_permission("TCD Lesson Note", "read"))
		frappe.set_user(self.learner)
		api.save_note(self.page.name, "")
		self.assertFalse(frappe.db.exists("TCD Lesson Note", {"user": self.learner}))

	# ------------------------------------------------------------ suggested edits

	def edit(self, index, field, value):
		return [{"index": index, "field": field, "value": value}]

	def test_suggest_accept_creates_version(self):
		versions = frappe.db.count("TCD Content Version", {"content": self.page.name})
		frappe.set_user(self.learner)
		_, html, _ = render(self.url(), self.learner)
		self.assertIn("tcd-suggest-form", html)
		name = api.propose_change(
			self.page.name,
			json.dumps(self.edit(1, "text", "Python is a <script>x</script> language.")),
			summary="typo",
		)
		self.assertIn(
			"Python is a language.", frappe.db.get_value("TCD Content", self.page.name, "blocks")
		)  # unchanged
		with self.assertRaises(frappe.PermissionError):
			api.accept_change_request(name)
		frappe.set_user(self.reviewer)
		self.assertTrue(api.change_request_diff(name)["diff"])
		api.accept_change_request(name, "thanks")
		page = frappe.get_doc("TCD Content", self.page.name)
		self.assertEqual(page.status, "Published")
		self.assertIn("<script>x</script>", json.loads(page.blocks)[1]["text"])  # stored as text...
		_, html, _ = render(self.url(), self.other)
		self.assertNotIn("<script>x</script>", html)  # ...and escaped on render
		frappe.set_user(self.reviewer)
		self.assertEqual(frappe.db.count("TCD Content Version", {"content": self.page.name}), versions + 1)
		self.assertEqual(frappe.db.get_value("TCD Change Request", name, "status"), "Accepted")
		with self.assertRaises(frappe.ValidationError):
			api.reject_change_request(name)  # already closed

	def test_conflict_reject_and_limits(self):
		frappe.set_user(self.learner)
		first = api.propose_change(self.page.name, json.dumps(self.edit(5, "items", "uno\ndos")), summary="a")
		second = api.propose_change(
			self.page.name, json.dumps(self.edit(0, "text", "Introduction")), summary="b"
		)
		frappe.set_user(self.reviewer)
		api.accept_change_request(second)
		with self.assertRaises(frappe.ValidationError):
			api.accept_change_request(first)  # page changed since: conflict, nothing overwritten
		self.assertEqual(frappe.db.get_value("TCD Change Request", first, "status"), "Conflict")
		self.assertEqual(
			json.loads(frappe.db.get_value("TCD Content", self.page.name, "blocks"))[5]["items"],
			["one", "two"],
		)

		frappe.set_user(self.learner)
		third = api.propose_change(self.page.name, json.dumps(self.edit(3, "text", "Vars")), summary="c")
		frappe.set_user(self.reviewer)
		api.reject_change_request(third, "keep it")
		self.assertEqual(frappe.db.get_value("TCD Change Request", third, "status"), "Rejected")

		frappe.set_user(self.learner)
		with self.assertRaises(frappe.ValidationError):
			api.propose_change(
				self.page.name, json.dumps(self.edit(2, "url", "https://evil")), summary="x"
			)  # video url
		with self.assertRaises(frappe.ValidationError):
			api.propose_change(self.page.name, json.dumps([]), summary="nothing")
		for i in range(change_requests.PER_HOUR - 3):
			api.propose_change(self.page.name, json.dumps(self.edit(3, "text", f"v{i}")), summary="s")
		with self.assertRaises(frappe.ValidationError):
			api.propose_change(self.page.name, json.dumps(self.edit(3, "text", "again")), summary="s")
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{"doctype": "TCD Change Request", "content": self.page.name, "user": self.learner}
			).insert()
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Change Request", "read"))
