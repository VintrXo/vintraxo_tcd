import json

import frappe
from frappe.tests import IntegrationTestCase

from vintraxo_tcd import api
from vintraxo_tcd.core.search import snippet, tokenize
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user, publish
from vintraxo_tcd.tests.test_p2 import make_quiz
from vintraxo_tcd.vintraxo_tcd.report.tcd_learner_progress import tcd_learner_progress as progress_report
from vintraxo_tcd.vintraxo_tcd.report.tcd_quiz_analytics import tcd_quiz_analytics as quiz_report


def para(text):
	return json.dumps([{"type": "paragraph", "text": text}], ensure_ascii=False)


class TestP4(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		settings = frappe.get_single("TCD Settings")
		settings.require_approval_before_publish = 1
		settings.save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			"TCD Quiz Submission",
			"TCD Quiz",
			"TCD Progress",
			"TCD Tutorial Lesson",
			"TCD Content Version",
			"TCD Content",
		):
			frappe.db.delete(dt)
		self.space = make_space("p4-public").name

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ search

	def test_tokenize(self):
		self.assertEqual(tokenize("  المُتغيرات في  بايثون بايثون x "), ["المتغيرات", "في", "بايثون"])
		self.assertEqual(tokenize("a"), [])

	def test_ranking_title_beats_body(self):
		body = make_content(self.space, "مقدمة عامة", blocks=para("هنا نشرح الدوال في بايثون"))
		title = make_content(self.space, "الدوال في بايثون", blocks=para("شرح"))
		partial = make_content(self.space, "الدوال المتقدمة", blocks=para("بايثون"))
		results = api.search_content("الدوال بايثون")
		self.assertEqual([r.name for r in results], [title.name, partial.name, body.name])
		self.assertTrue(all(r.score > 0 for r in results))

	def test_all_terms_required_and_wildcards_escaped(self):
		make_content(self.space, "بايثون", blocks=para("100% مجاني"))
		make_content(self.space, "جافا", blocks=para("مجاني"))
		self.assertEqual(len(api.search_content("بايثون مجاني")), 1)
		self.assertEqual(len(api.search_content("مجاني")), 2)
		self.assertEqual(len(api.search_content("0%")), 1)
		self.assertEqual(api.search_content("_%"), [])

	def test_search_respects_permissions(self):
		make_content(self.space, "سر داخلي", visibility="Public")  # draft
		publish(make_content(self.space, "سر منشور", visibility="Public"))
		frappe.set_user(self.learner)
		self.assertEqual([r.title for r in api.search_content("سر")], ["سر منشور"])

	def test_snippet(self):
		text = "x" * 200 + " target " + "y" * 200
		s = snippet(text, ["target"])
		self.assertIn("target", s)
		self.assertTrue(s.startswith("...") and s.endswith("..."))
		self.assertLess(len(s), 140)

	# ------------------------------------------------------------ reports

	def _lesson_with_quiz(self):
		lesson = publish(make_content(self.space, "Quiz lesson", content_type="Lesson", visibility="Public"))
		quiz = make_quiz(lesson.name)
		return lesson, quiz, {row.question_type: row.name for row in quiz.questions}

	def test_submission_stores_results_and_quiz_analytics(self):
		_lesson, quiz, q = self._lesson_with_quiz()
		frappe.set_user(self.learner)
		api.submit_quiz(quiz.name, {q["Single Choice"]: [1], q["True False"]: [1]})
		api.submit_quiz(
			quiz.name, {q["Single Choice"]: [2], q["True False"]: [1], q["Multiple Choice"]: [2, 4]}
		)
		frappe.set_user(self.vip)
		api.submit_quiz(quiz.name, {q["Single Choice"]: [1]})

		frappe.set_user("Administrator")
		sub = frappe.get_all(
			"TCD Quiz Submission", filters={"user": self.learner, "attempt": 1}, pluck="results"
		)[0]
		self.assertEqual(
			json.loads(sub), {q["Single Choice"]: False, q["True False"]: True, q["Multiple Choice"]: False}
		)

		# change the answer key afterwards: stored results must still be used
		quiz.reload()
		quiz.questions[0].correct_answers = "1"
		quiz.save()

		frappe.set_user(self.vip)  # instructor
		_cols, rows, _msg, chart, summary = quiz_report.execute({"quiz": quiz.name})
		single = rows[0]
		self.assertEqual((single["answered"], single["correct"]), (3, 1))
		self.assertEqual(single["correct_rate"], 33.3)
		self.assertEqual(single["common_wrong"], "3")  # option 1 text is "3"
		self.assertEqual(rows[2]["answered"], 1)
		self.assertEqual(rows[2]["correct_rate"], 100)
		labels = {s["label"]: s["value"] for s in summary}
		self.assertEqual(labels["Attempts"], 3)
		self.assertEqual(labels["Learners Passed"], 50)
		self.assertTrue(chart)

	def test_quiz_analytics_requires_quiz_access(self):
		_, quiz, _ = self._lesson_with_quiz()
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			quiz_report.execute({"quiz": quiz.name})

	def test_learner_progress_report(self):
		lesson, quiz, q = self._lesson_with_quiz()
		other = publish(make_content(self.space, "Other", content_type="Lesson", visibility="Public"))
		frappe.set_user(self.learner)
		api.track_view(other.name)
		api.submit_quiz(
			quiz.name, {q["Single Choice"]: [2], q["True False"]: [1], q["Multiple Choice"]: [2, 4]}
		)

		frappe.set_user(self.vip)
		_cols, rows, _msg, _chart, summary = progress_report.execute({"space": self.space})
		by_content = {r.content: r for r in rows if r.user == self.learner}
		self.assertEqual(by_content[lesson.name].status, "Completed")
		self.assertEqual(by_content[lesson.name].best_score, 100)
		self.assertEqual(by_content[lesson.name].quiz_attempts, 1)
		self.assertEqual(by_content[other.name].status, "In Progress")
		self.assertIsNone(by_content[other.name].best_score)
		self.assertEqual({s["label"]: s["value"] for s in summary}["Completion Rate"], 50)

		_c, rows, *_ = progress_report.execute({"status": "Completed"})
		self.assertTrue(rows and all(r.status == "Completed" for r in rows))

		frappe.set_user(self.learner)  # learners only see their own rows
		_c, rows, *_ = progress_report.execute({})
		self.assertEqual({r.user for r in rows}, {self.learner})

	def test_onload_flags(self):
		doc = make_content(self.space, "Onload")
		doc = frappe.get_doc("TCD Content", doc.name)
		doc.run_method("onload")
		self.assertTrue(doc.get_onload().require_approval)
		self.assertTrue(doc.get_onload().is_reviewer)
		self.assertTrue(doc.get_onload().portal_url.startswith("/learn/p4-public/"))
