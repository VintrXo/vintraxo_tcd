"""Phase 10: the code runner client. The runner itself is mocked: no code is executed anywhere."""

import base64
import json
from unittest.mock import MagicMock, patch

import frappe
import requests

from vintraxo_tcd import api
from vintraxo_tcd.core import assessment, runner
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course
from vintraxo_tcd.tests.test_ph4_assessment import question

POST = "vintraxo_tcd.core.runner.requests.post"


def b64(text):
	return base64.b64encode(text.encode()).decode()


def judge0(stdout="", status=3, compile_output=None, stderr=None, http=201):
	r = MagicMock()
	r.status_code = http
	r.json.return_value = {
		"stdout": b64(stdout) if stdout else None,
		"stderr": b64(stderr) if stderr else None,
		"compile_output": b64(compile_output) if compile_output else None,
		"status": {"id": status, "description": "x"},
		"time": "0.012",
		"memory": 2048,
	}
	return r


class TestPhase10Runner(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Code Run", "TCD Question", "TCD Quiz Bank Item", *CLEAN):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		self.configure(runner_enabled=1)
		self.space = make_space("ph10-space").name
		self.l1 = lesson(self.space, "Runner lesson")

	def tearDown(self):
		frappe.set_user("Administrator")
		self.configure(runner_enabled=0)

	def configure(self, **values):
		s = frappe.get_single("TCD Settings")
		s.update(
			{
				"runner_url": "http://10.0.0.5:2358/",
				"runner_token": "tok",
				"runner_runs_per_minute": 10,
				"runner_languages": [],
				"enable_portal": 1,
				**values,
			}
		)
		s.save()
		frappe.clear_document_cache("TCD Settings", "TCD Settings")

	# ------------------------------------------------------------ settings

	def test_settings(self):
		s = frappe.get_single("TCD Settings")
		self.assertEqual(s.runner_url, "http://10.0.0.5:2358")
		self.assertEqual(runner.languages()["java"], 62)  # defaults seeded
		self.assertIn("cpp", api.playground_config()["runner_languages"])
		with self.assertRaises(frappe.ValidationError):
			self.configure(runner_url="ftp://runner")
		with self.assertRaises(frappe.ValidationError):
			self.configure(runner_languages=[{"language": "java", "runner_language_id": 62}] * 2)
		self.configure(runner_cpu_seconds=99, runner_memory_mb=1)
		s = frappe.get_single("TCD Settings")
		self.assertEqual((s.runner_cpu_seconds, s.runner_memory_mb), (15, 32))  # clamped
		self.configure(runner_enabled=0)
		self.assertEqual(runner.languages(), {})
		self.assertEqual(api.playground_config()["runner_languages"], [])

	# ------------------------------------------------------------ practice runs

	def test_practice_run_and_log(self):
		frappe.set_user(self.learner)
		with patch(POST, return_value=judge0("مرحبا\n")) as post:
			out = api.run_code(
				"java", 'class Main { public static void main(String[] a) { System.out.println("مرحبا"); } }'
			)
		self.assertEqual((out["status"], out["output"], out["time_ms"]), ("Finished", "مرحبا\n", 12.0))
		kwargs = post.call_args.kwargs
		self.assertTrue(
			post.call_args.args[0].startswith(
				"http://10.0.0.5:2358/submissions?base64_encoded=true&wait=true"
			)
		)
		payload = kwargs["json"]
		self.assertEqual((payload["language_id"], payload["enable_network"]), (62, False))
		self.assertEqual(payload["memory_limit"], 256 * 1024)
		self.assertIn("مرحبا", base64.b64decode(payload["source_code"]).decode())
		self.assertEqual(kwargs["headers"]["X-Auth-Token"], "tok")
		self.assertFalse(kwargs["allow_redirects"])

		frappe.set_user("Administrator")
		log = frappe.get_doc("TCD Code Run", {"user": self.learner})
		self.assertEqual((log.language, log.purpose, log.status), ("java", "Practice", "Finished"))
		self.assertEqual(len(log.code_hash), 64)  # the code itself is not stored
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Code Run", "read"))

	def test_statuses_errors_and_limits(self):
		frappe.set_user(self.learner)
		with patch(POST, return_value=judge0(status=6, compile_output="error: ';' expected")):
			out = api.run_code("cpp", "int main(){")
		self.assertEqual(out["status"], "Compilation Error")
		self.assertIn("expected", out["error"])
		with patch(POST, return_value=judge0(status=5)):
			self.assertEqual(api.run_code("go", "for {}")["status"], "Time Limit")
		with patch(POST, side_effect=requests.ConnectionError("down")):
			with self.assertRaises(runner.RunnerError):
				api.run_code("c", "int main(){}")
		with self.assertRaises(runner.RunnerError):
			api.run_code("cobol", "DISPLAY 1")
		with self.assertRaises(runner.RunnerError):
			api.run_code("java", "x" * (65 * 1024))

		frappe.set_user("Administrator")
		self.assertEqual(frappe.db.count("TCD Code Run", {"status": "Error"}), 1)  # the outage is logged
		self.configure(runner_runs_per_minute=1)
		frappe.db.delete("TCD Code Run")
		frappe.set_user(self.learner)
		with patch(POST, return_value=judge0("1")):
			api.run_code("bash", "echo 1")
			with self.assertRaises(runner.RunnerError):
				api.run_code("bash", "echo 1")
		frappe.set_user("Guest")
		with self.assertRaises(frappe.PermissionError):
			api.run_code("bash", "echo 1")

	def test_runner_off(self):
		self.configure(runner_enabled=0)
		frappe.set_user(self.learner)
		with self.assertRaises(runner.RunnerError):
			api.run_code("java", "x")
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			question("Code", code_language="java", expected_output="42")  # needs the runner

	# ------------------------------------------------------------ grading on the runner

	def _quiz(self, q):
		course = make_course(self.space, "Runner course", [[self.l1]], instructors=[self.vip])
		quiz = frappe.get_doc(
			{
				"doctype": "TCD Quiz",
				"title": "Runner quiz",
				"content": self.l1.name,
				"pass_percentage": 50,
				"max_attempts": 0,
				"bank_items": [{"question": q.name}],
			}
		).insert()
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		return quiz

	def test_server_grading_ignores_device_output(self):
		java = question("Code", code_language="java", expected_output="42", points=2)
		self.assertTrue(assessment.payload(assessment.item_from_bank(java), {})["run_on_server"])
		quiz = self._quiz(java)
		forged = {java.name: {"code": "print 41", "output": "42"}}  # device claims the right output

		with patch(POST, return_value=judge0("41\n")):
			res = api.submit_quiz(quiz.name, forged)
		self.assertFalse(res["passed"])  # the runner's output counts

		with patch(POST, return_value=judge0("42\n")):
			self.assertTrue(
				api.submit_quiz(quiz.name, {java.name: {"code": "print 42", "output": ""}})["passed"]
			)

		# a learner cannot send the runner's output themselves
		sneaky = {java.name: {"code": "print 41", "output": "42", "server_output": "42"}}
		with patch(POST, return_value=judge0("41\n")) as post:
			self.assertFalse(api.submit_quiz(quiz.name, sneaky)["passed"])
		post.assert_called_once()

		with patch(POST, side_effect=requests.ConnectionError("down")):
			res = api.submit_quiz(quiz.name, forged)
		self.assertTrue(res["pending_review"])  # outage: a person decides, not "wrong"
		frappe.set_user("Administrator")
		stored = json.loads(frappe.db.get_value("TCD Quiz Submission", res["submission"], "answers"))
		self.assertIsNone(stored[java.name]["server_output"])
		runs = frappe.db.count("TCD Code Run", {"purpose": "Grading"})
		frappe.set_user(self.vip)
		with patch(POST) as post:
			api.get_review_items(res["submission"])
		post.assert_not_called()  # reviewing never re-runs code
		frappe.set_user("Administrator")
		self.assertEqual(frappe.db.count("TCD Code Run", {"purpose": "Grading"}), runs)

	def test_python_question_graded_on_server(self):
		py = question(
			"Code", code_language="python", expected_output="ok", grade_on_server=1, setup_code="x = 1"
		)
		self.assertFalse(
			assessment.payload(assessment.item_from_bank(py), {})["run_on_server"]
		)  # practice in browser
		quiz = self._quiz(py)
		with patch(POST, return_value=judge0("no")) as post:
			res = api.submit_quiz(quiz.name, {py.name: {"code": "print('no')", "output": "ok"}})
		self.assertFalse(res["passed"])
		sent = base64.b64decode(post.call_args.kwargs["json"]["source_code"]).decode()
		self.assertTrue(sent.startswith("x = 1\n"))  # setup code runs first

	def test_playground_block_with_runner_language(self):
		page = lesson(
			self.space,
			"Java page",
			blocks=json.dumps([{"type": "playground", "language": "java", "code": "class Main {}"}]),
		)
		self.assertEqual(json.loads(page.blocks)[0]["language"], "java")
