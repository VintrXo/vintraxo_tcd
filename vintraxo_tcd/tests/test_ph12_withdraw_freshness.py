import frappe
from frappe.utils import add_days, add_months, getdate, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import freshness, training
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, enrollment, lesson, make_course


class TestPhase12WithdrawFreshness(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update({"enable_portal": 1, "default_review_months": 12}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Training Rule", "TCD Rule Role", *CLEAN):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		frappe.db.delete("ToDo", {"reference_type": "TCD Content"})
		self.space = make_space("ph12-space").name
		self.l1 = lesson(self.space, "Fresh lesson")

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ withdraw

	def test_withdraw_and_reenroll(self):
		course = make_course(self.space, "Optional course", [[self.l1]])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		_status, html, _ = render(f"/learn/{self.space}/course/{course.slug}", self.learner)
		self.assertIn("tcd-withdraw", html)
		self.assertEqual(api.withdraw("Course", course.name)["status"], "Withdrawn")
		self.assertIsNone(api.get_course(course.name)["enrollment"])  # page offers Enroll again
		_, html, _ = render(f"/learn/{self.space}/course/{course.slug}", self.learner)
		self.assertIn("tcd-enroll", html)
		with self.assertRaises(frappe.DoesNotExistError):
			api.withdraw("Course", course.name)
		api.enroll("Course", course.name)
		self.assertEqual(enrollment(self.learner, course.name).status, "Active")

	def test_cannot_withdraw_mandatory_or_completed(self):
		course = make_course(self.space, "Mandatory course", [[self.l1]])
		rule = frappe.get_doc(
			{
				"doctype": "TCD Training Rule",
				"title": "Must",
				"target_type": "Course",
				"course": course.name,
				"roles": [{"role": "TCD Learner"}],
			}
		).insert()
		training.apply_rule(rule.name, [self.learner])
		frappe.set_user(self.learner)
		_, html, _ = render(f"/learn/{self.space}/course/{course.slug}", self.learner)
		self.assertNotIn("tcd-withdraw", html)
		with self.assertRaises(frappe.PermissionError):
			api.withdraw("Course", course.name)

		other = make_course(self.space, "Done course", [[self.l1]])
		frappe.set_user(self.vip)
		api.enroll("Course", other.name)
		api.complete_lesson(self.l1.name)
		with self.assertRaises(frappe.ValidationError):
			api.withdraw("Course", other.name)

	# ------------------------------------------------------------ freshness

	def test_review_cycle(self):
		page = frappe.get_doc("TCD Content", self.l1.name)
		self.assertEqual(page.content_owner, "Administrator")
		self.assertEqual(getdate(page.last_reviewed_on), getdate(nowdate()))
		self.assertEqual(getdate(page.next_review_date), getdate(add_months(nowdate(), 12)))

		page.review_cycle_months = 3
		page.save()
		self.assertEqual(getdate(page.next_review_date), getdate(add_months(nowdate(), 3)))
		page.skip_review = 1
		page.save()
		self.assertIsNone(page.next_review_date)

	def test_overdue_notice_reminder_and_confirm(self):
		frappe.db.set_value(
			"TCD Content",
			self.l1.name,
			{"next_review_date": add_days(nowdate(), -2), "content_owner": self.author},
		)
		status, html, _ = render(f"/learn/{self.space}/{self.l1.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-outdated", html)

		frappe.set_user("Administrator")
		freshness.daily()
		freshness.daily()  # one reminder per page and date
		todos = frappe.get_all("ToDo", filters={"reference_name": self.l1.name}, pluck="allocated_to")
		self.assertEqual(todos, [self.author])
		row = next(r for r in freshness.rows({"only_overdue": 1}) if r["name"] == self.l1.name)
		self.assertEqual(row["days_overdue"], 2)

		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.confirm_content_review(self.l1.name)
		frappe.set_user(self.author)
		api.confirm_content_review(self.l1.name)
		self.assertEqual(
			getdate(frappe.db.get_value("TCD Content", self.l1.name, "next_review_date")),
			getdate(add_months(nowdate(), 12)),
		)
		_, html, _ = render(f"/learn/{self.space}/{self.l1.slug}", self.learner)
		self.assertNotIn("tcd-outdated", html)
