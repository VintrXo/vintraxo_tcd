"""Shared base class for vintraxo_tcd tests.

The tests clean whole TCD tables in setUp and rely on the transaction being rolled back at the end.
Some Frappe functions commit internally (e.g. `trigger_daily_alerts`), which once made those deletes permanent
on the development site. While a TCD test class runs, `frappe.db.commit` is a no-op, so nothing a test does can
outlive it.
"""

from unittest.mock import patch

import frappe
from frappe.tests import IntegrationTestCase


class TCDTestCase(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		cls._commit_guard = patch.object(frappe.db, "commit", lambda *args, **kwargs: None)
		cls._commit_guard.start()
		super().setUpClass()

	@classmethod
	def tearDownClass(cls):
		try:
			super().tearDownClass()
		finally:
			frappe.db.rollback()
			cls._commit_guard.stop()
