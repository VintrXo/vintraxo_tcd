import json

import frappe
from frappe.utils import add_days, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import careers
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_user
from vintraxo_tcd.tests.test_p3 import render


class TestPhase16Careers(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		cls.other = make_user("tcd-other@test.local", ["TCD Learner"])
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()
		for name in ("Python", "SQL"):
			if not frappe.db.exists("TCD Skill", name):
				frappe.get_doc({"doctype": "TCD Skill", "skill_name": name}).insert()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			"TCD Learner Profile",
			"TCD Job Opening",
			"TCD Job Skill",
			"TCD Job Application",
			"TCD User Skill",
		):
			frappe.db.delete(dt)
		frappe.db.delete("TCD User Skill", {"user": self.learner})

	def tearDown(self):
		frappe.set_user("Administrator")

	def job(self, **kw):
		return frappe.get_doc(
			{
				"doctype": "TCD Job Opening",
				"title": "Data analyst",
				"hiring_manager": self.vip,
				"required_skills": [{"skill": "Python", "level": "2"}, {"skill": "SQL", "level": "1"}],
				**kw,
			}
		).insert()

	def test_profile_privacy(self):
		frappe.set_user(self.learner)
		api.save_profile(
			json.dumps(
				{
					"headline": "<b>Analyst</b>",
					"experience": [{"company": "VX", "job_title": "Intern", "from_year": "2024"}],
				}
			)
		)
		status, html, _ = render("/learn/profile", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("&lt;b&gt;Analyst&lt;/b&gt;", html)  # escaped
		self.assertIn("tcd-profile-form", html)
		self.assertEqual(
			render(f"/learn/profile?user={self.learner}", self.other)[0], 404
		)  # private by default
		frappe.set_user(self.learner)
		api.save_profile({"headline": "Analyst", "public_profile": 1})
		status, html, _ = render(f"/learn/profile?user={self.learner}", self.other)
		self.assertEqual(status, 200)
		self.assertNotIn("tcd-profile-form", html)  # only the owner edits
		self.assertEqual(render("/learn/profile", "Guest")[0], 302)
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			frappe.set_user(self.author)
			frappe.get_doc({"doctype": "TCD Learner Profile", "user": self.author}).insert(
				ignore_permissions=True
			)

	def test_jobs_match_apply_and_review(self):
		job = self.job()
		closed = self.job(title="Old role", closes_on=add_days(nowdate(), -1))
		frappe.get_doc(
			{"doctype": "TCD User Skill", "user": self.learner, "skill": "Python", "level": 3}
		).insert(ignore_permissions=True)
		frappe.set_user(self.learner)
		jobs = careers.open_jobs(self.learner)
		self.assertEqual([j["name"] for j in jobs], [job.name])  # closed one hidden
		self.assertEqual(jobs[0]["match"], 50)  # Python met, SQL missing
		status, html, _ = render("/learn/jobs", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("Data analyst", html)
		name = api.apply_for_job(job.name, "I like data")
		with self.assertRaises(frappe.ValidationError):
			api.apply_for_job(job.name, "again")
		with self.assertRaises(frappe.ValidationError):
			api.apply_for_job(closed.name, "late")
		self.assertTrue(
			frappe.get_all(
				"Notification Log", filters={"for_user": self.vip, "document_type": "TCD Job Application"}
			)
		)

		frappe.set_user(self.vip)  # the hiring manager reviews
		self.assertEqual(frappe.get_list("TCD Job Application", pluck="name"), [name])
		app = frappe.get_doc("TCD Job Application", name)
		app.status = "Reviewing"
		app.save()
		self.assertTrue(
			frappe.get_all(
				"Notification Log", filters={"for_user": self.learner, "document_type": "TCD Job Application"}
			)
		)
		frappe.set_user(self.reviewer)  # not the hiring manager
		self.assertEqual(frappe.get_list("TCD Job Application", pluck="name"), [])
		self.assertFalse(frappe.has_permission("TCD Job Application", "read", name))
		frappe.set_user(self.other)
		self.assertFalse(frappe.has_permission("TCD Job Application", "read"))
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({"doctype": "TCD Job Application", "job": job.name, "user": self.other}).insert()
