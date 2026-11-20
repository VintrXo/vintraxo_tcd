import json
import os
import tempfile

import frappe

from vintraxo_tcd.core import ops, server_keys
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import make_space

EXAMPLE = os.path.join(os.path.dirname(server_keys.__file__), "..", "..", "deploy", "keys.example.json")


class TestPhase26ServerKeys(TCDTestCase):
	def setUp(self):
		frappe.set_user("Administrator")
		frappe.get_single("TCD Settings").update(
			{"runner_enabled": 0, "runner_url": None, "meeting_provider": None, "payment_gateway": None}
		).save()
		frappe.get_single("TCD AI Settings").update({"enabled": 0}).save()
		for email in ("ph26-trial@test.local",):
			if not frappe.db.exists("User", email):
				frappe.get_doc({"doctype": "User", "email": email, "first_name": "Trial"}).insert()

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_example_file_changes_nothing_but_trial_accounts(self):
		with open(EXAMPLE, encoding="utf-8") as f:
			data = json.load(f)
		data["trial_accounts"] = None
		report = server_keys.apply(data)
		self.assertEqual({r["status"] for r in report.values()}, {"skipped"})
		self.assertFalse(frappe.get_single("TCD AI Settings").enabled)
		self.assertFalse(frappe.db.exists("Email Account", "REPLACE noreply@your-domain.com"))

	def test_keys_are_stored_encrypted(self):
		space = make_space("ph26-space").name
		report = server_keys.apply(
			{
				"ai": {"api_key": "sk-ant-test", "model": "claude-opus-5-5"},
				"runner": {"url": "https://judge0.example.com", "token": "rt"},
				"zoom": {"account_id": "a", "client_id": "c", "client_secret": "zs"},
				"github": {space: {"repo": "acme/docs", "token": "gh-t"}},
				"email": {
					"email_id": "noreply@ph26.test",
					"password": "pw",
					"smtp_server": "smtp.ph26.test",
				},
			}
		)
		for section in ("ai", "runner", "zoom", "github", "email"):
			self.assertEqual(report[section]["status"], "set", (section, report[section]))
		self.assertNotIn("sk-ant-test", json.dumps(report))  # names only, never values

		ai = frappe.get_single("TCD AI Settings")
		self.assertEqual((ai.enabled, ai.model), (1, "claude-opus-5-5"))
		self.assertEqual(ai.get_password("api_key"), "sk-ant-test")
		self.assertNotEqual(frappe.db.get_single_value("TCD AI Settings", "api_key"), "sk-ant-test")
		s = frappe.get_single("TCD Settings")
		self.assertEqual(
			(s.runner_enabled, s.runner_url, s.meeting_provider), (1, "https://judge0.example.com", "Zoom")
		)
		self.assertEqual(s.get_password("zoom_client_secret"), "zs")
		sp = frappe.get_doc("TCD Space", space)
		self.assertEqual((sp.github_repo, sp.get_password("github_token")), ("acme/docs", "gh-t"))
		acc = frappe.get_doc("Email Account", "noreply@ph26.test")
		self.assertEqual((acc.enable_outgoing, acc.default_outgoing, acc.smtp_port), (1, 1, "587"))

	def test_one_bad_section_does_not_stop_the_others(self):
		report = server_keys.apply(
			{
				"payment": {"gateway": "No Such Gateway"},
				"google_meet": {"google_calendar": "No Such Calendar"},
				"ai": {"api_key": "sk-ant-2"},
			}
		)
		self.assertEqual(report["google_meet"]["status"], "failed")
		self.assertEqual(report["ai"]["status"], "set")
		if frappe.db.exists("DocType", "Payment Gateway"):  # payments app installed: name is checked
			self.assertEqual(report["payment"]["status"], "failed")
			self.assertFalse(frappe.get_single("TCD Settings").payment_gateway)
		self.assertFalse(frappe.get_single("TCD Settings").google_calendar)
		self.assertTrue(frappe.db.exists("User", "ph26-trial@test.local"))  # earlier work kept

	def test_trial_accounts_disabled_and_readiness_warns(self):
		user = "learner1@vintraxo.local"
		if not frappe.db.exists("User", user):
			frappe.get_doc({"doctype": "User", "email": user, "first_name": "Learner"}).insert()
		frappe.db.set_value("User", user, "enabled", 1)
		self.assertTrue(any("trial accounts" in i["message"] for i in ops.readiness()))
		report = server_keys.apply({"trial_accounts": "disable"})
		self.assertIn(user, report["trial_accounts"]["keys"])
		self.assertEqual(frappe.db.get_value("User", user, "enabled"), 0)
		self.assertFalse(any("trial accounts" in i["message"] for i in ops.readiness()))

	def test_documents_and_placeholders(self):
		self.assertFalse(server_keys._filled("REPLACE me"))
		self.assertFalse(server_keys._filled("  "))
		self.assertTrue(server_keys._filled(0))
		report = server_keys.apply(
			{"documents": [{"doctype": "Google Settings", "enable": 0, "client_id": "", "client_secret": ""}]}
		)
		self.assertEqual(report["documents"]["status"], "skipped")
		report = server_keys.apply(
			{
				"documents": [
					{"doctype": "Google Settings", "enable": 1, "client_id": "cid", "client_secret": "cs"}
				]
			}
		)
		self.assertEqual(report["documents"]["keys"], ["Google Settings Google Settings"])
		self.assertEqual(frappe.get_single("Google Settings").get_password("client_secret"), "cs")

	def test_not_callable_over_http(self):
		with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
			json.dump({}, f)
		frappe.local.request = object()
		try:
			with self.assertRaises(frappe.PermissionError):
				server_keys.apply_keys(f.name)
		finally:
			del frappe.local.request
			os.unlink(f.name)
