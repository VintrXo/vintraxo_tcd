import json
import re

import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import studio
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson


class TestPhase18Studio(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update(
			{"enable_portal": 1, "require_approval_before_publish": 1}
		).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in CLEAN:
			frappe.db.delete(dt)
		self.space = make_space("ph18-space").name

	def tearDown(self):
		frappe.set_user("Administrator")

	def page(self, **kw):
		data = {
			"space": self.space,
			"title": "Studio <b>page</b>",
			"content_type": "Lesson",
			"blocks": [{"type": "paragraph", "text": "Hello"}],
			**kw,
		}
		return api.studio_save_page(json.dumps(data))

	def test_access(self):
		self.assertEqual(render("/learn/studio", self.learner)[0], 404)
		self.assertEqual(render("/learn/studio/page", self.learner)[0], 404)
		status, html, _ = render("/learn/studio", self.author)
		self.assertEqual(status, 200)
		self.assertIn("/learn/studio/page", html)
		status, html, _ = render("/learn", self.author)
		self.assertIn('href="/learn/studio"', html)  # tile for authors
		status, html, _ = render("/learn", self.learner)
		self.assertNotIn('href="/learn/studio"', html)
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			self.page()

	def test_page_lifecycle_through_review(self):
		frappe.set_user(self.author)
		r = self.page()
		doc = frappe.get_doc("TCD Content", r["name"])
		self.assertEqual((doc.status, doc.owner), ("Draft", self.author))
		with self.assertRaises(frappe.ValidationError):  # block schema still applies
			self.page(name=r["name"], blocks=[{"type": "heading"}])
		self.page(name=r["name"], title="Renamed", blocks=[{"type": "heading", "text": "H", "level": 2}])
		self.assertEqual(frappe.db.get_value("TCD Content", r["name"], "title"), "Renamed")

		status, html, _ = render(f"/learn/studio/page?name={r['name']}", self.author)
		self.assertEqual(status, 200)
		self.assertIn('id="tcd-studio-spec"', html)
		self.assertIn('data-status="In Review"', html)
		api.set_content_status(r["name"], "In Review")
		with self.assertRaises(frappe.PermissionError):  # an author cannot approve
			api.set_content_status(r["name"], "Approved")

		frappe.set_user(self.reviewer)
		api.set_content_status(r["name"], "Approved")
		api.set_content_status(r["name"], "Published")
		frappe.set_user(self.author)
		with self.assertRaises(frappe.ValidationError):  # published pages are locked
			self.page(name=r["name"], title="Changed after publish")
		status, html, _ = render(f"/learn/studio/page?name={r['name']}", self.author)
		self.assertIn('data-locked="1"', html)

	def test_title_escaped_and_space_required(self):
		frappe.set_user(self.author)
		r = self.page()
		status, html, _ = render(f"/learn/studio/page?name={r['name']}", self.author)
		self.assertEqual(status, 200)
		body = re.sub(r"<title>.*?</title>", "", html, flags=re.S)  # <title> is plain text for browsers
		self.assertIn("Studio &lt;b&gt;page&lt;/b&gt;", body)
		self.assertNotIn("Studio <b>page</b>", body)
		with self.assertRaises(frappe.ValidationError):
			self.page(space="")

	def test_course_builder(self):
		a = lesson(self.space, "Lesson A")
		b = lesson(self.space, "Lesson B")
		frappe.set_user(self.author)
		r = api.studio_save_course(json.dumps({"space": self.space, "title": "Built in studio"}))
		course = r["name"]
		api.studio_save_course(
			json.dumps(
				{
					"name": course,
					"title": "Built in studio",
					"chapters": [
						{
							"title": "Start",
							"items": [{"content": a.name}, {"content": b.name, "is_optional": 1}],
						},
						{"title": "More", "items": []},
					],
				}
			)
		)
		data = studio.course_data(course)
		self.assertEqual([c["title"] for c in data["chapters"]], ["Start", "More"])
		self.assertEqual([i["content"] for i in data["chapters"][0]["items"]], [a.name, b.name])
		self.assertEqual(data["chapters"][0]["items"][1]["is_optional"], 1)

		# reorder, rename and drop a chapter
		first = data["chapters"][0]
		api.studio_save_course(
			json.dumps(
				{
					"name": course,
					"chapters": [{"name": first["name"], "title": "Renamed", "items": [{"content": b.name}]}],
				}
			)
		)
		data = studio.course_data(course)
		self.assertEqual([c["title"] for c in data["chapters"]], ["Renamed"])
		self.assertEqual(data["chapters"][0]["name"], first["name"])  # same chapter kept
		self.assertEqual(frappe.db.count("TCD Chapter", {"course": course}), 1)

		with self.assertRaises(frappe.ValidationError):
			api.studio_save_course(json.dumps({"name": course, "chapters": [{"title": " ", "items": []}]}))
		with self.assertRaises(frappe.ValidationError):
			api.studio_save_course(
				json.dumps({"name": course, "chapters": [{"title": "X", "items": [{"content": "missing"}]}]})
			)

		self.assertIn(a.name, [p.name for p in api.studio_find_pages("Lesson", self.space)])
		status, html, _ = render(f"/learn/studio/course?name={course}", self.author)
		self.assertEqual(status, 200)
		self.assertIn('id="tcd-studio-course"', html)

	def test_learner_cannot_use_course_api(self):
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.studio_save_course(json.dumps({"space": self.space, "title": "Nope"}))
		with self.assertRaises(frappe.PermissionError):
			api.studio_find_pages("x")

	def test_breadcrumb_titles_escaped(self):
		page = lesson(self.space, "Bold <b>title</b>")
		status, html, _ = render(f"/learn/{self.space}/{page.slug}", self.learner)
		self.assertEqual(status, 200)
		body = re.sub(r"<title>.*?</title>", "", html, flags=re.S)  # <title> is plain text for browsers
		self.assertNotIn("<b>title</b>", body)  # breadcrumb, header and body
		self.assertIn('<span itemprop="name">Bold &lt;b&gt;title&lt;/b&gt;</span>', body)
