import json

import frappe
from frappe.utils import add_days, getdate, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import batches, teams
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course


class TestPhase23Batches(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		cls.other = make_user("tcd-other@test.local", ["TCD Learner"])
		cls.mentor = make_user("tcd-mentor@test.local", ["TCD Learner"])
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			*CLEAN,
			"TCD Session",
			"TCD Batch Member",
			"TCD Batch Mentor",
			"TCD Batch Timetable Row",
			"TCD Batch Feedback",
			"TCD Team",
			"TCD Team Member",
		):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Batch")
		self.space = make_space("ph23-space").name
		self.course = make_course(self.space, "Batch course", [[lesson(self.space, "Batch lesson")]])
		self.batch = frappe.get_doc(
			{
				"doctype": "TCD Batch",
				"group_name": "Cohort A",
				"members": [{"user": self.learner}, {"user": self.other}],
				"mentors": [{"user": self.mentor}],
			}
		).insert()
		self.second = frappe.get_doc(
			{"doctype": "TCD Batch", "group_name": "Cohort B", "members": [{"user": self.vip}]}
		).insert()

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_mentor_follows_batch(self):
		self.assertTrue(teams.is_manager(self.mentor))
		self.assertEqual(teams.members(self.mentor), sorted([self.learner, self.other]))
		self.assertEqual(teams.members(self.mentor, "batch:Cohort A"), sorted([self.learner, self.other]))
		with self.assertRaises(frappe.PermissionError):
			teams.members(self.mentor, "batch:Cohort B")
		self.assertFalse(teams.is_manager(self.other))
		status, html, _ = render("/learn/team?team=batch:Cohort A", self.mentor)
		self.assertEqual(status, 200)
		self.assertIn("tcd-batch-feedback", html)
		self.assertEqual(render("/learn/team", self.other)[0], 404)

	def test_feedback(self):
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.ValidationError):
			api.batch_feedback(
				"Cohort A", json.dumps({"content_rating": 6, "instructor_rating": 4, "overall_rating": 4})
			)
		api.batch_feedback(
			"Cohort A",
			json.dumps(
				{"content_rating": 5, "instructor_rating": 4, "overall_rating": 4, "comment": "<b>good</b>"}
			),
		)
		api.batch_feedback(
			"Cohort A", json.dumps({"content_rating": 3, "instructor_rating": 4, "overall_rating": 4})
		)  # update
		self.assertEqual(frappe.db.count("TCD Batch Feedback", {"batch": "Cohort A"}), 1)
		frappe.set_user(self.other)
		api.batch_feedback(
			"Cohort A", json.dumps({"content_rating": 5, "instructor_rating": 2, "overall_rating": 5})
		)
		with self.assertRaises(frappe.PermissionError):  # not a member
			api.batch_feedback(
				"Cohort B", json.dumps({"content_rating": 5, "instructor_rating": 5, "overall_rating": 5})
			)
		summary = batches.feedback_summary("Cohort A")
		self.assertEqual(
			(summary["responses"], summary["content_rating"], summary["instructor_rating"]), (2, 4.0, 3.0)
		)
		status, html, _ = render("/learn/my", self.learner)
		self.assertEqual(status, 200)
		self.assertIn('data-batch="Cohort A"', html)
		_status, html, _ = render("/learn/team?team=batch:Cohort A", self.mentor)
		self.assertNotIn("<b>good</b>", html)
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({"doctype": "TCD Batch Feedback", "batch": "Cohort A", "user": self.vip}).insert()

	def test_timetable_generates_sessions(self):
		start = getdate(add_days(nowdate(), 1))
		self.batch.update(
			{
				"course": self.course.name,
				"start_date": start,
				"end_date": add_days(start, 13),
				"timetable": [
					{
						"day": start.strftime("%A"),
						"start_time": "10:00:00",
						"end_time": "12:00:00",
						"location": "Room 1",
					},
					{
						"day": getdate(add_days(start, 2)).strftime("%A"),
						"start_time": "18:00:00",
						"end_time": "19:00:00",
						"session_type": "Online",
					},
				],
			}
		)
		self.batch.save()
		r = api.generate_batch_sessions("Cohort A")
		self.assertEqual(r, {"created": 4, "skipped": 0})  # two rows x two weeks
		sessions = frappe.get_all(
			"TCD Session", filters={"batch": "Cohort A"}, fields=["title", "location", "session_type"]
		)
		self.assertEqual({s.title for s in sessions}, {"Batch course"})
		self.assertEqual(api.generate_batch_sessions("Cohort A"), {"created": 0, "skipped": 4})
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.generate_batch_sessions("Cohort A")
		frappe.set_user("Administrator")
		self.batch.reload()
		self.batch.timetable[0].end_time = "09:00:00"
		with self.assertRaises(frappe.ValidationError):
			self.batch.save()
