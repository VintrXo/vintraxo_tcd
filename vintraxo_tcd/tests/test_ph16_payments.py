from unittest.mock import MagicMock, patch

import frappe
from frappe.utils import add_days, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import payments
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, enrollment, lesson, make_course


class TestPhase16Payments(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		if not frappe.db.exists("Currency", "USD"):
			frappe.get_doc({"doctype": "Currency", "currency_name": "USD", "enabled": 1}).insert()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Payment", "TCD Coupon", "TCD Coupon Item", *CLEAN):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		frappe.get_single("TCD Settings").update({"enable_portal": 1, "payment_gateway": "Stripe"}).save()
		self.space = make_space("ph16p-space").name
		self.course = make_course(
			self.space,
			"Paid course",
			[[lesson(self.space, "Paid lesson")]],
			paid=1,
			price=100,
			currency="USD",
		)

	def tearDown(self):
		frappe.set_user("Administrator")
		frappe.get_single("TCD Settings").update({"payment_gateway": None}).save()

	def coupon(self, code, **kw):
		return frappe.get_doc(
			{"doctype": "TCD Coupon", "code": code, "discount_type": "Percentage", "discount_value": 20, **kw}
		).insert()

	def test_paid_course_needs_checkout(self):
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.enroll("Course", self.course.name)
		_, html, _ = render(f"/learn/{self.space}/course/{self.course.slug}", self.learner)
		self.assertIn("tcd-buy-btn", html)
		with patch.object(payments, "payments_available", return_value=False):
			with self.assertRaises(frappe.ValidationError):
				api.checkout("Course", self.course.name)  # no Payments app: clear message
		self.assertEqual(frappe.db.count("TCD Payment"), 0)  # nothing written

	def test_checkout_coupon_and_gateway_callback(self):
		frappe.set_user("Administrator")
		self.coupon("save20", max_uses=1)
		self.assertTrue(frappe.db.exists("TCD Coupon", "SAVE20"))  # upper-cased
		controller = MagicMock()
		controller.get_payment_url.return_value = "https://pay.example.com/checkout/1"
		frappe.set_user(self.learner)
		self.assertEqual(api.price_quote("Course", self.course.name, "save20")["total"], 80)
		with (
			patch.object(payments, "payments_available", return_value=True),
			patch.object(payments, "_controller", return_value=controller),
		):
			r = api.checkout(
				"Course", self.course.name, coupon="save20", redirect_to="https://evil.example.com"
			)
		self.assertEqual(r["url"], "https://pay.example.com/checkout/1")
		kwargs = controller.get_payment_url.call_args.kwargs
		self.assertEqual(
			(kwargs["amount"], kwargs["reference_doctype"], kwargs["currency"]), (80, "TCD Payment", "USD")
		)
		self.assertEqual(kwargs["redirect_to"], "/learn/my")  # outside redirects are refused
		self.assertIsNone(enrollment(self.learner, self.course.name))  # not before payment

		frappe.set_user("Administrator")
		pay = frappe.get_doc("TCD Payment", r["payment"])
		pay.run_method("on_payment_authorized", "Completed")
		pay.run_method("on_payment_authorized", "Completed")  # gateways may call twice
		self.assertEqual(frappe.db.get_value("TCD Payment", pay.name, "status"), "Paid")
		self.assertEqual(enrollment(self.learner, self.course.name).status, "Active")
		self.assertEqual(frappe.db.get_value("TCD Coupon", "SAVE20", "used"), 1)
		frappe.set_user(self.vip)
		with self.assertRaises(frappe.ValidationError):
			api.price_quote("Course", self.course.name, "save20")  # used up

	def test_free_with_full_coupon_and_rules(self):
		frappe.set_user("Administrator")
		self.coupon("FREE", discount_value=100)
		self.coupon("OLD", valid_until=add_days(nowdate(), -1))
		other = make_course(
			self.space, "Other paid", [[lesson(self.space, "Other lesson")]], paid=1, price=50, currency="USD"
		)
		self.coupon("ONLYOTHER", items=[{"course": other.name}])
		with self.assertRaises(frappe.ValidationError):
			self.coupon("BAD", discount_value=150)
		frappe.set_user(self.learner)
		for bad in ("OLD", "ONLYOTHER", "NOPE"):
			with self.assertRaises(frappe.ValidationError):
				api.price_quote("Course", self.course.name, bad)
		with patch.object(payments, "payments_available", return_value=False):
			r = api.checkout("Course", self.course.name, coupon="FREE")  # nothing to pay: no gateway needed
		self.assertTrue(r["enrolled"])
		self.assertEqual(frappe.db.get_value("TCD Payment", {"user": self.learner}, "status"), "Free")
		self.assertEqual(enrollment(self.learner, self.course.name).status, "Active")
		self.assertTrue(
			api.checkout("Course", self.course.name)["enrolled"]
		)  # already enrolled: no second charge

		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({"doctype": "TCD Payment", "user": self.vip, "status": "Paid"}).insert()
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Payment", "read"))
