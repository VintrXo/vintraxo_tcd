import io
import json
import os
import shutil
import zipfile

import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import progress
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson

MANIFEST = """<?xml version="1.0"?>
<manifest identifier="m" xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2">
  <organizations default="o"><organization identifier="o"><item identifier="i1" identifierref="r1"><title>T</title></item></organization></organizations>
  <resources><resource identifier="r1" type="webcontent" href="course/index.html"/></resources>
</manifest>"""


def make_zip(files: dict) -> bytes:
	buf = io.BytesIO()
	with zipfile.ZipFile(buf, "w") as z:
		for name, data in files.items():
			z.writestr(name, data)
	return buf.getvalue()


class TestPhase16Scorm(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in CLEAN:
			frappe.db.delete(dt)
		frappe.get_single("TCD Settings").update({"enable_portal": 1, "allow_scorm": 1}).save()
		self.space = make_space("ph16s-space").name
		self.page = lesson(self.space, "Scorm lesson")
		self.files = []

	def tearDown(self):
		frappe.set_user("Administrator")
		frappe.get_single("TCD Settings").update({"allow_scorm": 0}).save()
		shutil.rmtree(
			frappe.get_site_path("public", "files", "scorm"), ignore_errors=True
		)  # disk is not rolled back
		for path in self.files:
			if os.path.exists(path):
				os.remove(path)

	def upload(self, files: dict, name="pkg.zip") -> str:
		f = frappe.get_doc(
			{"doctype": "File", "file_name": name, "is_private": 1, "content": make_zip(files)}
		).insert()
		self.files.append(f.get_full_path())
		return f.file_url

	def attach(self, url, user="Administrator"):
		frappe.set_user(user)
		doc = frappe.get_doc("TCD Content", self.page.name)
		doc.status = "Draft" if doc.status == "Published" else doc.status
		doc.save()
		doc.scorm_package = url
		doc.lesson_type = "SCORM"
		doc.save()
		return doc

	def test_install_and_complete(self):
		url = self.upload({"imsmanifest.xml": MANIFEST, "course/index.html": "<html>ok</html>"})
		doc = self.attach(url)
		self.assertTrue(doc.scorm_launch.startswith("/files/scorm/"))
		self.assertTrue(doc.scorm_launch.endswith("/course/index.html"))
		self.assertTrue(os.path.exists(frappe.get_site_path("public", doc.scorm_launch.lstrip("/"))))
		for status in ("In Review", "Approved", "Published"):
			doc.status = status
			doc.save()

		status, html, _ = render(f"/learn/{self.space}/{doc.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-scorm-frame", html)
		frappe.set_user(self.learner)
		api.scorm_commit(doc.name, json.dumps({"cmi.core.lesson_location": "p3", "evil.key": "x"}))
		self.assertEqual(api.scorm_data(doc.name), {"cmi.core.lesson_location": "p3"})  # only cmi.* kept
		self.assertNotEqual(progress.get_progress(self.learner, doc.name).status, "Completed")
		self.assertTrue(api.scorm_commit(doc.name, {"cmi.core.lesson_status": "completed"})["completed"])
		self.assertEqual(progress.get_progress(self.learner, doc.name).status, "Completed")
		with self.assertRaises(frappe.ValidationError):
			api.scorm_commit(doc.name, {f"cmi.interactions.{i}.result": "x" * 4000 for i in range(20)})

	def test_unsafe_packages_and_permissions(self):
		with self.assertRaises(frappe.ValidationError):
			self.attach(self.upload({"imsmanifest.xml": MANIFEST, "../evil.html": "x"}, "slip.zip"))
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			self.attach(self.upload({"index.html": "x"}, "nomanifest.zip"))
		bomb = '<?xml version="1.0"?><!DOCTYPE m [<!ENTITY a "aaaa"><!ENTITY b "&a;&a;&a;">]><manifest>&b;</manifest>'
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			self.attach(self.upload({"imsmanifest.xml": bomb}, "bomb.zip"))  # defusedxml refuses entities
		frappe.set_user("Administrator")
		good = self.upload({"imsmanifest.xml": MANIFEST, "course/index.html": "ok"}, "good.zip")
		with self.assertRaises(frappe.PermissionError):
			self.attach(good, self.author)  # authors cannot upload packages
		frappe.set_user("Administrator")
		frappe.get_single("TCD Settings").update({"allow_scorm": 0}).save()
		with self.assertRaises(frappe.ValidationError):
			self.attach(good)
		self.assertFalse(
			os.path.isdir(frappe.get_site_path("public", "files", "scorm"))
		)  # nothing was extracted
