import frappe
from frappe.email.doctype.notification.notification import trigger_daily_alerts
from frappe.utils import add_days, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import analytics
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, enrollment, lesson, make_course
from vintraxo_tcd.tests.test_ph4_assessment import question


def logs(user, contains=None):
	rows = frappe.get_all(
		"Notification Log", filters={"for_user": user}, fields=["subject", "document_type", "document_name"]
	)
	return [r for r in rows if not contains or contains in (r.subject or "")]


class TestPhase7Notifications(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update(
			{"enable_portal": 1, "require_approval_before_publish": 1}
		).save()

	def setUp(self):
		frappe.set_user("Administrator")
		extra = (
			"TCD Certificate",
			"TCD Acknowledgment",
			"TCD Governance Version",
			"TCD Governance Document",
			"TCD Question",
			"TCD Assignment Submission",
			"TCD Assignment",
		)
		for dt in (*extra, *CLEAN):
			frappe.db.delete(dt)
		for child in (
			"TCD Learning Item",
			"TCD Course Instructor",
			"TCD Governance Role",
			"TCD Quiz Bank Item",
		):
			frappe.db.delete(child)
		frappe.db.delete("Notification Log")
		self.space = make_space("ph7-space").name
		self.l1 = lesson(self.space, "Notified lesson")

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ standard notifications

	def test_standard_notifications(self):
		self.assertEqual(frappe.db.count("Notification", {"module": "VintraXo TCD", "is_standard": 1}), 7)
		draft = make_content(self.space, "Needs review")
		draft.status = "In Review"
		draft.save()
		self.assertTrue(logs(self.reviewer, "Needs review"))

		course = make_course(
			self.space, "Notify course", [[self.l1]], issue_certificate=1, instructors=[self.vip]
		)
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		self.assertTrue([r for r in logs(self.learner) if r.document_type == "TCD Enrollment"])
		api.complete_lesson(self.l1.name)
		self.assertTrue([r for r in logs(self.learner) if r.document_type == "TCD Certificate"])

		frappe.set_user("Administrator")
		doc = frappe.get_doc(
			{
				"doctype": "TCD Governance Document",
				"title": "Approval needed",
				"code": "POL-N1",
				"document_owner": self.author,
				"approver": self.vip,
			}
		).insert()
		for status in ("Review", "Approval"):
			api.set_governance_status(doc.name, status)
		self.assertTrue(logs(self.reviewer, "Approval needed"))
		self.assertTrue(logs(self.vip, "Approval needed"))

	def test_due_soon_daily_alert(self):
		course = make_course(self.space, "Due course", [[self.l1]])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		frappe.set_user("Administrator")
		frappe.db.set_value(
			"TCD Enrollment", enrollment(self.learner, course.name).name, "due_date", add_days(nowdate(), 3)
		)
		frappe.db.delete("Notification Log")
		trigger_daily_alerts()
		self.assertTrue([r for r in logs(self.learner) if r.document_type == "TCD Enrollment"])

	# ------------------------------------------------------------ data-driven notifications

	def test_instructor_notifications(self):
		course = make_course(
			self.space, "Taught", [[self.l1]], rule="Manual Approval", instructors=[self.vip]
		)
		assignment = frappe.get_doc(
			{
				"doctype": "TCD Assignment",
				"title": "Essay task",
				"content": self.l1.name,
				"course": course.name,
				"max_score": 10,
				"pass_score": 5,
				"required_to_complete": 0,
			}
		).insert()
		essay = question("Essay", "Explain", points=2)
		quiz = frappe.get_doc(
			{
				"doctype": "TCD Quiz",
				"title": "Essay quiz",
				"content": self.l1.name,
				"pass_percentage": 50,
				"required_to_complete": 0,
				"bank_items": [{"question": essay.name}],
			}
		).insert()

		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.submit_assignment(assignment.name, answer_text="first")
		api.submit_assignment(assignment.name, answer_text="second")  # same subject: deduplicated
		api.submit_quiz(quiz.name, {essay.name: "text"})
		api.complete_lesson(self.l1.name)

		self.assertEqual(len(logs(self.vip, "Essay task")), 1)
		self.assertEqual(len([r for r in logs(self.vip) if r.document_type == "TCD Quiz Submission"]), 1)
		self.assertEqual(len([r for r in logs(self.vip) if r.document_type == "TCD Enrollment"]), 1)
		self.assertFalse(logs(self.reviewer, "Essay task"))  # not an instructor

	def test_acknowledgment_due(self):
		doc = frappe.get_doc(
			{
				"doctype": "TCD Governance Document",
				"title": "Read me",
				"code": "POL-N2",
				"document_owner": self.author,
				"approver": "Administrator",
				"audience_roles": [{"role": "TCD Learner"}],
			}
		).insert()
		for status in ("Review", "Approval", "Active"):
			api.set_governance_status(doc.name, status)
		self.assertTrue(logs(self.learner, "Read me"))
		self.assertFalse(logs(self.author, "Read me (version 1)"))  # author is not in the audience

	# ------------------------------------------------------------ analytics

	def test_reports(self):
		course = make_course(self.space, "Report course", [[self.l1]], instructors=[self.vip])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		api.content_feedback(self.l1.name, 1)
		frappe.set_user(self.vip)
		api.enroll("Course", course.name)
		frappe.db.set_value(
			"TCD Enrollment", enrollment(self.vip, course.name).name, "due_date", "2000-01-01"
		)

		frappe.set_user("Administrator")
		row = next(r for r in analytics.course_rows({}) if r["course"] == course.name)
		self.assertEqual(
			(row["enrolled"], row["completed"], row["completion_rate"], row["overdue"]), (2, 1, 50, 1)
		)
		self.assertEqual(row["avg_days_to_complete"], 0)
		usage = next(r for r in analytics.usage_rows({"space": self.space}) if r["content"] == self.l1.name)
		self.assertEqual(
			(usage["readers"], usage["completed"], usage["helpful_rate"]), (1, 1, 100)
		)  # vip never opened it

		doc = frappe.get_doc(
			{
				"doctype": "TCD Governance Document",
				"title": "Compliance doc",
				"code": "POL-N3",
				"document_owner": self.author,
				"approver": "Administrator",
				"audience_roles": [{"role": "TCD Instructor"}],
			}
		).insert()
		for status in ("Review", "Approval", "Active"):
			api.set_governance_status(doc.name, status)
		frappe.set_user(self.vip)
		api.acknowledge(doc.name)
		frappe.set_user("Administrator")
		comp = next(r for r in analytics.compliance_rows() if r["document"] == doc.name)
		self.assertEqual((comp["audience"], comp["acknowledged"], comp["compliance"]), (1, 1, 100))
		self.assertEqual(analytics.compliance_card()["fieldtype"], "Percent")
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			analytics.compliance_card()

	def test_portal_notifications(self):
		course = make_course(self.space, "Portal notify", [[self.l1]])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		status, html, _ = render("/learn/my", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-notifications", html)
