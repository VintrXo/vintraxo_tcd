import json
import os
import tempfile

import frappe

from vintraxo_tcd.core import move
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import make_content, make_space
from vintraxo_tcd.tests.test_ph1_courses import CLEAN


class TestPhase27Move(TCDTestCase):
	def setUp(self):
		frappe.set_user("Administrator")
		for dt in CLEAN:
			frappe.db.delete(dt)
		frappe.db.delete("TCD Space", {"name": "ph27-copy"})
		self.space = make_space("ph27-space").name
		make_content(self.space, "Moved page")

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_export_then_import_once(self):
		with tempfile.TemporaryDirectory() as d:
			paths = move.export_spaces(d, [self.space])
			self.assertEqual(paths, [os.path.join(d, f"{self.space}.json")])
			self.assertEqual(oct(os.stat(paths[0]).st_mode & 0o777), "0o600")
			with open(paths[0], encoding="utf-8") as f:
				bundle = json.load(f)
			bundle["space"]["space_name"] = "ph27-copy"  # as if on another server
			with open(paths[0], "w", encoding="utf-8") as f:
				json.dump(bundle, f)

			lang = frappe.local.lang
			frappe.local.lang = None  # as under `bench execute`: notifications must still work
			try:
				report = move.import_spaces(d)
			finally:
				frappe.local.lang = lang
			self.assertIn("TCD Content: 1", report["ph27-copy"])
			self.assertEqual(frappe.db.count("TCD Content", {"space": "ph27-copy"}), 1)
			self.assertEqual(move.import_spaces(d)["ph27-copy"], "skipped (already here)")
			self.assertEqual(frappe.db.count("TCD Content", {"space": "ph27-copy"}), 1)

	def test_menu_and_images_travel(self):
		png = (
			b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15"
			b"\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
		)
		f = frappe.get_doc(
			{"doctype": "File", "file_name": "ph27-pic.png", "content": png, "is_private": 0}
		).insert()
		page = make_content(self.space, "With picture")
		page.blocks = json.dumps([{"type": "image", "url": f.file_url, "alt": "pic"}])
		page.save()
		sp = frappe.get_doc("TCD Space", self.space)
		sp.append("navigation", {"group_title": "Start", "link_type": "Page", "content": page.name})
		sp.append(
			"navigation",
			{
				"group_title": "Start",
				"link_type": "External Link",
				"url": "https://example.com",
				"label": "Out",
			},
		)
		sp.save()
		with tempfile.TemporaryDirectory() as d:
			move.export_spaces(d, [self.space])
			manifest = json.load(open(os.path.join(d, "files", "manifest.json")))
			self.assertIn(f.file_url, manifest)
			path = os.path.join(d, f"{self.space}.json")
			bundle = json.load(open(path))
			bundle["space"]["space_name"] = "ph27-copy"
			json.dump(bundle, open(path, "w"))
			frappe.delete_doc("File", f.name, force=True)  # as on a server that never had the picture

			move.import_spaces(d)
		copy = frappe.get_doc("TCD Space", "ph27-copy")
		new_page = frappe.db.get_value("TCD Content", {"space": "ph27-copy", "slug": page.slug})
		self.assertEqual([r.content for r in copy.navigation if r.link_type == "Page"], [new_page])
		self.assertEqual(
			[r.url for r in copy.navigation if r.link_type == "External Link"], ["https://example.com"]
		)
		url = json.loads(frappe.db.get_value("TCD Content", new_page, "blocks"))[0]["url"]
		restored = frappe.get_doc("File", {"file_url": url})
		self.assertEqual(open(restored.get_full_path(), "rb").read(), png)

	def test_cli_setup_sets_a_language(self):
		from frappe.locale import get_date_format

		from vintraxo_tcd.core.server_keys import cli_setup

		lang = frappe.local.lang
		frappe.local.lang = None  # as under `bench execute`
		try:
			cli_setup()  # without it Frappe 16.33 - 16.60 raises UnboundLocalError here
			self.assertTrue(frappe.local.lang)
			self.assertTrue(get_date_format())
		finally:
			frappe.local.lang = lang

	def test_not_callable_over_http(self):
		frappe.local.request = object()
		try:
			with self.assertRaises(frappe.PermissionError):
				move.export_spaces("/nonexistent")
		finally:
			del frappe.local.request
