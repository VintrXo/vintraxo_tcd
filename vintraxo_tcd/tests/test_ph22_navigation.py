import frappe

from vintraxo_tcd.core import navigation
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user, publish
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course


class TestPhase22Navigation(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (*CLEAN, "TCD Space Nav Item"):
			frappe.db.delete(dt)
		self.space = make_space("ph22-space")
		self.intro = lesson(self.space.name, "Start here")
		self.ref = lesson(self.space.name, "Reference <b>A</b>")
		self.hidden = publish(
			make_content(self.space.name, "Staff page", content_type="Lesson", visibility="Restricted")
		)
		self.course = make_course(self.space.name, "Nav course", [[self.intro]])

	def tearDown(self):
		frappe.set_user("Administrator")

	def set_nav(self, rows):
		self.space.reload()
		self.space.set("navigation", rows)
		self.space.save()

	def test_menu_groups_order_and_permissions(self):
		self.set_nav(
			[
				{"group_title": "Getting started", "link_type": "Page", "content": self.intro.name},
				{"group_title": "Getting started", "link_type": "Course", "course": self.course.name},
				{"group_title": "Reference", "link_type": "Page", "content": self.ref.name},
				{"group_title": "Reference", "link_type": "Page", "content": self.hidden.name},
				{
					"group_title": "Links",
					"link_type": "External Link",
					"url": "https://frappe.io",
					"label": "Frappe",
				},
			]
		)
		frappe.set_user(self.learner)
		menu = navigation.outline(self.space.name, current=self.ref.name)
		self.assertEqual([g["title"] for g in menu["groups"]], ["Getting started", "Reference", "Links"])
		self.assertEqual(
			[i["title"] for i in menu["groups"][1]["items"]], ["Reference <b>A</b>"]
		)  # restricted page left out
		self.assertTrue(menu["groups"][1]["items"][0]["current"])
		self.assertTrue(menu["groups"][2]["items"][0]["external"])

		status, html, _ = render(f"/learn/{self.space.name}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-with-outline", html)
		self.assertIn("Reference &lt;b&gt;A&lt;/b&gt;", html)
		self.assertNotIn("Staff page", html)
		self.assertIn("tcd_portal.js", html)  # theme button and menu behaviour
		status, html, _ = render(f"/learn/{self.space.name}/{self.ref.slug}", self.learner)
		self.assertIn('class="tcd-outline-item is-open is-current"', html)

	def test_course_menu_wins_over_space_menu(self):
		self.set_nav([{"group_title": "G", "link_type": "Page", "content": self.ref.name}])
		_status, html, _ = render(
			f"/learn/{self.space.name}/{self.intro.slug}?course={self.course.name}", self.learner
		)
		self.assertIn("Nav course", html)
		self.assertNotIn('<p class="tcd-outline-group">G</p>', html)

	def test_validation(self):
		other = make_space("ph22-other")
		foreign = lesson(other.name, "Foreign")
		for rows in (
			[{"group_title": "G", "link_type": "Page", "content": foreign.name}],
			[{"group_title": "G", "link_type": "Page"}],
			[{"group_title": "G", "link_type": "External Link", "url": "javascript:alert(1)", "label": "x"}],
			[{"group_title": "G", "link_type": "External Link", "url": "https://x.io"}],
		):
			with self.assertRaises(frappe.ValidationError):
				self.set_nav(rows)
		self.set_nav(
			[
				{
					"group_title": "G",
					"link_type": "Page",
					"content": self.intro.name,
					"url": "https://left.over",
				}
			]
		)
		self.assertIsNone(self.space.navigation[0].url)  # fields of other link types are cleared

	def test_no_menu_without_rows(self):
		self.assertIsNone(navigation.outline(self.space.name))
		_status, html, _ = render(f"/learn/{self.space.name}", self.learner)
		self.assertNotIn("tcd-with-outline", html)
