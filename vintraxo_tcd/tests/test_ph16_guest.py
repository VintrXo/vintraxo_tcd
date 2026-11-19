import frappe
from frappe.utils import set_request

from vintraxo_tcd.core import permissions
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course


class TestPhase16Guest(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in CLEAN:
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		self.settings(0)
		self.space = make_space("ph16-public").name
		self.public = lesson(self.space, "Open page")
		self.internal = lesson(self.space, "Staff page")
		frappe.db.set_value("TCD Content", self.internal.name, "visibility", "Internal")
		self.draft = make_content(self.space, "Draft page", visibility="Public")
		self.secret_space = make_space("ph16-secret", visibility="Restricted", roles=("TCD Instructor",)).name
		self.secret = lesson(self.secret_space, "Secret page")
		self.course = make_course(self.space, "Open course", [[self.public]])

	def tearDown(self):
		frappe.set_user("Administrator")
		self.settings(0)

	def settings(self, on):
		frappe.get_single("TCD Settings").update({"enable_portal": 1, "enable_guest_access": on}).save()

	def test_off_by_default(self):
		status, _html, location = render("/learn", "Guest")
		self.assertEqual(status, 302)
		self.assertIn("/login", location)
		self.assertEqual(render(f"/learn/{self.space}/{self.public.slug}", "Guest")[0], 302)

	def test_visitors_read_public_published_only(self):
		self.settings(1)
		status, html, _ = render("/learn", "Guest")
		self.assertEqual(status, 200)
		status, html, _ = render(f"/learn/{self.space}", "Guest")
		self.assertEqual(status, 200)
		self.assertIn("Open page", html)
		self.assertNotIn("Staff page", html)
		self.assertNotIn("Draft page", html)
		status, html, _ = render(f"/learn/{self.space}/{self.public.slug}", "Guest")
		self.assertEqual(status, 200)
		self.assertIn("tcd-guest", html)
		self.assertNotIn("tcd-complete", html)
		self.assertNotIn("tcd-discussion-form", html)
		self.assertNotIn("tcd-notes", html)
		for page in (self.internal, self.draft):
			self.assertEqual(render(f"/learn/{self.space}/{page.slug}", "Guest")[0], 404)
		self.assertEqual(render(f"/learn/{self.secret_space}/{self.secret.slug}", "Guest")[0], 404)
		status, html, _ = render(f"/learn/{self.space}/course/{self.course.slug}", "Guest")
		self.assertEqual(status, 200)
		self.assertIn("/login?redirect-to=", html)
		for path in ("/learn/my", "/learn/policies", "/learn/team", "/learn/instructor"):
			status, _, _location = render(path, "Guest")
			self.assertIn(status, (302, 404), path)
		self.assertEqual(
			frappe.db.count("TCD Progress", {"user": "Guest"}), 0
		)  # nothing written for visitors

	def test_api_never_serves_visitors(self):
		self.settings(1)
		frappe.set_user("Guest")
		set_request(method="GET", path="/api/resource/TCD Content")
		self.assertFalse(permissions.guest_allowed())
		self.assertEqual(frappe.get_list("TCD Content", pluck="name"), [])
		self.assertFalse(frappe.has_permission("TCD Content", "read", self.public.name))
		self.assertFalse(frappe.has_permission("TCD Content", "write", self.public.name))
		set_request(method="GET", path="/learn")
		self.assertTrue(permissions.guest_allowed())
		self.assertEqual(frappe.get_list("TCD Content", pluck="name"), [self.public.name])
		self.assertFalse(frappe.has_permission("TCD Content", "write", self.public.name))
