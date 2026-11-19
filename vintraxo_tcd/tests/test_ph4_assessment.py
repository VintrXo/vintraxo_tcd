import json

import frappe
from frappe.utils import add_to_date, now_datetime

from vintraxo_tcd import api
from vintraxo_tcd.core import assessment
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course
from vintraxo_tcd.vintraxo_tcd.report.tcd_quiz_analytics import tcd_quiz_analytics as quiz_report


def question(qtype, text="Q", category=None, **kw):
	return frappe.get_doc(
		{"doctype": "TCD Question", "question": text, "question_type": qtype, "category": category, **kw}
	).insert()


class TestPhase4Assessment(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		settings = frappe.get_single("TCD Settings")
		settings.update({"require_approval_before_publish": 1, "enable_portal": 1})
		settings.save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			"TCD Question",
			"TCD Question Category",
			"TCD Quiz Bank Item",
			"TCD Rubric Criterion",
			*CLEAN,
		):
			frappe.db.delete(dt)
		for child in ("TCD Learning Item", "TCD Course Instructor"):
			frappe.db.delete(child)
		self.space = make_space("ph4-space").name
		self.lesson = lesson(self.space, "Assessed lesson")
		frappe.get_doc({"doctype": "TCD Question Category", "category_name": "ph4-cat"}).insert()

	def tearDown(self):
		frappe.set_user("Administrator")

	def quiz(self, bank=(), **kw):
		return frappe.get_doc(
			{
				"doctype": "TCD Quiz",
				"title": "Bank quiz",
				"content": self.lesson.name,
				"pass_percentage": 60,
				"bank_items": list(bank),
				**kw,
			}
		).insert()

	# ------------------------------------------------------------ validation

	def test_question_validation(self):
		bad = [
			dict(qtype="Single Choice", options="a\nb", correct_answers="1,2"),
			dict(qtype="Ordering", options="only one"),
			dict(qtype="Matching", pairs="a => b"),
			dict(qtype="Matching", pairs="a - b\nc - d"),
			dict(qtype="Fill Blank", text="___ and ___", accepted_answers="one"),
			dict(qtype="Code", code_language="python"),  # no expected output, no manual review
			dict(qtype="Code", expected_output="1"),  # no language
			dict(qtype="Essay", points=0),
		]
		for kw in bad:
			qtype = kw.pop("qtype")
			text = kw.pop("text", "Q")
			with self.assertRaises(frappe.ValidationError, msg=(qtype, kw)):
				question(qtype, text, **kw)
		with self.assertRaises(frappe.ValidationError):
			self.quiz(bank=[{"category": "ph4-cat", "pick_count": 3}])  # empty category

	# ------------------------------------------------------------ grading by type

	def test_grading_all_types(self):
		qs = {
			"single": question("Single Choice", options="a\nb\nc", correct_answers="2", points=1),
			"fill": question(
				"Fill Blank",
				"Python ___ by ___",
				accepted_answers="was created|created\nGuido|Guido van Rossum",
				points=2,
			),
			"match": question("Matching", pairs="int => عدد صحيح\nstr => نص\nbool => منطقي", points=3),
			"order": question("Ordering", options="first\nsecond\nthird", points=3),
			"short": question("Short Answer", accepted_answers="بايثون\nPython", points=1),
			"code": question("Code", code_language="python", expected_output="SECRET-OUTPUT-42", points=2),
			"sql": question("SQL", setup_code="create table t(a)", expected_output="a\n1", points=2),
		}
		quiz = self.quiz(bank=[{"question": q.name} for q in qs.values()])
		frappe.set_user(self.learner)
		payload = api.get_quiz(quiz.name)
		dumped = json.dumps(payload, ensure_ascii=False)
		for secret in (
			"Guido",
			"SECRET-OUTPUT",
			"accepted",
			"expected_output",
			"correct_answers",
			"عدد صحيح =>",
		):
			self.assertNotIn(secret, dumped)
		by_type = {p["type"]: p for p in payload["questions"]}
		self.assertEqual(sorted(by_type["Matching"]["rights"]), sorted(["عدد صحيح", "نص", "منطقي"]))
		self.assertEqual(by_type["Fill Blank"]["blanks"], 2)
		self.assertEqual(by_type["SQL"]["setup_code"], "create table t(a)")

		answers = {
			qs["single"].name: [2],
			qs["fill"].name: ["Created", "guido van rossum"],
			qs["match"].name: {"0": "عدد صحيح", "1": "منطقي", "2": "نص"},  # 1 of 3
			qs["order"].name: [1, 3, 2],  # 1 of 3 positions
			qs["short"].name: "  بَايثون ",  # diacritics/spaces ignored
			qs["code"].name: {"code": "print('SECRET-OUTPUT-42')", "output": "SECRET-OUTPUT-42\n"},
			qs["sql"].name: {"code": "select 1 as a", "output": "a\n2"},
		}
		res = api.submit_quiz(quiz.name, answers)
		by_id = {r["id"]: r for r in res["results"]}
		self.assertTrue(by_id[qs["fill"].name]["is_correct"])
		self.assertFalse(by_id[qs["match"].name]["is_correct"])
		self.assertTrue(by_id[qs["code"].name]["is_correct"])
		self.assertFalse(by_id[qs["sql"].name]["is_correct"])
		# 1 + 2 + 1 + 1 + 1 + 2 + 0 = 8 of 14
		self.assertEqual((res["score"], res["max_score"]), (8, 14))
		self.assertFalse(res["passed"])
		self.assertFalse(res["pending_review"])

	# ------------------------------------------------------------ paper, randomization, time limit

	def test_random_paper_and_time_limit(self):
		for i in range(4):
			question("True False", f"TF {i}", category="ph4-cat", correct_answers="1")
		fixed = question("Single Choice", "Fixed", options="x\ny", correct_answers="1")
		quiz = self.quiz(
			bank=[{"question": fixed.name}, {"category": "ph4-cat", "pick_count": 2}],
			time_limit_minutes=5,
			shuffle_options=1,
		)
		frappe.set_user(self.learner)
		meta = api.get_quiz(quiz.name)
		self.assertTrue(meta["requires_start"])
		self.assertEqual(meta["questions"], [])
		with self.assertRaises(frappe.ValidationError):
			api.submit_quiz(quiz.name, {})  # must start first

		started = api.start_quiz(quiz.name)
		ids = [q["id"] for q in started["questions"]]
		self.assertEqual(len(ids), 3)
		self.assertIn(fixed.name, ids)
		self.assertGreater(started["attempt"]["seconds_left"], 250)
		self.assertEqual([q["id"] for q in api.get_quiz(quiz.name)["questions"]], ids)  # resume, same paper
		self.assertEqual([q["id"] for q in api.start_quiz(quiz.name)["questions"]], ids)

		answers = {i: [1] for i in ids}
		sub = frappe.db.get_value("TCD Quiz Submission", {"user": self.learner, "status": "In Progress"})
		frappe.db.set_value("TCD Quiz Submission", sub, "deadline", add_to_date(now_datetime(), minutes=-5))
		res = api.submit_quiz(quiz.name, answers)
		self.assertTrue(res["timed_out"])
		self.assertEqual(res["score"], 0)
		self.assertEqual(frappe.db.get_value("TCD Quiz Submission", sub, "status"), "Graded")

		api.start_quiz(quiz.name)
		res = api.submit_quiz(quiz.name, {q["id"]: [1] for q in api.get_quiz(quiz.name)["questions"]})
		self.assertTrue(res["passed"])

	# ------------------------------------------------------------ manual review

	def test_manual_review_with_rubric(self):
		course = make_course(self.space, "Graded course", [[self.lesson]], instructors=[self.vip])
		essay = question(
			"Essay",
			"Explain variables",
			points=4,
			rubric=[{"criterion": "Accuracy", "max_points": 2}, {"criterion": "Clarity", "max_points": 2}],
		)
		code = question("Code", code_language="python", expected_output="1", manual_review=1, points=2)
		auto = question("True False", correct_answers="1", points=2)
		quiz = self.quiz(bank=[{"question": q.name} for q in (essay, code, auto)])

		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		res = api.submit_quiz(
			quiz.name,
			{
				essay.name: "A variable is a name.",
				code.name: {"code": "print(1)", "output": "1"},
				auto.name: [1],
			},
		)
		self.assertTrue(res["pending_review"])
		self.assertFalse(res["passed"])
		sub = res["submission"]
		self.assertEqual(frappe.db.get_value("TCD Quiz Submission", sub, "status"), "Pending Review")
		with self.assertRaises(frappe.PermissionError):
			api.review_quiz_submission(sub, {})

		frappe.set_user(self.author)  # not an instructor, not a reviewer
		with self.assertRaises(frappe.PermissionError):
			api.review_quiz_submission(sub, {})

		frappe.set_user(self.vip)
		items = api.get_review_items(sub)
		self.assertEqual({i["id"] for i in items}, {essay.name, code.name})
		self.assertTrue(next(i for i in items if i["id"] == code.name)["auto_hint"])
		with self.assertRaises(frappe.ValidationError):
			api.review_quiz_submission(sub, {essay.name: {"rubric": {"Accuracy": 3, "Clarity": 0}}})
		partial = api.review_quiz_submission(
			sub, {essay.name: {"rubric": {"Accuracy": 2, "Clarity": 1}, "feedback": "Good"}}
		)
		self.assertEqual(partial["status"], "Pending Review")
		done = api.review_quiz_submission(sub, {code.name: {"points": 2}})
		# essay 4 * 3/4 = 3, code 2, auto 2 -> 7 / 8
		self.assertEqual((done["status"], done["score"], done["passed"]), ("Graded", 7, True))
		self.assertEqual(
			frappe.db.get_value(
				"TCD Progress", {"user": self.learner, "content": self.lesson.name}, "status"
			),
			"Completed",
		)

	# ------------------------------------------------------------ permissions and analytics

	def test_bank_hidden_from_learners_and_analytics(self):
		q = question("Single Choice", options="a\nb", correct_answers="1")
		quiz = self.quiz(bank=[{"question": q.name}])
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Question", "read"))
		self.assertFalse(frappe.has_permission("TCD Question Category", "read"))
		api.submit_quiz(quiz.name, {q.name: 2})
		api.submit_quiz(quiz.name, {q.name: [1]})

		frappe.set_user("Administrator")
		_cols, rows, _m, _c, summary = quiz_report.execute({"quiz": quiz.name})
		self.assertEqual((rows[0]["answered"], rows[0]["correct"], rows[0]["common_wrong"]), (2, 1, "b"))
		self.assertEqual({s["label"]: s["value"] for s in summary}["Attempts"], 2)

	def test_item_helpers(self):
		item = assessment.item_from_bank(question("Ordering", options="a\nb\nc", points=3))
		self.assertEqual(assessment.grade_item(item, [1, 2, 3])["earned"], 3)
		self.assertEqual(assessment.grade_item(item, "garbage")["earned"], 0)
		self.assertEqual(assessment.grade_item(item, None)["earned"], 0)
