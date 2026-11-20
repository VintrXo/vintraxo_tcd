import json

import frappe
from frappe.utils import add_days, getdate, now_datetime, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import courses, studio
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course


class TestPhase20Schedule(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (*CLEAN, "TCD Course Interest", "Notification Log"):
			frappe.db.delete(dt)
		self.space = make_space("ph20-space").name
		self.open_lesson = lesson(self.space, "Week one")
		self.later = lesson(self.space, "Week two")
		self.course = make_course(
			self.space, "Drip course", [[self.open_lesson], [self.later]], publish_it=False, self_enrollment=1
		)
		second = frappe.get_all(
			"TCD Chapter", filters={"course": self.course.name}, order_by="sort_order asc", pluck="name"
		)[1]
		frappe.db.set_value("TCD Chapter", second, "release_after_days", 3)
		self.course.reload()
		self.course.status = "Published"
		self.course.save()

	def tearDown(self):
		frappe.set_user("Administrator")

	def enroll(self):
		frappe.set_user(self.learner)
		api.enroll("Course", self.course.name)

	def test_chapter_opens_days_after_enrollment(self):
		self.assertIsNone(courses.drip_lock(self.learner, self.later.name))  # not enrolled: no lock
		self.enroll()
		opens = courses.drip_lock(self.learner, self.later.name)
		self.assertEqual(opens, getdate(add_days(nowdate(), 3)))
		self.assertIsNone(courses.drip_lock(self.learner, self.open_lesson.name))

		status = courses.course_status(self.learner, self.course.name)
		item = status["chapters"][1]["items"][0]
		self.assertTrue(item["locked"])
		self.assertEqual(item["opens_on"], opens)

		lesson_data = api.get_lesson(self.later.name)
		self.assertEqual((lesson_data["blocks"], lesson_data["opens_on"]), ([], str(opens)))
		with self.assertRaises(frappe.ValidationError):
			api.complete_lesson(self.later.name)
		status_code, html, _ = render(
			f"/learn/{self.space}/{self.later.slug}?course={self.course.name}", self.learner
		)
		self.assertEqual(status_code, 200)
		self.assertIn("tcd-opens-on", html)

		# five days later the chapter is open
		name = frappe.db.get_value("TCD Enrollment", {"user": self.learner, "course": self.course.name})
		frappe.db.set_value("TCD Enrollment", name, "enrolled_on", add_days(now_datetime(), -5))
		self.assertIsNone(courses.drip_lock(self.learner, self.later.name))
		frappe.set_user(self.learner)
		api.complete_lesson(self.later.name)

	def test_fixed_opening_date(self):
		chapter = frappe.get_all(
			"TCD Chapter", filters={"course": self.course.name}, order_by="sort_order asc", pluck="name"
		)[1]
		frappe.db.set_value(
			"TCD Chapter", chapter, {"release_after_days": 0, "release_on": add_days(nowdate(), 10)}
		)
		self.enroll()
		self.assertEqual(courses.drip_lock(self.learner, self.later.name), getdate(add_days(nowdate(), 10)))
		frappe.db.set_value("TCD Chapter", chapter, "release_on", add_days(nowdate(), -1))
		self.assertIsNone(courses.drip_lock(self.learner, self.later.name))

	def test_coming_soon_and_notify_me(self):
		self.course.reload()
		self.course.coming_soon = 1
		self.course.save()
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.enroll("Course", self.course.name)
		api.course_interest(self.course.name, 1)
		api.course_interest(self.course.name, 1)  # once only
		self.assertEqual(frappe.db.count("TCD Course Interest", {"course": self.course.name}), 1)
		_code, html, _ = render(f"/learn/{self.space}/course/{self.course.slug}", self.learner)
		self.assertIn('data-on="0"', html)  # "stop notifying me"

		frappe.set_user("Administrator")
		self.course.reload()
		self.course.coming_soon = 0
		self.course.save()
		self.assertTrue(
			frappe.get_all(
				"Notification Log", filters={"for_user": self.learner, "document_name": self.course.name}
			)
		)
		self.assertEqual(
			frappe.db.get_value("TCD Course Interest", {"course": self.course.name}, "notified"), 1
		)
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.ValidationError):  # open now
			api.course_interest(self.course.name, 1)
		api.enroll("Course", self.course.name)

		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):  # only through the course page
			frappe.get_doc(
				{"doctype": "TCD Course Interest", "course": self.course.name, "user": self.vip}
			).insert()

	def test_studio_saves_release_settings(self):
		frappe.set_user(self.author)
		r = api.studio_save_course(json.dumps({"space": self.space, "title": "Studio drip"}))
		api.studio_save_course(
			json.dumps(
				{
					"name": r["name"],
					"coming_soon": 1,
					"chapters": [
						{
							"title": "A",
							"release_after_days": 7,
							"items": [{"content": self.open_lesson.name}],
						},
						{"title": "B", "release_on": str(add_days(nowdate(), 30)), "items": []},
					],
				}
			)
		)
		data = studio.course_data(r["name"])
		self.assertEqual(data["doc"]["coming_soon"], 1)
		self.assertEqual(data["chapters"][0]["release_after_days"], 7)
		self.assertEqual(data["chapters"][1]["release_on"], str(getdate(add_days(nowdate(), 30))))
