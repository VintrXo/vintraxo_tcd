import json

import frappe

from vintraxo_tcd.api import search_content
from vintraxo_tcd.core.content import slugify
from vintraxo_tcd.core.search import normalize_text
from vintraxo_tcd.tests.base import TCDTestCase

USERS = {
	"author": ("tcd-author@test.local", ["TCD Content Author"]),
	"reviewer": ("tcd-reviewer@test.local", ["TCD Content Reviewer"]),
	"learner": ("tcd-learner@test.local", ["TCD Learner"]),
	"vip": ("tcd-vip@test.local", ["TCD Learner", "TCD Instructor"]),
}

BLOCKS = [
	{"type": "heading", "text": "مُقَدِّمَة", "level": 2},
	{"type": "paragraph", "text": "تعلّم بايثون خطوة بخطوة"},
	{"type": "code", "code": "print('hi')", "language": "python"},
	{"type": "list", "items": ["أولاً", "ثانياً"]},
	{"type": "playground", "language": "python", "code": "x = 1"},
]


def make_user(email, roles):
	if not frappe.db.exists("User", email):
		frappe.get_doc(
			{"doctype": "User", "email": email, "first_name": email.split("@")[0], "send_welcome_email": 0}
		).insert(ignore_permissions=True)
	user = frappe.get_doc("User", email)
	user.set("roles", [])
	user.add_roles(*roles)
	return email


def make_space(name, visibility="Public", roles=()):
	if frappe.db.exists("TCD Space", name):
		frappe.delete_doc("TCD Space", name, force=True, ignore_permissions=True)
	return frappe.get_doc(
		{
			"doctype": "TCD Space",
			"space_name": name,
			"title": name,
			"visibility": visibility,
			"allowed_roles": [{"role": r} for r in roles],
		}
	).insert()


def make_content(space, title, **kw):
	return frappe.get_doc(
		{"doctype": "TCD Content", "space": space, "title": title, "blocks": json.dumps(BLOCKS), **kw}
	).insert()


def publish(doc):
	frappe.set_user("Administrator")
	doc.reload()
	for status in ("In Review", "Approved", "Published"):
		doc.status = status
		doc.save()
	return doc


