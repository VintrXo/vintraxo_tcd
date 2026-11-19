import frappe
from frappe.utils import add_days, add_to_date, now_datetime

from vintraxo_tcd import api
from vintraxo_tcd.core import sessions
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course
from vintraxo_tcd.vintraxo_tcd.report.tcd_attendance import tcd_attendance as report


class TestPhase12Sessions(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		cls.other = make_user("tcd-instructor2@test.local", ["TCD Instructor"])
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Session", "TCD Session Attendance", "TCD Batch", "TCD Batch Member", *CLEAN):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		frappe.db.delete("TCD Course Instructor")
		frappe.db.delete("Notification Log", {"document_type": "TCD Session"})
		self.space = make_space("ph12s-space").name
		self.l1 = lesson(self.space, "Session lesson")
		self.course = make_course(self.space, "Classroom course", [[self.l1]], instructors=[self.vip])
		for user in (self.learner, self.reviewer):
			frappe.set_user(user)
			api.enroll("Course", self.course.name)
		frappe.set_user("Administrator")

	def tearDown(self):
		frappe.set_user("Administrator")

	def session(self, user=None, start_in_hours=24, **kw):
		frappe.set_user(user or self.vip)
		start = add_to_date(now_datetime(), hours=start_in_hours)
		doc = frappe.get_doc(
			{
				"doctype": "TCD Session",
				"title": kw.pop("title", "Kick-off"),
				"course": self.course.name,
				"starts_on": start,
				"ends_on": add_to_date(start, hours=2),
				**kw,
			}
		).insert()
		frappe.set_user("Administrator")
		return doc

	# ------------------------------------------------------------ permissions and validation

	def test_permissions(self):
		s = self.session(session_type="Online", meeting_url="https://meet.example.com/x")
		self.assertEqual(s.instructor, self.vip)
		frappe.set_user(self.other)  # an instructor of another course
		self.assertEqual(frappe.get_list("TCD Session"), [])
		self.assertFalse(frappe.has_permission("TCD Session", "write", s.name))
		with self.assertRaises(frappe.PermissionError):
			self.session(user=self.other, title="Not mine")
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Session", "read", s.name))
		with self.assertRaises(frappe.PermissionError):
			api.load_session_learners(s.name)

	def test_validation(self):
		with self.assertRaises(frappe.ValidationError):
			self.session(start_in_hours=2, ends_on=add_to_date(now_datetime(), hours=1))
		with self.assertRaises(frappe.ValidationError):
			self.session(session_type="Online", meeting_url="javascript:alert(1)")
		future = self.session()
		frappe.set_user(self.vip)
		future.append("attendance", {"user": self.learner, "status": "Present"})
		with self.assertRaises(frappe.ValidationError):
			future.save()  # not started yet
		future.reload()
		future.append("attendance", {"user": self.author})  # not enrolled
		with self.assertRaises(frappe.ValidationError):
			future.save()

	# ------------------------------------------------------------ invitations, attendance, notifications

	def test_batch_invitation_and_attendance(self):
		batch = frappe.get_doc(
			{"doctype": "TCD Batch", "group_name": "Morning group", "members": [{"user": self.learner}]}
		).insert()
		s = self.session(batch=batch.name, start_in_hours=-1)  # started an hour ago
		self.assertEqual(sessions.invited(s), [self.learner])  # reviewer is enrolled but not in the batch
		notes = frappe.get_all(
			"Notification Log",
			filters={"document_type": "TCD Session"},
			pluck="for_user",
			ignore_permissions=True,
		)
		self.assertEqual(notes, [self.learner])

		frappe.set_user(self.vip)
		self.assertEqual(api.load_session_learners(s.name), 1)
		self.assertEqual(api.load_session_learners(s.name), 0)  # existing rows are kept
		s.reload()
		s.attendance[0].status = "Late"
		s.save()

		frappe.set_user(self.learner)
		mine = api.course_sessions(self.course.name)
		self.assertEqual([r["attendance"] for r in mine["upcoming"] + mine["past"]], ["Late"])
		frappe.set_user(self.reviewer)
		self.assertEqual(api.course_sessions(self.course.name), {"upcoming": [], "past": []})

	def test_learner_views_and_report(self):
		online = self.session(
			session_type="Online", meeting_url="https://meet.example.com/x", title="Online one"
		)
		past = self.session(start_in_hours=-48, title="Past one")
		frappe.set_user(self.vip)
		api.load_session_learners(past.name)
		past.reload()
		for row in past.attendance:
			row.status = "Present" if row.user == self.learner else "Absent"
		past.status = "Completed"
		past.save()
		cancelled = self.session(title="Dropped")
		frappe.set_user(self.vip)
		cancelled.status = "Cancelled"
		cancelled.save()

		frappe.set_user(self.learner)
		upcoming = sessions.upcoming_for(self.learner)
		self.assertEqual([s["title"] for s in upcoming], ["Online one"])
		self.assertEqual(upcoming[0]["meeting_url"], "https://meet.example.com/x")
		_status, html, _ = render(f"/learn/{self.space}/course/{self.course.slug}", self.learner)
		self.assertIn("tcd-sessions", html)
		self.assertIn("meet.example.com", html)
		self.assertNotIn("Dropped", html)
		_, html, _ = render("/learn/my", self.learner)
		self.assertIn("Online one", html)
		_, html, _ = render(f"/learn/{self.space}/course/{self.course.slug}", self.author)  # not enrolled
		self.assertNotIn("meet.example.com", html)

		frappe.set_user(self.vip)
		_c, rows, _m, _ch, summary = report.execute({"course": self.course.name})
		by_user = {r["user"]: r for r in rows}
		self.assertEqual((by_user[self.learner]["held"], by_user[self.learner]["attendance"]), (1, 100))
		self.assertEqual(by_user[self.reviewer]["Absent"], 1)
		self.assertEqual({s["label"]: s["value"] for s in summary}["Attendance"], 50)
		frappe.set_user(self.other)
		self.assertEqual(report.execute({})[1], [])  # another instructor sees nothing
		self.assertTrue(online.name)

	def test_cancel_and_move_notify(self):
		s = self.session()
		frappe.db.delete("Notification Log", {"document_type": "TCD Session"})
		frappe.set_user(self.vip)
		s.starts_on = add_days(s.starts_on, 1)
		s.ends_on = add_days(s.ends_on, 1)
		s.save()
		s.status = "Cancelled"
		s.save()
		subjects = frappe.get_all(
			"Notification Log",
			filters={"document_type": "TCD Session", "for_user": self.learner},
			pluck="subject",
			ignore_permissions=True,
		)
		self.assertEqual(len(subjects), 2)
