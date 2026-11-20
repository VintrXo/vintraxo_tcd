import frappe

from vintraxo_tcd.core import wiki
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import make_content, make_space
from vintraxo_tcd.tests.test_ph1_courses import CLEAN


class TestPhase29ParagraphMarkdown(TCDTestCase):
	def setUp(self):
		frappe.set_user("Administrator")
		for dt in CLEAN:
			frappe.db.delete(dt)
		self.space = make_space("ph29-space").name
		self.target = make_content(self.space, "Target page")

	def html(self, block):
		return wiki.prepare_blocks([block], self.space)[0].get("html")

	def test_plain_text_stays_plain(self):
		for text in ("plain text", "price 2*3*4", "snake_case_name", "a < b"):
			self.assertIsNone(self.html({"type": "paragraph", "text": text}), text)

	def test_markdown_in_paragraph_and_callout(self):
		html = self.html({"type": "paragraph", "text": "Press **Save** or `Ctrl` + *S*"})
		self.assertIn("<strong>Save</strong>", html)
		self.assertIn("<code>Ctrl</code>", html)
		self.assertIn("<em>S</em>", html)
		self.assertNotIn("<p>", html)  # fits inside the paragraph's own <p>
		self.assertEqual(self.html({"type": "paragraph", "text": r"file\_name"}), "file_name")
		html = self.html({"type": "callout", "text": "Steps:\n\n- one\n- **two**"})
		self.assertIn("<li><strong>two</strong></li>", html)

	def test_links_and_sanitizing(self):
		html = self.html({"type": "paragraph", "text": f"See **[[{self.target.slug}|the target]]**"})
		self.assertIn("the target</a></strong>", html)
		html = self.html(
			{"type": "paragraph", "text": "**x** <script>alert(1)</script> <img src=x onerror=alert(1)>"}
		)
		self.assertNotIn("<script", html)
		self.assertNotIn("onerror", html)
		html = self.html({"type": "paragraph", "text": "[bad](javascript:alert(1)) **x**"})
		self.assertNotIn("javascript:", html)


class TestEnrollmentNotificationSubject(TCDTestCase):
	def test_subject_shows_the_course_title(self):
		from vintraxo_tcd.tests.test_ph1_courses import lesson, make_course

		frappe.set_user("Administrator")
		for dt in CLEAN:
			frappe.db.delete(dt)
		space = make_space("ph29-notif").name
		course = make_course(space, "Readable course title", [[lesson(space, "L1")]])
		notification = frappe.get_doc("Notification", "TCD Enrollment Created")
		self.assertLessEqual(len(notification.subject), 140)
		doc = frappe._dict(course=course.name, learning_path=None)
		subject = frappe.render_template(notification.subject, {"doc": doc})
		self.assertIn("Readable course title", subject)
		self.assertNotIn(course.name, subject)