class TestP1Content(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		settings = frappe.get_single("TCD Settings")
		settings.require_approval_before_publish = 1
		settings.save()
		frappe.clear_document_cache("TCD Settings", "TCD Settings")

	def setUp(self):
		frappe.set_user("Administrator")
		frappe.db.delete("TCD Content Relation")
		frappe.db.delete("TCD Content Version")
		frappe.db.delete("TCD Content")
		frappe.db.delete("TCD Category")
		self.space = make_space("p1-public").name

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ search / slugs / blocks

	def test_normalize_arabic(self):
		self.assertEqual(normalize_text("مُقَدِّمَة"), "مقدمه")
		self.assertEqual(normalize_text("إسـلام  أحمد"), "اسلام احمد")
		self.assertEqual(normalize_text("مستوى ٣"), "مستوي 3")

	def test_slug_and_search_text(self):
		doc = make_content(self.space, "مقدمة في بايثون")
		self.assertEqual(doc.slug, slugify("مقدمة في بايثون"))
		self.assertEqual(doc.slug, "مقدمه-في-بايثون")
		self.assertIn("مقدمه", doc.search_text)
		self.assertIn("print('hi')", doc.search_text)
		self.assertIn("اولا", doc.search_text)

		dup = make_content(self.space, "مقدمة في بايثون")
		self.assertEqual(dup.slug, "مقدمه-في-بايثون-2")
		with self.assertRaises(frappe.ValidationError):
			make_content(self.space, "x", slug=doc.slug)

	def test_defaults_from_settings(self):
		doc = make_content(self.space, "Defaults")
		self.assertEqual(doc.visibility, "Internal")
		self.assertIn(doc.language, ("ar", "en"))

	def test_invalid_blocks(self):
		bad = [
			"not json",
			json.dumps({"type": "paragraph"}),
			json.dumps([{"type": "video", "url": "x"}]),
			json.dumps([{"type": "paragraph"}]),
			json.dumps([{"type": "heading", "text": "h", "level": 9}]),
			json.dumps([{"type": "playground", "language": "cobol", "code": "DISPLAY 1"}]),
			json.dumps([{"type": "image", "url": "javascript:alert(1)"}]),
			json.dumps([{"type": "list", "items": [1, 2]}]),
		]
		for blocks in bad:
			with self.assertRaises(frappe.ValidationError, msg=blocks):
				frappe.get_doc(
					{"doctype": "TCD Content", "space": self.space, "title": "Bad", "blocks": blocks}
				).insert()

	def test_unknown_block_keys_dropped(self):
		doc = frappe.get_doc(
			{
				"doctype": "TCD Content",
				"space": self.space,
				"title": "Clean",
				"blocks": json.dumps([{"type": "paragraph", "text": "a", "onclick": "x"}]),
			}
		).insert()
		self.assertEqual(json.loads(doc.blocks), [{"type": "paragraph", "text": "a"}])

	def test_search_api_normalizes(self):
		make_content(self.space, "مقدمة في البرمجة")
		results = search_content("مُقدِّمة")
		self.assertTrue(any(r.title == "مقدمة في البرمجة" for r in results))

	# ------------------------------------------------------------ workflow & versions

	def test_workflow_creates_versions(self):
		doc = make_content(self.space, "Workflow")
		with self.assertRaises(frappe.ValidationError):
			doc.status = "Published"
			doc.save()
		doc.reload()

		publish(doc)
		doc.reload()
		self.assertEqual(doc.status, "Published")
		self.assertTrue(doc.published_on)
		self.assertEqual(doc.current_version, f"{doc.name}-v1")

		# locked while published
		doc.title = "Changed"
		with self.assertRaises(frappe.ValidationError):
			doc.save()
		doc.reload()

		doc.status = "Draft"
		doc.title = "Changed"
		doc.save()
		publish(doc)
		doc.reload()
		self.assertEqual(doc.current_version, f"{doc.name}-v2")
		self.assertEqual(frappe.db.count("TCD Content Version", {"content": doc.name}), 2)
		self.assertEqual(frappe.db.get_value("TCD Content Version", f"{doc.name}-v1", "title"), "Workflow")

	def test_version_immutable(self):
		doc = publish(make_content(self.space, "Immutable"))
		version = frappe.get_doc("TCD Content Version", doc.current_version)
		version.title = "hack"
		with self.assertRaises(frappe.ValidationError):
			version.save(ignore_permissions=True)
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{"doctype": "TCD Content Version", "content": doc.name, "version_number": 9}
			).insert(ignore_permissions=True)

	def test_author_cannot_approve(self):
		frappe.set_user(self.author)
		doc = make_content(self.space, "Author piece", visibility="Public")
		doc.status = "In Review"
		doc.save()
		doc.status = "Approved"
		with self.assertRaises(frappe.PermissionError):
			doc.save()

		frappe.set_user(self.reviewer)
		doc = frappe.get_doc("TCD Content", doc.name)
		doc.status = "Approved"
		doc.save()
		self.assertEqual(doc.current_version, f"{doc.name}-v1")
		self.assertEqual(
			frappe.db.get_value("TCD Content Version", doc.current_version, "approved_by"), self.reviewer
		)

	def test_direct_publish_without_approval(self):
		settings = frappe.get_single("TCD Settings")
		settings.require_approval_before_publish = 0
		settings.save()
		try:
			frappe.set_user(self.author)
			doc = make_content(self.space, "Quick")
			doc.status = "Published"
			doc.save()
			self.assertTrue(doc.current_version)
		finally:
			frappe.set_user("Administrator")
			settings.reload()
			settings.require_approval_before_publish = 1
			settings.save()

	def test_delete_content_cleans_up(self):
		doc = publish(make_content(self.space, "Delete me"))
		other = make_content(self.space, "Other")
		frappe.get_doc(
			{"doctype": "TCD Content Relation", "from_content": other.name, "to_content": doc.name}
		).insert()
		frappe.delete_doc("TCD Content", doc.name)
		self.assertFalse(frappe.db.exists("TCD Content Version", {"content": doc.name}))
		self.assertFalse(frappe.db.exists("TCD Content Relation", {"to_content": doc.name}))

	# ------------------------------------------------------------ structure

	def test_category_rules(self):
		parent = frappe.get_doc(
			{"doctype": "TCD Category", "category_name": "Python", "space": self.space}
		).insert()
		child = frappe.get_doc(
			{
				"doctype": "TCD Category",
				"category_name": "Basics",
				"space": self.space,
				"parent_category": parent.name,
			}
		).insert()
		parent.parent_category = child.name
		with self.assertRaises(frappe.ValidationError):
			parent.save()

		other_space = make_space("p1-other").name
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "TCD Category",
					"category_name": "X",
					"space": other_space,
					"parent_category": parent.name,
				}
			).insert()
		with self.assertRaises(frappe.ValidationError):
			make_content(other_space, "Wrong category", category=parent.name)

	def test_relation_rules(self):
		a = make_content(self.space, "A")
		b = make_content(self.space, "B")

		def rel(f, t, kind="Prerequisite"):
			return frappe.get_doc(
				{"doctype": "TCD Content Relation", "from_content": f, "to_content": t, "relation_type": kind}
			).insert()

		rel(a.name, b.name)
		for f, t in ((a.name, a.name), (a.name, b.name), (b.name, a.name)):
			with self.assertRaises(frappe.ValidationError):
				rel(f, t)
		rel(b.name, a.name, "Related")

	def test_space_id_validation(self):
		with self.assertRaises(frappe.ValidationError):
			make_space("Bad Space!")

	# ------------------------------------------------------------ permissions

	def test_learner_sees_only_published_public(self):
		internal_space = make_space("p1-internal", "Internal").name
		draft = make_content(self.space, "Draft public", visibility="Public")
		pub = publish(make_content(self.space, "Published public", visibility="Public"))
		pub_internal = publish(make_content(self.space, "Published internal", visibility="Internal"))
		in_internal_space = publish(make_content(internal_space, "In internal space", visibility="Public"))

		frappe.set_user(self.learner)
		visible = set(frappe.get_list("TCD Content", pluck="name"))
		self.assertEqual(visible, {pub.name})
		self.assertTrue(frappe.has_permission("TCD Content", "read", pub.name))
		for doc in (draft, pub_internal, in_internal_space):
			self.assertFalse(frappe.has_permission("TCD Content", "read", doc.name), doc.title)
		self.assertNotIn(internal_space, frappe.get_list("TCD Space", pluck="name"))
		# learner cannot read versions at all (no DocPerm)
		self.assertFalse(frappe.has_permission("TCD Content Version", "read"))

		frappe.set_user(self.author)
		visible = set(frappe.get_list("TCD Content", pluck="name"))
		self.assertTrue({draft.name, pub.name, pub_internal.name, in_internal_space.name} <= visible)

	def test_restricted_space_and_content(self):
		vip_space = make_space("p1-vip", "Restricted", roles=["TCD Instructor"]).name
		in_vip = publish(make_content(vip_space, "VIP lesson", visibility="Public"))
		restricted = publish(make_content(self.space, "Restricted lesson", visibility="Restricted"))

		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Content", "read", in_vip.name))
		self.assertFalse(frappe.has_permission("TCD Space", "read", vip_space))
		self.assertFalse(frappe.has_permission("TCD Content", "read", restricted.name))

		frappe.set_user(self.vip)
		self.assertTrue(frappe.has_permission("TCD Content", "read", in_vip.name))
		self.assertIn(in_vip.name, frappe.get_list("TCD Content", pluck="name"))
		# public space has no allowed roles: restricted content there stays hidden
		self.assertFalse(frappe.has_permission("TCD Content", "read", restricted.name))

		frappe.set_user(self.author)
		self.assertNotIn(in_vip.name, frappe.get_list("TCD Content", pluck="name"))

	def test_inactive_space_hidden(self):
		pub = publish(make_content(self.space, "Soon hidden", visibility="Public"))
		frappe.db.set_value("TCD Space", self.space, "is_active", 0)
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Content", "read", pub.name))
		self.assertEqual(frappe.get_list("TCD Content", pluck="name"), [])
