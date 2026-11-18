import frappe
from frappe.tests import IntegrationTestCase

from vintraxo_tcd.install import TCD_ROLES


class TestP0Foundation(IntegrationTestCase):
	def test_roles_exist(self):
		for role in TCD_ROLES:
			self.assertTrue(frappe.db.exists("Role", role), f"Missing role {role}")

	def test_settings_defaults(self):
		settings = frappe.get_single("TCD Settings")
		self.assertIn(settings.default_language, ("ar", "en"))
		self.assertEqual(settings.default_visibility, "Internal")

	def test_settings_timeout_validation(self):
		settings = frappe.get_single("TCD Settings")
		settings.playground_timeout_seconds = 999
		with self.assertRaises(frappe.ValidationError):
			settings.validate()
