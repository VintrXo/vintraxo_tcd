import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import discussions
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course


class TestPhase12Discussions(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		cls.other = make_user("tcd-other@test.local", ["TCD Learner"])
		frappe.get_single("TCD Settings").update({"enable_portal": 1, "enable_discussions": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Discussion Post", *CLEAN):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		frappe.db.delete("TCD Course Instructor")
		frappe.db.delete("Notification Log", {"document_type": "TCD Discussion Post"})
		self.space = make_space("ph12d-space").name
		self.page = lesson(self.space, "Discussed lesson")
		frappe.db.set_value("TCD Content", self.page.name, "content_owner", self.author)
		make_course(self.space, "Discussed course", [[self.page]], instructors=[self.vip])

	def tearDown(self):
		frappe.set_user("Administrator")

	def notes(self, user):
		return frappe.get_all(
			"Notification Log",
			filters={"document_type": "TCD Discussion Post", "for_user": user},
			pluck="subject",
			ignore_permissions=True,
		)

	def test_ask_answer_accept(self):
		frappe.set_user(self.learner)
		q = api.discussion_post(self.page.name, "  <b>How</b> do I read a file?  ")
		self.assertEqual(
			q["body"], "<b>How</b> do I read a file?"
		)  # stored as plain text, shown with textContent
		self.assertTrue(self.notes(self.author))  # page owner
		self.assertTrue(self.notes(self.vip))  # instructor of a course using the page
		self.assertFalse(self.notes(self.learner))

		frappe.set_user(self.other)
		peer = api.discussion_post(self.page.name, "Use open()", thread=q["name"])
		self.assertFalse(peer["staff"])
		frappe.set_user(self.vip)
		answer = api.discussion_post(self.page.name, "open(path).read()", thread=q["name"])
		self.assertTrue(answer["staff"])
		self.assertEqual(len(self.notes(self.learner)), 2)
		self.assertEqual(frappe.db.get_value("TCD Discussion Post", q["name"], "status"), "Answered")

		frappe.set_user(self.other)  # not the asker, not a moderator
		with self.assertRaises(frappe.PermissionError):
			api.discussion_accept(answer["name"])
		frappe.set_user(self.learner)
		api.discussion_accept(peer["name"])
		api.discussion_accept(answer["name"])  # only one best answer
		data = api.discussion_list(self.page.name)
		self.assertFalse(data["can_moderate"])
		replies = data["threads"][0]["replies"]
		self.assertEqual([r["accepted"] for r in replies], [False, True])
		with self.assertRaises(frappe.ValidationError):
			api.discussion_post(self.page.name, "nested", thread=answer["name"])  # no reply to a reply

	def test_moderation_and_visibility(self):
		frappe.set_user(self.learner)
		q = api.discussion_post(self.page.name, "Off-topic advert")
		with self.assertRaises(frappe.PermissionError):
			api.discussion_hide(q["name"])
		frappe.set_user(self.author)  # page owner moderates
		self.assertTrue(api.discussion_list(self.page.name)["can_moderate"])
		api.discussion_hide(q["name"])
		frappe.set_user(self.other)
		self.assertEqual(api.discussion_list(self.page.name)["threads"], [])
		with self.assertRaises(frappe.ValidationError):
			api.discussion_post(self.page.name, "reply", thread=q["name"])
		frappe.set_user(self.reviewer)
		self.assertTrue(api.discussion_list(self.page.name)["threads"][0]["hidden"])

	def test_access_limits_and_desk(self):
		draft = make_content(self.space, "Draft page")
		restricted = lesson(
			make_space("ph12d-secret", visibility="Restricted", roles=("TCD Instructor",)).name, "Secret"
		)
		frappe.set_user(self.learner)
		for name in (draft.name, restricted.name):
			with self.assertRaises(frappe.DoesNotExistError):
				api.discussion_post(name, "Can I see this?")
		with self.assertRaises(frappe.ValidationError):
			api.discussion_post(self.page.name, "x")  # too short
		with self.assertRaises(frappe.ValidationError):
			api.discussion_post(self.page.name, "x" * 2001)
		for i in range(discussions.POSTS_PER_HOUR):
			api.discussion_post(self.page.name, f"question {i}")
		with self.assertRaises(frappe.ValidationError):
			api.discussion_post(self.page.name, "one more")
		frappe.set_user("Guest")
		with self.assertRaises(frappe.PermissionError):
			api.discussion_post(self.page.name, "guest post")

		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):  # Desk cannot create or rewrite posts
			frappe.get_doc(
				{
					"doctype": "TCD Discussion Post",
					"content": self.page.name,
					"user": self.learner,
					"body": "forged",
				}
			).insert()
		post = frappe.get_doc("TCD Discussion Post", {"body": "question 0"})
		post.body = "rewritten"
		with self.assertRaises(frappe.ValidationError):
			post.save()
		post.reload()
		post.hidden = 1
		post.save()  # moderation is allowed

		frappe.get_single("TCD Settings").update({"enable_discussions": 0}).save()
		frappe.set_user(self.other)
		with self.assertRaises(frappe.ValidationError):
			api.discussion_post(self.page.name, "while off")
		_, html, _ = render(f"/learn/{self.space}/{self.page.slug}", self.other)
		self.assertNotIn("tcd-discussion-form", html)
		frappe.set_user("Administrator")
		frappe.get_single("TCD Settings").update({"enable_discussions": 1}).save()
		_, html, _ = render(f"/learn/{self.space}/{self.page.slug}", self.other)
		self.assertIn("tcd-discussion-form", html)
