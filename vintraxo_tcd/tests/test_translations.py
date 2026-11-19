"""Arabic coverage: every DocType name, field label, description and Select option of the app
must have an Arabic translation (plain key or DocType context), and no Arabic text may keep
the "TCD" prefix. Keeps later phases honest about translations."""

import csv
import glob
import json
import os
import re

import frappe

from vintraxo_tcd.tests.base import TCDTestCase

LANG_CODES = re.compile(r"^[a-z]{2}$")
NOT_TRANSLATED = {"VX", "JSON", "SQL", "java", "cpp", "c", "csharp", "bash"}  # brand and technical names
LAYOUT = {"Section Break", "Column Break", "Tab Break"}


def load_ar():
	path = frappe.get_app_path("vintraxo_tcd", "translations", "ar.csv")
	plain, context = {}, {}
	with open(path, encoding="utf-8") as f:
		for row in csv.reader(f):
			if len(row) == 3 and row[2]:
				context[(row[0], row[2])] = row[1]
			elif len(row) >= 2:
				plain[row[0]] = row[1]
	return plain, context


def app_doctypes():
	base = frappe.get_app_path("vintraxo_tcd", "vintraxo_tcd", "doctype")
	for path in sorted(glob.glob(os.path.join(base, "*", "*.json"))):
		with open(path, encoding="utf-8") as f:
			yield json.load(f)


def app_reports():
	base = frappe.get_app_path("vintraxo_tcd", "vintraxo_tcd", "report")
	for path in sorted(glob.glob(os.path.join(base, "*", "*.json"))):
		with open(path, encoding="utf-8") as f:
			yield json.load(f)["name"]


class TestArabicTranslations(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.plain, cls.context = load_ar()

	def translated(self, text, doctype=None):
		return text in NOT_TRANSLATED or text in self.plain or (text, doctype) in self.context

	def test_doctype_and_report_names(self):
		missing = [d["name"] for d in app_doctypes() if not self.translated(d["name"])]
		missing += [r for r in app_reports() if not self.translated(r)]
		self.assertEqual(missing, [], "DocType/report names without Arabic")

	def test_field_labels_descriptions_and_options(self):
		missing = []
		for d in app_doctypes():
			dt = d["name"]
			for f in d["fields"]:
				texts = []
				if f.get("label") and not (f["fieldtype"] in LAYOUT and not f.get("label")):
					texts.append(f["label"])
				if f.get("description"):
					texts.append(f["description"])
				if f["fieldtype"] == "Select" and f.get("options"):
					texts += [o for o in f["options"].split("\n") if o and not LANG_CODES.match(o)]
				missing += [f"{dt}: {t}" for t in texts if not self.translated(t, dt)]
		self.assertEqual(missing, [], "Labels/descriptions/options without Arabic")

	def test_grid_and_list_values_have_plain_keys(self):
		"""Frappe translates Select values (lists, grids) and table descriptions WITHOUT context."""
		missing = []
		for d in app_doctypes():
			for f in d["fields"]:
				texts = []
				if f["fieldtype"] == "Select" and f.get("options"):
					texts += [o for o in f["options"].split("\n") if o and not LANG_CODES.match(o)]
				if f["fieldtype"] in ("Table", "Table MultiSelect") and f.get("description"):
					texts.append(f["description"])
				missing += [
					f"{d['name']}: {x}" for x in texts if x not in self.plain and x not in NOT_TRANSLATED
				]
		self.assertEqual(missing, [], "Values shown in lists/grids without a plain Arabic key")

	def test_no_tcd_prefix_in_arabic(self):
		bad = [k for k, v in self.plain.items() if "TCD" in v]
		bad += [f"{k} ({c})" for (k, c), v in self.context.items() if "TCD" in v]
		self.assertEqual(bad, [], "Arabic text still shows the TCD prefix")

	def test_values_are_arabic(self):
		arabic = re.compile("[؀-ۿ]")
		bad = [k for k, v in self.plain.items() if not arabic.search(v) and k not in NOT_TRANSLATED]
		self.assertEqual(bad, [], "Translations that contain no Arabic")
