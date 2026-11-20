import frappe
from frappe.utils import add_days, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import evaluations
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


class TestPhase19Evaluations(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		cls.other = make_user("tcd-other@test.local", ["TCD Learner"])
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			*CLEAN,
			"TCD Evaluation",
			"TCD Evaluator",
			"TCD Evaluator Slot",
			"TCD Course Evaluator",
			"TCD Certificate",
			"Notification Log",
		):
			frappe.db.delete(dt)
		self.space = make_space("ph19-space").name
		frappe.get_doc(
			{
				"doctype": "TCD Evaluator",
				"user": self.vip,
				"schedule": [{"day": d, "start_time": "09:00:00", "end_time": "11:00:00"} for d in DAYS],
			}
		).insert()
		self.l1 = lesson(self.space, "Eval lesson")
		self.course = make_course(
			self.space,
			"Certified course",
			[[self.l1]],
			instructors=[self.vip],
			issue_certificate=1,
			requires_evaluation=1,
			evaluation_minutes=60,
			self_enrollment=1,
		)

	def tearDown(self):
		frappe.set_user("Administrator")

	def complete(self, user):
		frappe.set_user(user)
		api.enroll("Course", self.course.name)
		api.complete_lesson(self.l1.name)

	def test_completion_waits_for_evaluation(self):
		self.complete(self.learner)
		self.assertFalse(frappe.db.exists("TCD Certificate", {"user": self.learner}))  # no certificate yet
		st = evaluations.state(self.learner, self.course.name)
		self.assertTrue(st["completed"] and st["can_book"])
		self.assertEqual(len(st["slots"]), 14 * 2)  # 2 one-hour slots a day for two weeks
		self.assertEqual(st["slots"][0]["date"], str(frappe.utils.getdate(add_days(nowdate(), 1))))
		self.assertTrue(
			frappe.get_all(
				"Notification Log", filters={"for_user": self.learner, "document_type": "TCD Course"}
			)
		)

		status, html, _ = render(f"/learn/{self.space}/course/{self.course.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertEqual(html.count('class="btn btn-default btn-xs tcd-slot"'), 28)

	def test_holiday_and_booked_slots_are_hidden(self):
		frappe.db.set_value(
			"TCD Evaluator",
			self.vip,
			{"unavailable_from": add_days(nowdate(), 1), "unavailable_to": add_days(nowdate(), 2)},
		)
		self.complete(self.learner)
		self.assertEqual(len(evaluations.available_slots(self.course.name)), 12 * 2)
		self.complete(self.other)
		slot = evaluations.available_slots(self.course.name)[0]
		frappe.set_user(self.other)
		api.book_evaluation(self.course.name, slot["evaluator"], slot["date"], slot["start_time"])
		slots = evaluations.available_slots(self.course.name)
		self.assertNotIn((slot["date"], slot["start_time"]), [(s["date"], s["start_time"]) for s in slots])

	def test_booking_rules(self):
		frappe.set_user(self.learner)
		slot = evaluations.available_slots(self.course.name)[0]
		with self.assertRaises(frappe.ValidationError):  # course not completed yet
			api.book_evaluation(self.course.name, slot["evaluator"], slot["date"], slot["start_time"])
		self.complete(self.learner)
		with self.assertRaises(frappe.ValidationError):  # not an offered time
			api.book_evaluation(self.course.name, slot["evaluator"], slot["date"], "13:00")
		name = api.book_evaluation(self.course.name, slot["evaluator"], slot["date"], slot["start_time"])
		self.assertEqual(frappe.db.get_value("TCD Evaluation", name, "status"), "Scheduled")
		self.assertTrue(
			frappe.get_all(
				"Notification Log", filters={"for_user": self.vip, "document_type": "TCD Evaluation"}
			)
		)
		with self.assertRaises(frappe.ValidationError):  # one booking at a time
			api.book_evaluation(self.course.name, slot["evaluator"], slot["date"], "10:00")

		frappe.set_user(self.other)  # another learner cannot see or cancel it
		self.assertFalse(frappe.has_permission("TCD Evaluation", "read", name))
		self.assertEqual(frappe.get_list("TCD Evaluation", pluck="name"), [])
		with self.assertRaises(frappe.PermissionError):
			api.cancel_evaluation(name)
		frappe.set_user(self.learner)
		self.assertTrue(frappe.has_permission("TCD Evaluation", "read", name))
		self.assertFalse(frappe.has_permission("TCD Evaluation", "write", name))
		api.cancel_evaluation(name)
		self.assertEqual(frappe.db.get_value("TCD Evaluation", name, "status"), "Cancelled")

		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):  # only through booking
			frappe.get_doc(
				{
					"doctype": "TCD Evaluation",
					"course": self.course.name,
					"user": self.learner,
					"evaluator": self.vip,
					"date": nowdate(),
					"start_time": "09:00",
					"end_time": "10:00",
				}
			).insert()

	def test_result_issues_certificate(self):
		self.complete(self.learner)
		slot = evaluations.available_slots(self.course.name)[0]
		name = api.book_evaluation(self.course.name, slot["evaluator"], slot["date"], slot["start_time"])
		frappe.set_user(self.vip)
		with self.assertRaises(frappe.ValidationError):  # before the session starts
			api.record_evaluation(name, "Passed", 90, "good")
		frappe.db.set_value("TCD Evaluation", name, "date", add_days(nowdate(), -1))  # the session took place

		frappe.set_user(self.other)
		with self.assertRaises(frappe.PermissionError):
			api.record_evaluation(name, "Passed", 90)
		frappe.set_user(self.vip)
		self.assertEqual([r.name for r in evaluations.for_evaluator(self.vip)["upcoming"]], [name])
		status, html, _ = render("/learn/instructor", self.vip)
		self.assertEqual(status, 200)
		self.assertIn(f'data-name="{name}"', html)
		frappe.set_user(self.vip)
		api.record_evaluation(name, "Failed", 40, "<b>practise loops</b>")
		st = evaluations.state(self.learner, self.course.name)
		self.assertTrue(st["can_book"])  # book again after a fail
		self.assertEqual(st["last"]["status"], "Failed")
		_status, html, _ = render(f"/learn/{self.space}/course/{self.course.slug}", self.learner)
		self.assertIn("&lt;b&gt;practise loops&lt;/b&gt;", html)

		frappe.set_user(self.learner)
		slot = evaluations.available_slots(self.course.name)[0]
		second = api.book_evaluation(self.course.name, slot["evaluator"], slot["date"], slot["start_time"])
		frappe.db.set_value("TCD Evaluation", second, "date", add_days(nowdate(), -1))
		frappe.set_user(self.vip)
		res = api.record_evaluation(second, "Passed", 95, "well done")
		cert = frappe.get_doc("TCD Certificate", res["certificate"])
		self.assertEqual((cert.user, cert.course, cert.status), (self.learner, self.course.name, "Active"))
		with self.assertRaises(frappe.ValidationError):  # result is final
			api.record_evaluation(second, "Failed")
		self.assertFalse(evaluations.state(self.learner, self.course.name)["can_book"])

	def test_course_without_evaluation_issues_directly(self):
		self.course.reload()
		self.course.status = "Draft"
		self.course.save()
		self.course.requires_evaluation = 0
		self.course.status = "Published"
		self.course.save()
		self.complete(self.learner)
		self.assertTrue(
			frappe.db.exists("TCD Certificate", {"user": self.learner, "course": self.course.name})
		)
		self.assertIsNone(evaluations.state(self.learner, self.course.name))

	def test_evaluator_validation(self):
		ev = frappe.get_doc("TCD Evaluator", self.vip)
		ev.append("schedule", {"day": "Monday", "start_time": "12:00:00", "end_time": "11:00:00"})
		with self.assertRaises(frappe.ValidationError):
			ev.save()

	def test_times_are_zero_padded(self):
		self.complete(self.learner)
		slot = evaluations.available_slots(self.course.name)[0]
		name = api.book_evaluation(self.course.name, slot["evaluator"], slot["date"], slot["start_time"])
		shown = evaluations.scheduled(self.learner, self.course.name)
		self.assertEqual((shown["name"], shown["start_time"], shown["end_time"]), (name, "09:00", "10:00"))
