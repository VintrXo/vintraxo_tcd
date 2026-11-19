import json

import frappe

from vintraxo_tcd import api
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user, publish


def make_quiz(content, **kw):
	return frappe.get_doc(
		{
			"doctype": "TCD Quiz",
			"title": "Quiz",
			"content": content,
			"pass_percentage": 50,
			"questions": [
				{
					"question": "2 + 2 ?",
					"question_type": "Single Choice",
					"options": "3\n4\n5",
					"correct_answers": "2",
				},
				{"question": "Python is a language", "question_type": "True False", "correct_answers": "1"},
				{
					"question": "Even numbers",
					"question_type": "Multiple Choice",
					"options": "1\n2\n3\n4",
					"correct_answers": "4, 2",
					"points": 2,
				},
			],
			**kw,
		}
	).insert()


class TestP2Learning(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		settings = frappe.get_single("TCD Settings")
		settings.require_approval_before_publish = 1
		settings.enable_playgrounds = 1
		settings.save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			"TCD Quiz Submission",
			"TCD Quiz Question",
			"TCD Quiz",
			"TCD Progress",
			"TCD Tutorial Lesson",
			"TCD Content Relation",
			"TCD Content Version",
			"TCD Content",
		):
			frappe.db.delete(dt)
		self.space = make_space("p2-public").name
		self.l1 = publish(make_content(self.space, "Lesson 1", content_type="Lesson", visibility="Public"))
		self.l2 = publish(make_content(self.space, "Lesson 2", content_type="Lesson", visibility="Public"))
		self.l3 = publish(make_content(self.space, "Lesson 3", content_type="Lesson", visibility="Public"))
		self.tut = publish(
			make_content(
				self.space,
				"Tutorial",
				content_type="Tutorial",
				visibility="Public",
				lessons=[
					{"lesson": self.l1.name},
					{"lesson": self.l2.name},
					{"lesson": self.l3.name, "is_optional": 1},
				],
			)
		)

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ tutorial structure

	def test_tutorial_lesson_rules(self):
		article = make_content(self.space, "Article")
		other = make_space("p2-other").name
		foreign = make_content(other, "Foreign", content_type="Lesson")
		for lessons in (
			[{"lesson": article.name}],
			[{"lesson": foreign.name}],
			[{"lesson": self.l1.name}, {"lesson": self.l1.name}],
		):
			with self.assertRaises(frappe.ValidationError):
				make_content(self.space, "Bad tutorial", content_type="Tutorial", lessons=lessons)

		# lessons are dropped for non-tutorials
		doc = make_content(self.space, "Not a tutorial", lessons=[{"lesson": self.l1.name}])
		self.assertEqual(doc.lessons, [])

	def test_published_tutorial_locked_and_snapshotted(self):
		tut = frappe.get_doc("TCD Content", self.tut.name)
		self.assertEqual(
			json.loads(frappe.db.get_value("TCD Content Version", tut.current_version, "lessons"))[0][
				"lesson"
			],
			self.l1.name,
		)
		tut.lessons = tut.lessons[:1]
		with self.assertRaises(frappe.ValidationError):
			tut.save()

	# ------------------------------------------------------------ progress

	def test_progress_rollup(self):
		frappe.set_user(self.learner)
		api.track_view(self.l1.name)
		self.assertEqual(api.get_lesson(self.l1.name)["progress"], "In Progress")

		api.complete_lesson(self.l1.name)
		summary = api.get_tutorial_progress(self.tut.name)
		self.assertEqual((summary["required"], summary["completed"], summary["percent"]), (2, 1, 50))
		self.assertFalse(summary["is_complete"])
		tut_progress = frappe.get_all(
			"TCD Progress", filters={"content": self.tut.name}, fields=["status", "percent"]
		)
		self.assertEqual(tut_progress[0].status, "In Progress")

		api.complete_lesson(self.l2.name)  # optional lesson 3 not needed
		self.assertTrue(api.get_tutorial_progress(self.tut.name)["is_complete"])
		self.assertEqual(api.get_lesson(self.tut.name)["progress"], "Completed")

		# viewing again never downgrades
		api.track_view(self.l1.name)
		self.assertEqual(api.get_lesson(self.l1.name)["progress"], "Completed")

		with self.assertRaises(frappe.ValidationError):
			api.complete_lesson(self.tut.name)

	def test_lesson_navigation_and_playground(self):
		frappe.set_user(self.learner)
		data = api.get_lesson(self.l2.name, tutorial=self.tut.name)
		self.assertEqual((data["prev"], data["next"]), (self.l1.name, self.l3.name))
		self.assertEqual(data["direction"], "rtl" if data["language"] == "ar" else "ltr")
		self.assertTrue(any(b["type"] == "playground" for b in data["blocks"]))

		frappe.set_user("Administrator")
		frappe.db.set_single_value("TCD Settings", "enable_playgrounds", 0)
		frappe.clear_document_cache("TCD Settings", "TCD Settings")
		try:
			frappe.set_user(self.learner)
			data = api.get_lesson(self.l2.name)
			self.assertFalse(data["playground"]["enabled"])
			self.assertFalse(any(b["type"] == "playground" for b in data["blocks"]))
		finally:
			frappe.set_user("Administrator")
			frappe.db.set_single_value("TCD Settings", "enable_playgrounds", 1)
			frappe.clear_document_cache("TCD Settings", "TCD Settings")

	def test_progress_privacy(self):
		frappe.set_user(self.learner)
		api.complete_lesson(self.l1.name)
		frappe.set_user(self.vip)
		api.track_view(self.l1.name)

		frappe.set_user(self.learner)
		users = set(frappe.get_list("TCD Progress", pluck="user"))
		self.assertEqual(users, {self.learner})
		other = frappe.db.get_value("TCD Progress", {"user": self.vip})
		self.assertFalse(frappe.has_permission("TCD Progress", "read", other))

		frappe.set_user(self.vip)  # instructor: sees learners' progress
		users = set(frappe.get_list("TCD Progress", pluck="user"))
		self.assertEqual(users, {self.learner, self.vip})

		fake = {"doctype": "TCD Progress", "user": self.learner, "content": self.l2.name}
		with self.assertRaises(frappe.PermissionError):  # no create DocPerm
			frappe.get_doc(fake).insert()
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):  # only the progress service writes
			frappe.get_doc(fake).insert()

	def test_hidden_lesson_not_accessible(self):
		draft = make_content(self.space, "Draft lesson", content_type="Lesson", visibility="Public")
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.get_lesson(draft.name)
		with self.assertRaises(frappe.PermissionError):
			api.complete_lesson(draft.name)

	# ------------------------------------------------------------ quiz

	def test_quiz_definition_validation(self):
		bad_questions = [
			{
				"question": "q",
				"question_type": "Single Choice",
				"options": "only one",
				"correct_answers": "1",
			},
			{"question": "q", "question_type": "Single Choice", "options": "a\nb", "correct_answers": "3"},
			{"question": "q", "question_type": "Single Choice", "options": "a\nb", "correct_answers": "1,2"},
			{"question": "q", "question_type": "True False", "correct_answers": "x"},
		]
		for q in bad_questions:
			with self.assertRaises(frappe.ValidationError, msg=q):
				frappe.get_doc(
					{"doctype": "TCD Quiz", "title": "Bad", "content": self.l1.name, "questions": [q]}
				).insert()
		quiz = make_quiz(self.l1.name)
		self.assertEqual(quiz.questions[2].correct_answers, "2,4")

	def test_quiz_flow(self):
		quiz = make_quiz(self.l1.name, max_attempts=2)
		q = {row.question_type: row.name for row in quiz.questions}

		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Quiz", "read", quiz.name))  # answers stay hidden
		payload = api.get_quiz(quiz.name)
		self.assertEqual(len(payload["questions"]), 3)
		self.assertNotIn("correct_answers", json.dumps(payload))
		self.assertNotIn("correct", payload["questions"][0])

		with self.assertRaises(frappe.ValidationError):
			api.complete_lesson(self.l1.name)  # required quiz not passed

		res = api.submit_quiz(quiz.name, json.dumps({q["Single Choice"]: 1}))
		self.assertFalse(res["passed"])
		self.assertEqual((res["score"], res["max_score"]), (0, 4))

		res = api.submit_quiz(
			quiz.name, {q["Single Choice"]: [2], q["True False"]: 1, q["Multiple Choice"]: [2, 4]}
		)
		self.assertTrue(res["passed"])
		self.assertEqual(res["percentage"], 100)
		self.assertEqual(res["results"][2]["correct"], [2, 4])
		self.assertEqual(api.get_lesson(self.l1.name)["progress"], "Completed")

		with self.assertRaises(frappe.ValidationError):
			api.submit_quiz(quiz.name, {})  # attempts exhausted

		sub = frappe.get_doc("TCD Quiz Submission", res["submission"])
		sub.percentage = 0
		with self.assertRaises(frappe.ValidationError):
			sub.save(ignore_permissions=True)

	def test_quiz_on_hidden_content(self):
		draft = make_content(self.space, "Draft with quiz", content_type="Lesson", visibility="Public")
		quiz = make_quiz(draft.name)
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.get_quiz(quiz.name)
		with self.assertRaises(frappe.PermissionError):
			api.submit_quiz(quiz.name, {})

	def test_submissions_privacy(self):
		quiz = make_quiz(self.l1.name)
		frappe.set_user(self.vip)
		api.submit_quiz(quiz.name, {})
		frappe.set_user(self.learner)
		api.submit_quiz(quiz.name, {})
		self.assertEqual(set(frappe.get_list("TCD Quiz Submission", pluck="user")), {self.learner})
		frappe.set_user(self.vip)
		self.assertEqual(set(frappe.get_list("TCD Quiz Submission", pluck="user")), {self.learner, self.vip})
