import json
from urllib.parse import parse_qsl, quote, unquote

import frappe
from frappe.utils import set_request
from frappe.website.serve import get_response

from vintraxo_tcd.core.portal import json_for_script
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user, publish

XSS_TITLE = "<script>alert('t')</script> عنوان"
XSS_TEXT = "<img src=x onerror=alert(1)>"


def render(url: str, user: str):
	"""Render a portal URL the way a browser request would (decoded path + query string)."""
	frappe.set_user(user)
	path, _, query = url.partition("?")
	path = unquote(path)
	set_request(method="GET", path=path, query_string=query)
	frappe.local.form_dict = frappe._dict(parse_qsl(query))
	response = get_response(path)
	return response.status_code, response.get_data(as_text=True), response.headers.get("Location", "")


class TestP3Portal(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		settings = frappe.get_single("TCD Settings")
		settings.update({"enable_portal": 1, "enable_playgrounds": 1, "require_approval_before_publish": 1})
		settings.save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Quiz", "TCD Progress", "TCD Content Relation", "TCD Content Version", "TCD Content"):
			frappe.db.delete(dt)
		self.space = make_space("p3-public").name
		self.lesson = publish(
			make_content(
				self.space,
				"مقدمة في بايثون",
				content_type="Lesson",
				visibility="Public",
				language="ar",
				blocks=json.dumps(
					[
						{"type": "paragraph", "text": XSS_TEXT},
						{"type": "code", "code": "print('<b>')", "language": "python"},
						{
							"type": "playground",
							"language": "python",
							"code": "print(1 < 2)",
							"expected_output": "True",
						},
					]
				),
			)
		)
		self.xss = publish(make_content(self.space, XSS_TITLE, content_type="Lesson", visibility="Public"))
		self.url = f"/learn/{self.space}/{quote(self.lesson.slug)}"

	def tearDown(self):
		frappe.set_user("Administrator")
		frappe.db.set_single_value("TCD Settings", "enable_portal", 1)

	def test_guest_redirected_to_login(self):
		status, _, location = render("/learn", "Guest")
		self.assertEqual(status, 302)
		self.assertIn("/login?redirect-to=/learn", location)

	def test_home_and_space(self):
		status, html, _ = render("/learn", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("p3-public", html)

		status, html, _ = render(f"/learn/{self.space}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn(quote(self.lesson.slug), html)

	def test_lesson_page_rtl_and_playground(self):
		status, html, _ = render(self.url, self.learner)
		self.assertEqual(status, 200)
		self.assertIn('dir="rtl"', html)
		self.assertIn("مقدمة في بايثون", html)
		self.assertIn('class="tcd-playground" data-language="python"', html)
		self.assertIn("print(1 &lt; 2)", html)
		self.assertIn("tcd_playground.js", html)
		self.assertIn("https://cdn.jsdelivr.net/pyodide/", html)

	def test_output_is_escaped(self):
		_, html, _ = render(self.url, self.learner)
		self.assertNotIn(XSS_TEXT, html)
		self.assertIn("&lt;img src=x onerror=alert(1)&gt;", html)
		self.assertNotIn("print('<b>')", html)

		_, html, _ = render(f"/learn/{self.space}/{quote(self.xss.slug)}", self.learner)
		self.assertNotIn("<script>alert('t')</script>", html)
		_, html, _ = render(f"/learn/{self.space}", self.learner)
		self.assertNotIn("<script>alert('t')</script>", html)
		_, html, _ = render("/learn?q=" + quote("<script>x</script>"), self.learner)
		self.assertNotIn("<script>x</script>", html)

	def test_hidden_content_is_404(self):
		draft = make_content(self.space, "Draft", content_type="Lesson", visibility="Public")
		internal_space = make_space("p3-internal", "Internal").name
		internal = publish(make_content(internal_space, "Internal", visibility="Public"))

		for path in (
			f"/learn/{self.space}/{quote(draft.slug)}",
			f"/learn/{internal_space}",
			f"/learn/{internal_space}/{quote(internal.slug)}",
			f"/learn/{self.space}/no-such-slug",
			"/learn/no-such-space",
		):
			status, _, _ = render(path, self.learner)
			self.assertEqual(status, 404, path)

		# staff can preview drafts
		status, html, _ = render(f"/learn/{self.space}/{quote(draft.slug)}", self.author)
		self.assertEqual(status, 200)
		self.assertIn("tcd-callout-warning", html)

	def test_search(self):
		status, html, _ = render("/learn?q=" + quote("مُقدِّمة"), self.learner)
		self.assertEqual(status, 200)
		self.assertIn("مقدمة في بايثون", html)

	def test_portal_disabled(self):
		frappe.db.set_single_value("TCD Settings", "enable_portal", 0)
		status, _, _ = render("/learn", self.learner)
		self.assertEqual(status, 404)

	def test_json_for_script(self):
		out = json_for_script({"a": "</script><script>alert(1)</script>&"})
		self.assertNotIn("<", out)
		self.assertNotIn("&", out)
		self.assertEqual(json.loads(out)["a"], "</script><script>alert(1)</script>&")

	def test_runtime_url_validation(self):
		settings = frappe.get_single("TCD Settings")
		settings.pyodide_index_url = "http://insecure.example/pyodide"
		with self.assertRaises(frappe.ValidationError):
			settings.validate()
		settings.pyodide_index_url = "/assets/pyodide"
		settings.validate()
		self.assertEqual(settings.pyodide_index_url, "/assets/pyodide/")
