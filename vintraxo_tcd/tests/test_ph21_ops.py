import frappe

from vintraxo_tcd.core import ops
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course


class TestPhase21Ops(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (*CLEAN, "TCD Evaluator", "TCD Evaluator Slot", "TCD Course Evaluator"):
			frappe.db.delete(dt)
		self.space = make_space("ph21-space").name

	def tearDown(self):
		frappe.set_user("Administrator")

	def messages(self, status=None):
		return [i["message"] for i in ops.readiness() if status is None or i["status"] == status]

	def test_report_shape_and_admin_only(self):
		items = ops.readiness()
		self.assertTrue(items)
		self.assertTrue(all(i["status"] in ("ok", "warn", "fail") for i in items))
		self.assertEqual(sum(ops.summary(items).values()), len(items))
		self.assertTrue(ops.readiness_report()["items"])
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			ops.readiness_report()

	def test_course_problems_are_reported(self):
		make_course(
			self.space,
			"Needs evaluator",
			[[lesson(self.space, "Ops lesson")]],
			issue_certificate=1,
			requires_evaluation=1,
		)
		self.assertTrue(any("Needs evaluator" in m for m in self.messages("fail")))

	def test_paid_course_without_gateway(self):
		settings = frappe.get_single("TCD Settings")
		settings.payment_gateway = None
		settings.save()
		make_course(self.space, "Paid", [[lesson(self.space, "Paid lesson")]], paid=1, price=100)
		self.assertTrue(any("payment gateway" in m for m in self.messages("fail")))
