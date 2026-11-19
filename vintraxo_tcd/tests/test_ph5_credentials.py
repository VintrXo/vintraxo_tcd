import frappe
from frappe.utils import add_days, getdate, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import credentials
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, enrollment, lesson, make_course
from vintraxo_tcd.vintraxo_tcd.report.tcd_competency_gap import tcd_competency_gap as gap_report


class TestPhase5Credentials(TCDTestCase):
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
		for dt in ("TCD Certificate", "TCD User Skill", "TCD Competency Profile", "TCD Skill", *CLEAN):
			frappe.db.delete(dt)
		for child in (
			"TCD Learning Item",
			"TCD Course Instructor",
			"TCD Skill Award",
			"TCD Competency Requirement",
		):
			frappe.db.delete(child)
		for s in ("Python", "SQL"):
			frappe.get_doc({"doctype": "TCD Skill", "skill_name": s, "skill_group": "Programming"}).insert()
		self.space = make_space("ph5-space").name
		self.l1 = lesson(self.space, "Skill lesson 1")
		self.l2 = lesson(self.space, "Skill lesson 2")

	def tearDown(self):
		frappe.set_user("Administrator")

	def course(self, title, lessons, **kw):
		kw.setdefault("skills", [{"skill": "Python", "level": "2"}])
		kw.setdefault("issue_certificate", 1)
		kw.setdefault("certificate_validity_months", 12)
		return make_course(self.space, title, [lessons], instructors=[self.vip], **kw)

	# ------------------------------------------------------------ awarding

	def test_completion_awards_skill_and_certificate(self):
		basic = self.course("Basic", [self.l1])
		advanced = self.course(
			"Advanced", [self.l2], skills=[{"skill": "Python", "level": "4"}, {"skill": "SQL", "level": "3"}]
		)
		frappe.set_user(self.learner)
		api.enroll("Course", advanced.name)
		api.complete_lesson(self.l2.name)
		api.enroll("Course", basic.name)
		api.complete_lesson(self.l1.name)

		self.assertEqual(
			credentials.user_level(self.learner, "Python"), 4
		)  # never lowered by the basic course
		self.assertEqual(credentials.user_level(self.learner, "SQL"), 3)
		certs = frappe.get_all(
			"TCD Certificate",
			filters={"user": self.learner},
			fields=["course", "expires_on", "status", "verification_code"],
		)
		self.assertEqual({c.course for c in certs}, {basic.name, advanced.name})
		self.assertTrue(
			all(c.status == "Active" and c.expires_on and len(c.verification_code) == 16 for c in certs)
		)

		# recomputing does not issue a second certificate
		from vintraxo_tcd.core import courses

		credentials.on_completed(enrollment(self.learner, basic.name))
		courses.refresh_course(self.learner, basic.name)
		self.assertEqual(frappe.db.count("TCD Certificate", {"user": self.learner, "course": basic.name}), 1)

	def test_manual_approval_issues_on_approve(self):
		course = self.course("Approved", [self.l1], completion_rule="Manual Approval")
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		self.assertFalse(frappe.db.exists("TCD Certificate", {"user": self.learner}))
		frappe.set_user(self.vip)
		api.approve_enrollment(enrollment(self.learner, course.name).name)
		self.assertTrue(frappe.db.exists("TCD Certificate", {"user": self.learner, "course": course.name}))

	def test_user_skill_rules(self):
		frappe.get_doc(
			{
				"doctype": "TCD User Skill",
				"user": self.learner,
				"skill": "SQL",
				"level": "2",
				"source_type": "Manual",
			}
		).insert()
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{"doctype": "TCD User Skill", "user": self.learner, "skill": "SQL", "level": "3"}
			).insert()
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "TCD User Skill",
					"user": self.vip,
					"skill": "SQL",
					"level": "3",
					"source_type": "Course",
				}
			).insert()
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({"doctype": "TCD Certificate", "user": self.learner, "title": "Fake"}).insert(
				ignore_permissions=True
			)

	# ------------------------------------------------------------ lifecycle

	def test_expire_renew_revoke(self):
		course = self.course("Lifecycle", [self.l1])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		cert = frappe.get_doc("TCD Certificate", {"user": self.learner, "course": course.name})
		self.assertEqual(getdate(cert.expires_on), getdate(frappe.utils.add_months(nowdate(), 12)))

		frappe.set_user("Administrator")
		forever = credentials.issue_certificate(
			self.learner, "Course", self.course("No expiry", [self.l2], certificate_validity_months=0).name
		)
		self.assertIsNone(forever.expires_on)
		frappe.db.set_value("TCD Certificate", cert.name, "expires_on", add_days(nowdate(), -1))
		credentials.expire_certificates()
		self.assertEqual(frappe.db.get_value("TCD Certificate", cert.name, "status"), "Expired")
		# regression: certificates without an expiry date never expire
		self.assertEqual(frappe.db.get_value("TCD Certificate", forever.name, "status"), "Active")

		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.renew_certificate(cert.name)
		frappe.set_user(self.vip)
		new = api.renew_certificate(cert.name)
		self.assertEqual(
			frappe.db.get_value("TCD Certificate", cert.name, ["status", "renewed_by"]),
			("Renewed", new["name"]),
		)

		with self.assertRaises(frappe.PermissionError):
			api.revoke_certificate(new["name"], "fraud")
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			api.revoke_certificate(new["name"], " ")
		api.revoke_certificate(new["name"], "Shared answers")
		self.assertEqual(frappe.db.get_value("TCD Certificate", new["name"], "status"), "Revoked")

	# ------------------------------------------------------------ verification, PDF, permissions

	def test_public_verification(self):
		course = self.course("Verified", [self.l1])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		cert = frappe.get_doc("TCD Certificate", {"user": self.learner})

		frappe.set_user("Guest")
		data = api.verify_certificate(cert.verification_code)
		self.assertEqual((data["title"], data["status"]), ("Verified", "Active"))
		self.assertNotIn(self.learner, str(data))  # no e-mail exposed
		with self.assertRaises(frappe.DoesNotExistError):
			api.verify_certificate("not-a-real-code")

		status, html, _ = render(f"/verify/{cert.verification_code}", "Guest")
		self.assertEqual(status, 200)
		self.assertIn("Verified", html)
		self.assertNotIn(self.learner, html)
		status, _, _ = render("/verify/unknown-code-123", "Guest")
		self.assertEqual(status, 404)

	def test_pdf_and_print_format(self):
		course = self.course("Printed", [self.l1])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		cert = frappe.get_doc("TCD Certificate", {"user": self.learner})
		html = frappe.get_print("TCD Certificate", cert.name, "TCD Certificate")
		self.assertIn('dir="rtl"', html)
		self.assertIn("Printed", html)
		self.assertIn(f"/verify/{cert.verification_code}", html)
		pdf = frappe.get_print("TCD Certificate", cert.name, "TCD Certificate", as_pdf=True)
		self.assertTrue(pdf.startswith(b"%PDF"))

	def test_permissions(self):
		mine = self.course("Taught", [self.l1])
		other = make_course(
			self.space, "Other", [[self.l2]], issue_certificate=1, skills=[{"skill": "SQL", "level": "1"}]
		)
		frappe.set_user(self.learner)
		for c in (mine, other):
			api.enroll("Course", c.name)
		api.complete_lesson(self.l1.name)
		api.complete_lesson(self.l2.name)
		frappe.set_user(self.reviewer)
		api.enroll("Course", other.name)
		api.complete_lesson(self.l2.name)

		frappe.set_user(self.learner)
		self.assertEqual(
			{c.user for c in frappe.get_list("TCD Certificate", fields=["user"])}, {self.learner}
		)
		self.assertEqual(set(frappe.get_list("TCD User Skill", pluck="user")), {self.learner})
		frappe.set_user(self.vip)  # instructor of "Taught" only
		certs = frappe.get_list("TCD Certificate", fields=["user", "course"])
		self.assertEqual({(c.user, c.course) for c in certs}, {(self.learner, mine.name)})
		skill_users = set(frappe.get_list("TCD User Skill", pluck="user"))
		self.assertIn(self.learner, skill_users)
		self.assertNotIn(self.reviewer, skill_users)

	# ------------------------------------------------------------ competency gap

	def test_gap_report(self):
		self.course("Gap course", [self.l1], skills=[{"skill": "SQL", "level": "3"}])
		frappe.get_doc(
			{
				"doctype": "TCD Competency Profile",
				"profile_name": "Analyst",
				"role": "TCD Learner",
				"requirements": [
					{"skill": "SQL", "required_level": "3"},
					{"skill": "Python", "required_level": "1"},
				],
			}
		).insert()
		credentials.award_skill(self.learner, "Python", 2)
		_cols, rows, _m, _c, summary = gap_report.execute({"profile": "Analyst", "user": self.learner})
		by_skill = {r["skill"]: r for r in rows}
		self.assertEqual((by_skill["SQL"]["gap"], by_skill["Python"]["gap"]), (3, 0))
		self.assertIn("Gap course", by_skill["SQL"]["suggested"])
		self.assertEqual({s["label"]: s["value"] for s in summary}["Open Gaps"], 1)
		_c, all_rows, *_ = gap_report.execute({"profile": "Analyst", "only_gaps": 1})
		self.assertTrue(all(r["gap"] for r in all_rows))
		self.assertIn(self.learner, {r["user"] for r in all_rows})

	def test_portal_shows_credentials(self):
		course = self.course("Portal cert", [self.l1])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		status, html, _ = render("/learn/my", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("download_pdf", html)
		self.assertIn("tcd-level", html)
		status, html, _ = render(f"/learn/{self.space}/course/{course.slug}", self.learner)
		self.assertIn("/verify/", html)
