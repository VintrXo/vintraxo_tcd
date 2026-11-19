import json
from unittest.mock import patch

import frappe
from frappe.utils import add_days, add_to_date, now_datetime

from vintraxo_tcd import api
from vintraxo_tcd.core import hr_sync, teams, transfer
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, enrollment, lesson, make_course
from vintraxo_tcd.tests.test_ph4_assessment import question


class TestPhase13(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		cls.boss = make_user("tcd-boss@test.local", ["TCD Learner"])
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			"TCD Team",
			"TCD Team Member",
			"TCD Session",
			"TCD Session Attendance",
			"TCD Certificate",
			"TCD Question",
			"TCD Quiz Bank Item",
			"TCD Content Import",
			*CLEAN,
		):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		frappe.db.delete("TCD Course Instructor")
		self.space = make_space("ph13-space").name
		self.l1 = lesson(self.space, "Team lesson")

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ attendance rule

	def test_minimum_attendance_completes_the_course(self):
		course = make_course(
			self.space, "Workshop", [[self.l1]], instructors=[self.vip], minimum_attendance=50
		)
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		self.assertEqual(enrollment(self.learner, course.name).status, "Active")  # no session held yet

		frappe.set_user(self.vip)
		start = add_to_date(now_datetime(), hours=-3)
		s = frappe.get_doc(
			{
				"doctype": "TCD Session",
				"title": "Day 1",
				"course": course.name,
				"starts_on": start,
				"ends_on": add_to_date(start, hours=2),
			}
		).insert()
		api.load_session_learners(s.name)
		s.reload()
		s.attendance[0].status = "Absent"
		s.save()
		self.assertEqual(enrollment(self.learner, course.name).status, "Active")
		s.attendance[0].status = "Late"  # late counts as attended
		s.save()
		self.assertEqual(enrollment(self.learner, course.name).status, "Completed")
		frappe.set_user(self.learner)
		data = api.get_course(course.name)
		self.assertEqual((data["attendance"], data["minimum_attendance"]), (100, 50))

	# ------------------------------------------------------------ manager dashboard

	def test_manager_sees_only_their_team(self):
		course = make_course(self.space, "Mandatory", [[self.l1]])
		frappe.get_doc(
			{
				"doctype": "TCD Team",
				"team_name": "Sales",
				"manager": self.boss,
				"members": [{"user": self.learner}],
			}
		).insert()
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "TCD Team",
					"team_name": "Bad",
					"manager": self.boss,
					"members": [{"user": self.boss}],
				}
			).insert()
		training_rule = frappe.get_doc(
			{
				"doctype": "TCD Training Rule",
				"title": "Must",
				"target_type": "Course",
				"course": course.name,
				"roles": [{"role": "TCD Learner"}],
			}
		).insert()
		from vintraxo_tcd.core import training

		training.apply_rule(training_rule.name, [self.learner, self.vip])
		frappe.db.set_value(
			"TCD Enrollment",
			enrollment(self.learner, course.name).name,
			"due_date",
			add_days(now_datetime(), -1),
		)

		frappe.set_user(self.boss)
		self.assertTrue(teams.is_manager(self.boss))
		data = api.team_overview()
		self.assertEqual([m["user"] for m in data["members"]], [self.learner])  # vip is not in the team
		row = data["members"][0]
		self.assertEqual((row["mandatory"], row["mandatory_done"], row["overdue"]), (1, 0, 1))
		self.assertEqual(data["summary"]["compliance"], 0)
		status, html, _ = render("/learn/team", self.boss)
		self.assertEqual(status, 200)
		self.assertIn("tcd-team-table", html)
		_, html, _ = render("/learn", self.boss)
		self.assertIn("/learn/team", html)

		frappe.set_user(self.vip)  # not a manager
		with self.assertRaises(frappe.PermissionError):
			api.team_overview()
		self.assertEqual(render("/learn/team", self.vip)[0], 404)
		frappe.set_user(self.boss)
		with self.assertRaises(frappe.PermissionError):
			api.team_overview("Other team")

	def test_direct_reports_from_hr(self):
		with (
			patch.object(
				teams, "direct_reports", side_effect=lambda u: {self.vip} if u == self.boss else set()
			),
		):
			frappe.set_user(self.boss)
			self.assertTrue(teams.is_manager(self.boss))
			self.assertEqual([m["user"] for m in api.team_overview("direct")["members"]], [self.vip])
		self.assertEqual(teams.direct_reports(self.boss), set())  # no HRMS on this site

	# ------------------------------------------------------------ HRMS write-back

	def test_hr_records_are_built_and_guarded(self):
		course = make_course(self.space, "HR course", [[self.l1]], summary="<b>Basics</b>")
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		with patch.object(hr_sync, "on_completed") as hook:
			api.complete_lesson(self.l1.name)
		hook.assert_called_once()
		frappe.set_user("Administrator")
		e = enrollment(self.learner, course.name)
		self.assertIsNone(hr_sync.record(e.name))  # no HRMS here: nothing happens
		employee = frappe._dict(name="EMP-0001", company="VX Co")
		event = hr_sync.event_values(e, course, employee)
		self.assertEqual(
			(event["event_status"], event["company"], event["type"]), ("Completed", "VX Co", "Theory")
		)
		self.assertGreater(event["end_time"], event["start_time"])
		self.assertEqual(event["employees"][0]["attendance"], "Present")
		self.assertNotIn("<b>", event["introduction"])  # escaped
		self.assertEqual(hr_sync.program_values(course, "VX Co")["training_program"], "TCD: HR course")

		created = []
		with (
			patch.object(hr_sync, "available", return_value=True),
			patch.object(hr_sync, "employee_profile", return_value=employee),
			patch.object(
				hr_sync,
				"_insert",
				side_effect=lambda v, submit=False: created.append((v["doctype"], submit))
				or frappe._dict(name="EV-1"),
			),
			patch("frappe.db.exists", return_value=False),
		):
			self.assertEqual(hr_sync.record(e.name), "EV-1")
		self.assertEqual(
			created, [("Training Program", False), ("Training Event", True), ("Training Result", True)]
		)
		self.assertEqual(frappe.db.get_value("TCD Enrollment", e.name, "hr_training_event"), "EV-1")
		with patch.object(hr_sync, "available", return_value=True):
			self.assertIsNone(hr_sync.record(e.name))  # already recorded: never twice

	# ------------------------------------------------------------ export / import

	def test_export_import_space(self):
		l2 = lesson(self.space, "Second lesson")
		course = make_course(self.space, "Exported course", [[self.l1, l2]])
		q = question("True False", correct_answers="1")
		frappe.get_doc(
			{
				"doctype": "TCD Quiz",
				"title": "Exported quiz",
				"content": self.l1.name,
				"pass_percentage": 50,
				"bank_items": [{"question": q.name}],
			}
		).insert()

		frappe.set_user(self.author)
		with self.assertRaises(frappe.PermissionError):
			transfer.export_space(self.space)
		frappe.set_user("Administrator")
		bundle = transfer.export_space(self.space)
		self.assertEqual(len(bundle["contents"]), 2)
		self.assertNotIn("search_text", bundle["contents"][0])
		raw = json.dumps(bundle, default=str).encode()

		with self.assertRaises(frappe.ValidationError):
			transfer.parse_bundle(b'{"format": "something-else"}')
		with self.assertRaises(frappe.ValidationError):
			transfer.import_bundle(transfer.parse_bundle(raw))  # same space name exists
		result = transfer.import_bundle(transfer.parse_bundle(raw), "ph13-copy")
		self.assertEqual(result["created"]["TCD Content"], 2)

		copied_course = frappe.get_doc("TCD Course", {"space": "ph13-copy"})
		self.assertNotEqual(copied_course.name, course.name)
		self.assertEqual(copied_course.status, "Published")
		chapter = frappe.get_doc("TCD Chapter", {"course": copied_course.name})
		new_pages = set(frappe.get_all("TCD Content", filters={"space": "ph13-copy"}, pluck="name"))
		self.assertTrue({i.content for i in chapter.items} <= new_pages)  # links rewritten
		quiz = frappe.get_doc("TCD Quiz", {"space": "ph13-copy"})
		self.assertIn(quiz.content, new_pages)
		self.assertNotEqual(quiz.bank_items[0].question, q.name)
		page = frappe.get_doc("TCD Content", {"space": "ph13-copy", "title": "Team lesson"})
		self.assertTrue(page.current_version and page.next_review_date)  # snapshot + review date

		frappe.set_user(self.learner)
		status, _, _ = render(f"/learn/ph13-copy/{page.slug}", self.learner)
		self.assertEqual(status, 200)
