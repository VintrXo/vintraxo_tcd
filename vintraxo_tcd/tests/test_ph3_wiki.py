import json

import frappe
from frappe.desk.doctype.tag.tag import add_tag

from vintraxo_tcd import api
from vintraxo_tcd.core import wiki
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user, publish
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN


def blocks(*items):
	return json.dumps(list(items), ensure_ascii=False)


def article(space, title, **kw):
	return publish(make_content(space, title, content_type="Article", visibility="Public", **kw))


class TestPhase3Wiki(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		settings = frappe.get_single("TCD Settings")
		settings.update({"require_approval_before_publish": 1, "enable_portal": 1})
		settings.save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Content Feedback", "TCD Content Template", *CLEAN):
			frappe.db.delete(dt)
		frappe.db.delete("Tag Link", {"document_type": "TCD Content"})
		self.space = make_space("ph3-wiki").name

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ markdown and links

	def test_markdown_is_sanitized(self):
		md = (
			"# Title\n\n**bold** and [x](javascript:alert(1))\n\n<script>alert(1)</script>"
			'<img src=x onerror="alert(1)"><meta http-equiv="refresh" content="0;url=https://evil">'
			'<link rel="stylesheet" href="https://evil/x.css"><iframe src="https://evil"></iframe>'
		)
		html = wiki.render_markdown(md, self.space)
		self.assertIn("<strong>bold</strong>", html)
		for bad in ("<script", "onerror", "javascript:", "<meta", "<link", "<iframe"):
			self.assertNotIn(bad, html.lower(), bad)

	def test_internal_links_and_backlinks(self):
		target = article(self.space, "Target Page")
		draft = make_content(self.space, "Draft Page", content_type="Article", visibility="Public")
		source = article(
			self.space,
			"Source Page",
			blocks=blocks(
				{
					"type": "paragraph",
					"text": f"See [[{target.slug}]] and [[{draft.slug}|the draft]] <b>x</b>",
				},
				{"type": "markdown", "text": f"Also [[{self.space}/{target.slug}|this]]"},
			),
		)
		self.assertEqual(json.loads(source.internal_links), [target.name, draft.name])
		frappe.set_user(self.learner)
		self.assertEqual([b["name"] for b in wiki.backlinks(target.name)], [source.name])
		html = wiki.render_inline(
			f"See [[{target.slug}]] and [[{draft.slug}|the draft]] <b>x</b>", self.space
		)
		self.assertIn('<a class="tcd-wikilink"', html)
		self.assertIn("Target Page", html)
		self.assertIn("the draft", html)  # unreadable target: plain label
		self.assertEqual(html.count("<a "), 1)
		self.assertIn("&lt;b&gt;", html)

		status, page, _ = render(f"/learn/{self.space}/{source.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-wikilink", page)
		self.assertIn("tcd-markdown", page)
		status, page, _ = render(f"/learn/{self.space}/{target.slug}", self.learner)
		self.assertIn("Source Page", page)  # "Linked from"

	# ------------------------------------------------------------ page tree

	def test_page_tree(self):
		root = article(self.space, "Root")
		child = article(self.space, "Child", parent_content=root.name)
		article(self.space, "Grandchild", parent_content=child.name)
		other = make_space("ph3-other").name
		tutorial = make_content(self.space, "Tut", content_type="Tutorial")

		root.reload()
		root.status = "Draft"
		root.save()
		root.parent_content = child.name
		with self.assertRaises(frappe.ValidationError):
			root.save()  # loop
		for bad in (
			lambda: make_content(other, "Elsewhere", parent_content=root.name),
			lambda: make_content(self.space, "Under tutorial", parent_content=tutorial.name),
		):
			with self.assertRaises(frappe.ValidationError):
				bad()

		frappe.set_user("Administrator")
		publish(frappe.get_doc("TCD Content", root.name))
		tree = wiki.page_tree(self.space)
		node = next(n for n in tree if n["name"] == root.name)
		self.assertEqual(node["children"][0]["children"][0]["title"], "Grandchild")
		gc = frappe.db.get_value("TCD Content", {"title": "Grandchild"})
		self.assertEqual([a.title for a in wiki.ancestors(gc)], ["Root", "Child"])
		status, page, _ = render(f"/learn/{self.space}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-tree", page)

	# ------------------------------------------------------------ versions

	def test_compare_and_restore(self):
		doc = article(self.space, "Versioned", blocks=blocks({"type": "paragraph", "text": "first text"}))
		doc.reload()
		doc.status = "Draft"
		doc.save()
		doc.title = "Versioned v2"
		doc.blocks = blocks({"type": "paragraph", "text": "second text"})
		doc.save()
		publish(doc)
		v1, v2 = f"{doc.name}-v1", f"{doc.name}-v2"

		res = api.compare_versions(v1, v2)
		self.assertIn("-  first text", res["diff"])
		self.assertIn("+  second text", res["diff"])
		self.assertEqual(api.compare_versions(v2, doc.name)["diff"], [])

		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.restore_version(v1)
		with self.assertRaises(frappe.PermissionError):
			api.compare_versions(v1, v2)

		frappe.set_user(self.author)
		api.restore_version(v1)
		doc.reload()
		self.assertEqual((doc.status, doc.title), ("Draft", "Versioned"))
		self.assertIn("first text", doc.blocks)

	# ------------------------------------------------------------ feedback, tags, templates, archive

	def test_page_feedback(self):
		doc = article(self.space, "Helpful?")
		frappe.set_user(self.learner)
		api.content_feedback(doc.name, 0, "unclear")
		stats = api.content_feedback(doc.name, 1)
		self.assertEqual(stats, {"helpful": 1, "total": 1})
		frappe.set_user(self.vip)
		api.content_feedback(doc.name, 1)
		frappe.set_user(self.learner)
		self.assertEqual(len(frappe.get_list("TCD Content Feedback")), 1)  # own only
		frappe.set_user(self.reviewer)
		self.assertEqual(len(frappe.get_list("TCD Content Feedback")), 2)  # staff with access
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{"doctype": "TCD Content Feedback", "content": doc.name, "user": self.reviewer}
			).insert(ignore_permissions=True)

	def test_tags(self):
		a = article(self.space, "Tagged public")
		b = make_content(self.space, "Tagged draft", content_type="Article", visibility="Public")
		for d in (a, b):
			add_tag("onboarding", "TCD Content", d.name)
		self.assertEqual(wiki.tags_of(a.name), ["onboarding"])
		frappe.set_user(self.learner)
		self.assertEqual(wiki.contents_with_tag("onboarding"), [a.name])
		status, page, _ = render("/learn?tag=onboarding", self.learner)
		self.assertIn("Tagged public", page)
		self.assertNotIn("Tagged draft", page)
		status, page, _ = render(f"/learn/{self.space}/{a.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("#onboarding", page)

	def test_templates(self):
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "TCD Content Template",
					"template_name": "Bad",
					"blocks": blocks({"type": "nope"}),
				}
			).insert()
		t = frappe.get_doc(
			{
				"doctype": "TCD Content Template",
				"template_name": "How-to",
				"content_type": "Article",
				"lesson_type": "Video",
				"blocks": blocks(
					{"type": "heading", "text": "Steps"}, {"type": "markdown", "text": "1. one"}
				),
			}
		).insert()
		self.assertIsNone(t.lesson_type)
		frappe.set_user(self.author)
		self.assertIn("Steps", api.get_template("How-to")["blocks"])
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.get_template("How-to")

	def test_archived_hidden_from_learners(self):
		doc = article(self.space, "Old page")
		doc.reload()
		doc.status = "Archived"
		doc.save()
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Content", "read", doc.name))
		status, page, _ = render(f"/learn/{self.space}/{doc.slug}", self.author)
		self.assertEqual(status, 200)
		self.assertIn("tcd-callout-danger", page)
