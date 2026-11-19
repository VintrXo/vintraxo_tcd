import json
from unittest.mock import MagicMock, patch

import frappe
from frappe.utils import add_days, getdate, now_datetime, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import integrations, training
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, enrollment, lesson, make_course
from vintraxo_tcd.vintraxo_tcd.report.tcd_training_compliance import tcd_training_compliance as report

POST = "vintraxo_tcd.core.integrations.requests.post"


def response(code=200, text="ok"):
	r = MagicMock()
	r.status_code, r.text = code, text
	return r


class TestPhase8Integrations(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for dt in ("TCD Training Rule", "TCD Rule Role", "TCD Rule HR Filter"):
			frappe.db.delete(dt)
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			"TCD Integration Event",
			"TCD Connector Event",
			"TCD Connector",
			"TCD Training Rule",
			"TCD Rule Role",
			"TCD Rule HR Filter",
			"TCD Certificate",
			*CLEAN,
		):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		frappe.db.delete("TCD Course Instructor")
		self.space = make_space("ph8-space").name
		self.l1 = lesson(self.space, "Integration lesson")

	def tearDown(self):
		frappe.set_user("Administrator")

	def connector(self, events=("Enrollment Created",), **kw):
		values = {
			"doctype": "TCD Connector",
			"connector_name": kw.pop("connector_name", "Test hook"),
			"endpoint_url": "http://127.0.0.1:9/hook",
			"allow_private_network": 1,
			"secret": "s3cret",
			"events": [{"event": e} for e in events],
			**kw,
		}
		return frappe.get_doc(values).insert()

	def queued(self, event=None):
		filters = {"event": event} if event else {}
		return frappe.get_all("TCD Integration Event", filters=filters, pluck="name", order_by="creation asc")

	# ------------------------------------------------------------ connector registry

	def test_connector_validation(self):
		for url in (
			"ftp://example.com/x",
			"http://example.com/x",
			"https://127.0.0.1/x",
			"https://10.1.2.3/x",
		):
			with self.assertRaises(frappe.ValidationError, msg=url):
				self.connector(endpoint_url=url, allow_private_network=0, connector_name=url)
		with self.assertRaises(frappe.ValidationError):
			integrations.check_url("https://localhost/x")  # resolved on send
		with self.assertRaises(frappe.ValidationError):
			self.connector(events=("Certificate Issued", "Certificate Issued"))
		ok = self.connector(max_attempts=99, timeout_seconds=500)
		self.assertEqual((ok.max_attempts, ok.timeout_seconds), (len(integrations.BACKOFF_MINUTES) + 1, 30))
		self.assertNotEqual(frappe.db.get_value("TCD Connector", ok.name, "secret"), "s3cret")

	# ------------------------------------------------------------ emit and deliver

	def test_events_are_signed_and_delivered(self):
		self.connector(
			events=("Enrollment Created", "Enrollment Completed", "Certificate Issued"),
			rate_limit_per_minute=0,
		)
		self.connector(connector_name="Disabled", enabled=0, events=("Enrollment Created",))
		course = make_course(self.space, "Hooked course", [[self.l1]], issue_certificate=1)
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		frappe.set_user("Administrator")
		events = frappe.get_all(
			"TCD Integration Event", fields=["name", "event", "connector"], order_by="creation asc"
		)
		self.assertEqual(
			[e.event for e in events], ["Enrollment Created", "Enrollment Completed", "Certificate Issued"]
		)
		self.assertEqual({e.connector for e in events}, {"Test hook"})

		with patch(POST, return_value=response()) as post:
			self.assertEqual([integrations.deliver(e.name) for e in events], ["Sent"] * 3)
		self.assertEqual(integrations.deliver(events[0].name), "Sent")  # already sent: not resent
		self.assertEqual(post.call_count, 3)
		kwargs = post.call_args_list[2].kwargs
		headers, body = kwargs["headers"], kwargs["data"]
		self.assertFalse(kwargs["allow_redirects"])
		self.assertEqual(headers["X-TCD-Event"], "certificate.issued")
		self.assertEqual(
			headers["X-TCD-Signature"],
			"sha256=" + integrations.sign("s3cret", headers["X-TCD-Timestamp"], body),
		)
		envelope = json.loads(body)
		self.assertEqual(envelope["id"], events[2].name)
		self.assertEqual(envelope["data"]["user"], self.learner)
		self.assertIn("/verify/", envelope["data"]["verify_url"])

		# not subscribed: nothing queued
		frappe.db.delete("TCD Integration Event")
		frappe.set_user(self.vip)
		api.enroll("Course", course.name)
		frappe.set_user("Administrator")
		self.assertEqual(len(self.queued()), 1)

	def test_slack_format(self):
		self.connector(payload_format="Slack", secret="")
		course = make_course(self.space, "Slack course", [[self.l1]])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		frappe.set_user("Administrator")
		with patch(POST, return_value=response()) as post:
			integrations.deliver(self.queued()[0])
		body = json.loads(post.call_args.kwargs["data"])
		self.assertEqual(list(body), ["text"])
		self.assertIn(self.learner, body["text"])
		self.assertNotIn("X-TCD-Signature", post.call_args.kwargs["headers"])

	def test_retry_backoff_and_failure(self):
		self.connector(max_attempts=2)
		course = make_course(self.space, "Retry course", [[self.l1]])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		frappe.set_user("Administrator")
		name = self.queued()[0]
		with patch(POST, return_value=response(500, "boom")):
			self.assertEqual(integrations.deliver(name), "Queued")
		ev = frappe.get_doc("TCD Integration Event", name)
		self.assertEqual((ev.attempts, ev.response_code), (1, 500))
		self.assertIn("boom", ev.last_error)
		self.assertGreater(ev.next_attempt_on, now_datetime())
		with patch(POST, return_value=response()) as post:
			integrations.process_queue()  # not due yet
		post.assert_not_called()

		with patch(POST, side_effect=ConnectionError("refused")):
			self.assertEqual(integrations.deliver(name), "Failed")
		ev.reload()
		self.assertEqual(ev.attempts, 2)
		self.assertIn("ConnectionError", ev.last_error)

		api.retry_integration_event(name)
		ev.reload()
		self.assertEqual((ev.status, ev.attempts), ("Queued", 0))
		with patch(POST, return_value=response()):
			integrations.process_queue()
		self.assertEqual(frappe.db.get_value("TCD Integration Event", name, "status"), "Sent")
		with self.assertRaises(frappe.ValidationError):
			api.retry_integration_event(name)

	def test_rate_limit_and_blocked_url(self):
		hook = self.connector(rate_limit_per_minute=1)
		course = make_course(self.space, "Busy course", [[self.l1]])
		for user in (self.learner, self.vip):
			frappe.set_user(user)
			api.enroll("Course", course.name)
		frappe.set_user("Administrator")
		first, second = self.queued()
		with patch(POST, return_value=response()) as post:
			self.assertEqual(integrations.deliver(first), "Sent")
			self.assertEqual(integrations.deliver(second), "Queued")  # deferred, no attempt used
		self.assertEqual(post.call_count, 1)
		self.assertEqual(frappe.db.get_value("TCD Integration Event", second, "attempts"), 0)

		# an endpoint that turns private after saving is blocked on send, never retried
		frappe.db.set_value(
			"TCD Connector",
			hook.name,
			{"endpoint_url": "https://127.0.0.1/x", "allow_private_network": 0, "rate_limit_per_minute": 0},
		)
		with patch(POST, return_value=response()) as post:
			self.assertEqual(integrations.deliver(second), "Failed")
		post.assert_not_called()

	def test_policy_events(self):
		self.connector(events=("Policy Activated", "Policy Acknowledged"))
		doc = frappe.get_doc(
			{
				"doctype": "TCD Governance Document",
				"title": "Hooked policy",
				"code": "POL-H1",
				"document_owner": self.author,
				"approver": "Administrator",
				"audience_roles": [{"role": "TCD Learner"}],
			}
		).insert()
		for status in ("Review", "Approval", "Active"):
			api.set_governance_status(doc.name, status)
		frappe.set_user(self.learner)
		api.acknowledge(doc.name)
		api.acknowledge(doc.name)  # idempotent: one event
		frappe.set_user("Administrator")
		self.assertEqual(len(self.queued("Policy Activated")), 1)
		ack = frappe.get_doc("TCD Integration Event", self.queued("Policy Acknowledged")[0])
		self.assertEqual(len(self.queued("Policy Acknowledged")), 1)
		self.assertEqual(json.loads(ack.payload)["user"], self.learner)
		frappe.db.delete("TCD Governance Document", {"name": "POL-H1"})
		frappe.db.delete("TCD Governance Version", {"governance_document": "POL-H1"})
		frappe.db.delete("TCD Acknowledgment", {"governance_document": "POL-H1"})

	def test_permissions(self):
		hook = self.connector()
		course = make_course(self.space, "Private log", [[self.l1]])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		name = frappe.get_all("TCD Integration Event", pluck="name", ignore_permissions=True)[0]
		for user in (self.learner, self.author, self.vip):
			frappe.set_user(user)
			self.assertFalse(frappe.has_permission("TCD Connector", "read"))
			self.assertFalse(frappe.has_permission("TCD Integration Event", "read"))
			with self.assertRaises(frappe.PermissionError):
				api.test_connector(hook.name)
			with self.assertRaises(frappe.PermissionError):
				api.retry_integration_event(name)
		frappe.set_user(self.vip)  # instructors may read rules, not run them
		rule = self.rule(course.name)
		with self.assertRaises(frappe.PermissionError):
			api.apply_training_rule(rule.name)

	# ------------------------------------------------------------ training rules

	def rule(self, course=None, roles=("TCD Learner",), **kw):
		current = frappe.session.user
		frappe.set_user("Administrator")
		values = {
			"doctype": "TCD Training Rule",
			"title": kw.pop("title", "Onboarding"),
			"target_type": "Course",
			"course": course,
			"due_in_days": 10,
			"roles": [{"role": r} for r in roles],
			**kw,
		}
		doc = frappe.get_doc(values).insert()
		frappe.set_user(current)
		return doc

	def test_rule_enrolls_matching_users(self):
		course = make_course(self.space, "Mandatory course", [[self.l1]])
		rule = self.rule(course.name)
		people = [self.learner, self.vip, self.author, self.reviewer]
		self.assertEqual(training.apply_rule(rule.name, people), 2)  # learner + vip (both TCD Learner)
		e = enrollment(self.learner, course.name)
		self.assertEqual((e.mandatory, e.training_rule), (1, rule.name))
		self.assertEqual(getdate(e.due_date), getdate(add_days(nowdate(), 10)))
		self.assertIsNone(enrollment(self.author, course.name))
		self.assertEqual(training.apply_rule(rule.name, people), 0)  # idempotent
		training.apply_rule(rule.name)  # all users: same result for ours

		# an admin decision wins: a withdrawn enrollment is not re-opened
		frappe.db.set_value("TCD Enrollment", e.name, "status", "Withdrawn")
		training.apply_rule(rule.name)
		self.assertEqual(enrollment(self.learner, course.name).status, "Withdrawn")

		# new users and role changes are picked up on save
		newcomer = make_user("tcd-newcomer@test.local", ["TCD Learner"])
		self.assertTrue(enrollment(newcomer, course.name))
		frappe.get_doc("User", self.author).add_roles("TCD Learner")
		self.assertTrue(enrollment(self.author, course.name))
		make_user(self.author, ["TCD Content Author"])  # restore

		draft = make_course(self.space, "Draft course", [[self.l1]], publish_it=False)
		self.assertEqual(training.apply_rule(self.rule(draft.name, title="Draft").name), 0)
		disabled = self.rule(course.name, title="Off", enabled=0)
		self.assertEqual(training.apply_rule(disabled.name), 0)
		self.assertEqual(report.execute({"training_rule": rule.name})[1][0]["assigned"], 1)
		frappe.delete_doc("User", newcomer, force=True, ignore_permissions=True)

	def test_rule_validation(self):
		with self.assertRaises(frappe.ValidationError):
			self.rule(None)  # no target
		with self.assertRaises(frappe.ValidationError):
			self.rule(roles=("TCD Learner", "TCD Learner"), target_type="Content", content=self.l1.name)
		course = make_course(self.space, "Validation course", [[self.l1]])
		guide = self.rule(
			target_type="Content", content=self.l1.name, course=course.name, mandatory=1, due_in_days=5
		)
		self.assertEqual((guide.course, guide.mandatory, guide.due_in_days), (None, 0, 0))

	def test_hr_filters_are_guarded(self):
		course = make_course(self.space, "Sales course", [[self.l1]])
		rule = self.rule(course.name, hr_filters=[{"filter_type": "Department", "value": "Sales"}])
		self.assertFalse(training.hr_available())  # tcd.localhost has no ERPNext
		self.assertIsNone(training.employee_profile(self.learner))
		self.assertEqual(training.apply_rule(rule.name), 0)  # HR filter without HR matches nobody
		people = [self.learner, self.vip]

		profiles = {self.learner: frappe._dict(name="EMP-1", department="Sales", designation="Clerk")}
		with (
			patch.object(training, "hr_available", return_value=True),
			patch.object(training, "employee_profile", side_effect=profiles.get),
		):
			self.assertEqual(training.apply_rule(rule.name, people), 1)
			rule.append("hr_filters", {"filter_type": "Designation", "value": "Manager"})
			self.assertFalse(training.rule_matches(rule, self.learner))  # different filters: all must match
		self.assertTrue(enrollment(self.learner, course.name))
		self.assertIsNone(enrollment(self.vip, course.name))

	def test_role_guides_compliance_and_portal(self):
		course = make_course(self.space, "Compliance course", [[self.l1]])
		self.rule(course.name)
		training.apply_rule(frappe.get_all("TCD Training Rule", pluck="name")[0])
		self.rule(target_type="Content", content=self.l1.name, title="Guide", roles=("TCD Instructor",))
		frappe.db.set_value(
			"TCD Enrollment", enrollment(self.vip, course.name).name, "due_date", "2000-01-01"
		)
		self.assertEqual([g["title"] for g in training.role_guides(self.vip)], ["Integration lesson"])
		self.assertEqual(training.role_guides(self.learner), [])

		frappe.set_user(self.learner)
		api.complete_lesson(self.l1.name)
		frappe.set_user("Administrator")
		_c, rows, _m, _ch, summary = report.execute({})
		by_user = {r["user"]: r for r in rows}
		self.assertEqual((by_user[self.learner]["completed"], by_user[self.learner]["compliance"]), (1, 100))
		self.assertEqual((by_user[self.vip]["overdue"], by_user[self.vip]["compliance"]), (1, 0))
		self.assertEqual(
			{s["label"]: s["value"] for s in summary}["Learners"], len(rows)
		)  # the site may hold other learners

		status, html, _ = render("/learn/my", self.vip)
		self.assertEqual(status, 200)
		self.assertIn("tcd-role-guides", html)
		self.assertIn("tcd-badge-warn", html)  # mandatory badge
		frappe.set_user("Administrator")
		frappe.db.set_value("TCD Training Rule", {"title": "Guide"}, "content", "missing-page")
		self.assertEqual(training.role_guides(self.vip), [])  # dangling rule is skipped, no error
		status, _, _ = render("/learn/my", self.vip)
		self.assertEqual(status, 200)
