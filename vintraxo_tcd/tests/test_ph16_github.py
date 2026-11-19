import base64
import json
from unittest.mock import MagicMock, patch

import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import github_sync
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson

REQ = "vintraxo_tcd.core.github_sync.requests"


def resp(code, data=None):
	r = MagicMock()
	r.status_code = code
	r.json.return_value = data if data is not None else {}
	return r


def b64(text):
	return base64.b64encode(text.encode()).decode()


class TestPhase16GitHub(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Change Request", *CLEAN):
			frappe.db.delete(dt)
		self.space = make_space("ph16g-space")
		self.space.update(
			{
				"github_repo": "VintrXo/handbook",
				"github_branch": "main",
				"github_path": "docs",
				"github_token": "ghp_x",
			}
		)
		self.space.save()
		self.page = lesson(
			self.space.name,
			"Onboarding",
			blocks=json.dumps(
				[
					{"type": "heading", "text": "Day one", "level": 2},
					{"type": "list", "items": ["Laptop", "Badge"]},
				]
			),
		)

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_markdown_round_trip(self):
		md = github_sync.to_markdown(frappe.get_doc("TCD Content", self.page.name))
		self.assertIn('title: "Onboarding"', md)
		self.assertIn("### Day one", md)
		self.assertIn("- Laptop", md)
		meta, body = github_sync.parse_markdown(md)
		self.assertEqual((meta["tcd_id"], meta["title"]), (self.page.name, "Onboarding"))
		self.assertTrue(body.startswith("### Day one"))

	def test_push_writes_and_skips_unchanged(self):
		with patch(REQ) as req:
			req.get.return_value = resp(404)
			req.put.return_value = resp(201)
			self.assertEqual(api.github_push(self.space.name), {"written": 1, "unchanged": 0})
		url = req.put.call_args.args[0]
		self.assertEqual(
			url, f"https://api.github.com/repos/VintrXo/handbook/contents/docs/{self.page.slug}.md"
		)
		payload = req.put.call_args.kwargs["json"]
		self.assertEqual(payload["branch"], "main")
		self.assertIn("Day one", base64.b64decode(payload["content"]).decode())
		self.assertEqual(req.put.call_args.kwargs["headers"]["Authorization"], "Bearer ghp_x")
		same = github_sync.to_markdown(frappe.get_doc("TCD Content", self.page.name))
		with patch(REQ) as req:
			req.get.return_value = resp(200, {"sha": "abc", "content": b64(same)})
			self.assertEqual(api.github_push(self.space.name), {"written": 0, "unchanged": 1})
			req.put.assert_not_called()

	def test_pull_creates_drafts_and_suggestions(self):
		changed = github_sync.to_markdown(frappe.get_doc("TCD Content", self.page.name)).replace(
			"Badge", "ID card"
		)
		new_file = '---\ntitle: "Holidays"\n---\n\nWe have **20** days.'
		listing = [
			{"type": "file", "name": f"{self.page.slug}.md", "url": "https://api.github.com/x/1"},
			{"type": "file", "name": "holidays.md", "url": "https://api.github.com/x/2"},
			{"type": "file", "name": "image.png", "url": "https://api.github.com/x/3"},
		]

		def fake_get(url, **kw):
			if url.endswith("/contents/docs"):
				return resp(200, listing)
			return resp(200, {"content": b64(changed if url.endswith("/1") else new_file)})

		with patch(REQ) as req:
			req.get.side_effect = fake_get
			self.assertEqual(api.github_pull(self.space.name), {"created": 1, "suggested": 1, "unchanged": 0})
		draft = frappe.get_doc("TCD Content", {"space": self.space.name, "title": "Holidays"})
		self.assertEqual(draft.status, "Draft")  # never published directly
		cr = frappe.get_doc("TCD Change Request", {"content": self.page.name})
		self.assertIn("ID card", cr.proposed_blocks)
		self.assertIn(
			"Badge", frappe.db.get_value("TCD Content", self.page.name, "blocks")
		)  # page unchanged until accepted

	def test_admins_only(self):
		frappe.set_user(self.author)
		with self.assertRaises(frappe.PermissionError):
			api.github_push(self.space.name)
		frappe.set_user("Administrator")
		self.space.github_repo = "not a repo"
		self.space.save()
		with self.assertRaises(frappe.ValidationError):
			api.github_pull(self.space.name)
