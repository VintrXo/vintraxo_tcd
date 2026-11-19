import base64
import json
from unittest.mock import MagicMock, patch

import frappe
import requests

from vintraxo_tcd import api
from vintraxo_tcd.core import badges
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course
from vintraxo_tcd.tests.test_ph4_assessment import question

POST = "vintraxo_tcd.core.runner.requests.post"


def judge0_by_stdin(table):
	"""Fake runner: answer depends on the stdin it receives."""

	def fake(url, json=None, **kw):
		stdin = base64.b64decode(json["stdin"]).decode()
		r = MagicMock()
		r.status_code = 201
		r.json.return_value = {
			"stdout": base64.b64encode(table.get(stdin, "").encode()).decode(),
			"status": {"id": 3},
			"time": "0.01",
			"memory": 1,
		}
		return r

	return fake


class TestPhase15(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			"TCD Question",
			"TCD Question Test Case",
			"TCD Quiz Bank Item",
			"TCD Quiz Violation",
			"TCD Code Run",
			"TCD Badge",
			"TCD Badge Award",
			"TCD Certificate",
			*CLEAN,
		):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		self.space = make_space("ph15-space").name
		self.l1 = lesson(self.space, "Assessed lesson")
		self.course = make_course(self.space, "Assessed course", [[self.l1]])
		frappe.set_user(self.learner)
		api.enroll("Course", self.course.name)
		frappe.set_user("Administrator")

	def tearDown(self):
		frappe.set_user("Administrator")
		s = frappe.get_single("TCD Settings")
		s.runner_enabled = 0
		s.save()

	def quiz(self, bank, **kw):
		return frappe.get_doc(
			{
				"doctype": "TCD Quiz",
				"title": "Q",
				"content": self.l1.name,
				"pass_percentage": 50,
				"max_attempts": 0,
				"bank_items": [{"question": q.name} for q in bank],
				**kw,
			}
		).insert()

	# ------------------------------------------------------------ negative marking

	def test_negative_marking(self):
		qs = [question("True False", f"Q{i}", correct_answers="1", points=4) for i in range(3)]
		quiz = self.quiz(qs, negative_marking=1, negative_mark_percent=50)
		frappe.set_user(self.learner)
		self.assertTrue(api.get_quiz(quiz.name)["negative_marking"])
		res = api.submit_quiz(
			quiz.name, {qs[0].name: [1], qs[1].name: [2], qs[2].name: []}
		)  # right, wrong, blank
		self.assertEqual((res["score"], res["max_score"]), (2, 12))  # 4 - 2 + 0
		res = api.submit_quiz(quiz.name, {q.name: [2] for q in qs})
		self.assertEqual(res["score"], 0)  # never below zero

	# ------------------------------------------------------------ test cases

	def test_test_cases_graded_on_runner(self):
		with self.assertRaises(frappe.ValidationError):  # runner off: test cases cannot run
			question(
				"Code", code_language="python", points=3, test_cases=[{"input": "1", "expected_output": "2"}]
			)
		frappe.get_single("TCD Settings").update(
			{"runner_enabled": 1, "runner_url": "http://10.0.0.5:2358", "runner_languages": []}
		).save()
		frappe.clear_document_cache("TCD Settings", "TCD Settings")
		q = question(
			"Code",
			code_language="python",
			points=3,
			test_cases=[
				{"input": "1", "expected_output": "2"},
				{"input": "5", "expected_output": "6", "hidden": 1},
				{"input": "9", "expected_output": "10", "hidden": 1},
			],
		)
		quiz = self.quiz([q])
		frappe.set_user(self.learner)
		paper = api.get_quiz(quiz.name)["questions"][0]
		self.assertEqual(
			paper["examples"], [{"input": "1", "expected_output": "2"}]
		)  # hidden cases stay on the server
		dumped = json.dumps(paper)
		for hidden in ('"input": "5"', '"expected_output": "6"', '"input": "9"', '"expected_output": "10"'):
			self.assertNotIn(hidden, dumped)  # exact values: random ids may contain the digits
		with patch(POST, side_effect=judge0_by_stdin({"1": "2", "5": "6", "9": "0"})):
			res = api.submit_quiz(
				quiz.name, {q.name: {"code": "print(int(input())+1)", "server_cases": [True, True, True]}}
			)
		self.assertEqual(res["score"], 2)  # 2 of 3 cases; the forged server_cases was ignored
		self.assertEqual(res["results"][0]["cases"], {"passed": 2, "total": 3})
		with patch(POST, side_effect=requests.ConnectionError("down")):
			self.assertTrue(api.submit_quiz(quiz.name, {q.name: {"code": "x"}})["pending_review"])

	# ------------------------------------------------------------ proctoring

	def test_proctoring(self):
		q = question("True False", "P", correct_answers="1", points=1)
		quiz = self.quiz([q], enable_proctoring=1, max_violations=2)
		frappe.set_user(self.learner)
		self.assertTrue(api.get_quiz(quiz.name)["requires_start"])  # proctored quizzes start an attempt
		self.assertEqual(api.report_quiz_violation(quiz.name, "tab")["violations"], 0)  # no attempt yet
		api.start_quiz(quiz.name)
		self.assertFalse(api.report_quiz_violation(quiz.name, "tab")["auto_submit"])
		r = api.report_quiz_violation(quiz.name, "paste")
		self.assertEqual((r["violations"], r["auto_submit"]), (2, True))
		self.assertEqual(
			api.report_quiz_violation(quiz.name, "hack")["violations"], 0
		)  # unknown kind ignored
		res = api.submit_quiz(quiz.name, {q.name: [1]})
		frappe.set_user("Administrator")
		sub = frappe.get_doc("TCD Quiz Submission", res["submission"])
		self.assertEqual((sub.violations, sub.flagged), (2, 1))
		self.assertEqual(
			sorted(frappe.get_all("TCD Quiz Violation", filters={"submission": sub.name}, pluck="kind")),
			["Left the Tab", "Pasted Text"],
		)
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Quiz Violation", "read"))

	# ------------------------------------------------------------ badges

	def test_badges(self):
		for name, event, extra in (
			("First Step", "Lessons Completed", {"threshold": 1}),
			("Graduate", "Course Completed", {"course": self.course.name}),
			(
				"Other Course",
				"Course Completed",
				{"course": make_course(self.space, "Other", [[lesson(self.space, "Other lesson")]]).name},
			),
			("Two Lessons", "Lessons Completed", {"threshold": 2}),
			("Off", "Lessons Completed", {"enabled": 0}),
		):
			frappe.get_doc({"doctype": "TCD Badge", "badge_name": name, "event": event, **extra}).insert()
		frappe.set_user(self.learner)
		api.complete_lesson(self.l1.name)
		frappe.set_user("Administrator")
		got = set(frappe.get_all("TCD Badge Award", filters={"user": self.learner}, pluck="badge"))
		self.assertEqual(got, {"First Step", "Graduate"})
		badges.check(self.learner, "Lessons Completed")  # idempotent
		self.assertEqual(frappe.db.count("TCD Badge Award", {"user": self.learner}), 2)
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc({"doctype": "TCD Badge Award", "user": self.learner, "badge": "Graduate"}).insert()
		self.assertTrue(
			frappe.get_all(
				"Notification Log", filters={"for_user": self.learner, "document_type": "TCD Badge Award"}
			)
		)
		_, html, _ = render("/learn/my", self.learner)
		self.assertIn("tcd-badges", html)
		self.assertIn("Graduate", html)
