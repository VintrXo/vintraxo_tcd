import frappe
from frappe.utils import add_days, add_months, getdate, nowdate

from vintraxo_tcd import api
from vintraxo_tcd.core import governance
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson
from vintraxo_tcd.vintraxo_tcd.report.tcd_acknowledgment_status import tcd_acknowledgment_status as ack_report


class TestPhase6Governance(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Acknowledgment", "TCD Governance Version", "TCD Governance Document", *CLEAN):
			frappe.db.delete(dt)
		for child in ("TCD Governance Role", "TCD Governance Department", "TCD Governance Link"):
			frappe.db.delete(child)
		frappe.db.delete("ToDo", {"reference_type": "TCD Governance Document"})
		self.space = make_space("ph6-space").name

	def tearDown(self):
		frappe.set_user("Administrator")

	def make_doc(self, code="POL-1", roles=("TCD Learner",), **kw):
		frappe.set_user("Administrator")
		return frappe.get_doc(
			{
				"doctype": "TCD Governance Document",
				"title": "Code of conduct",
				"doc_kind": "Policy",
				"code": code,
				"document_owner": self.author,
				"approver": self.vip,
				"body": "## Rules\n\nBe kind. <script>alert(1)</script>",
				"review_cycle_months": 12,
				"audience_roles": [{"role": r} for r in roles],
				**kw,
			}
		).insert()

	def move(self, doc, status, user="Administrator"):
		frappe.set_user(user)
		api.set_governance_status(doc.name, status)
		return frappe.get_doc("TCD Governance Document", doc.name)

	def activate(self, doc):
		for status in ("Review", "Approval", "Active"):
			doc = self.move(doc, status)
		return doc

	# ------------------------------------------------------------ lifecycle

	def test_lifecycle_and_versions(self):
		doc = self.make_doc(code="pol-hr-1")
		self.assertEqual(doc.name, "POL-HR-1")  # code upper-cased
		with self.assertRaises(frappe.ValidationError):
			self.move(doc, "Active")  # Draft -> Active not allowed
		doc = self.move(doc, "Review", self.author)
		with self.assertRaises(frappe.PermissionError):
			self.move(doc, "Approval", self.author)
		doc = self.move(doc, "Approval", self.reviewer)
		with self.assertRaises(frappe.PermissionError):
			self.move(doc, "Active", self.reviewer)  # not the approver
		doc = self.move(doc, "Active", self.vip)  # the approver (no write permission needed)
		with self.assertRaises(frappe.PermissionError):
			self.move(doc, "Revision", self.vip)  # but nothing else
		self.assertEqual(doc.version, 1)
		self.assertEqual(getdate(doc.next_review_date), getdate(add_months(nowdate(), 12)))
		self.assertTrue(frappe.db.exists("TCD Governance Version", "POL-HR-1-v1"))

		frappe.set_user("Administrator")
		doc.reload()
		doc.body = "changed"
		with self.assertRaises(frappe.ValidationError):
			doc.save()  # active is locked

		doc = self.move(doc, "Revision")
		doc.body = "## Rules v2"
		doc.save()
		frappe.set_user(self.learner)
		policy = api.get_policy("POL-HR-1")
		self.assertEqual(policy["version"], 1)  # readers keep the approved version
		self.assertTrue(policy["under_revision"])
		self.assertNotIn("<script", policy["html"])

		frappe.set_user("Administrator")
		for status in ("Review", "Approval", "Active"):
			doc = self.move(doc, status)
		self.assertEqual(doc.version, 2)
		frappe.set_user(self.learner)
		self.assertIn("Rules v2", api.get_policy("POL-HR-1")["html"])

	def test_validation(self):
		with self.assertRaises(frappe.ValidationError):
			self.make_doc(effective_date="2030-01-10", expiry_date="2030-01-01")
		with self.assertRaises(frappe.ValidationError):
			self.make_doc(code="POL-L", links=[{"target_type": "Content"}])
		# without ERPNext the department is stored and ignored
		self.assertFalse(governance.has_departments())
		doc = self.activate(self.make_doc(code="POL-D", audience_departments=[{"department": "Sales"}]))
		frappe.set_user(self.learner)
		self.assertEqual(api.get_policy(doc.name)["version"], 1)

	# ------------------------------------------------------------ audience and acknowledgment

	def test_audience_and_acknowledgment(self):
		learners = self.activate(self.make_doc(code="POL-A"))
		staff_only = self.activate(self.make_doc(code="POL-S", roles=("TCD Instructor",)))
		everyone = self.activate(self.make_doc(code="POL-E", roles=()))
		draft = self.make_doc(code="POL-DRAFT")

		frappe.set_user(self.learner)
		self.assertEqual(
			{d.name for d in governance.documents_for(self.learner)}, {learners.name, everyone.name}
		)
		for hidden in (staff_only.name, draft.name):
			with self.assertRaises(frappe.DoesNotExistError):
				api.get_policy(hidden)
		with self.assertRaises(frappe.DoesNotExistError):
			api.acknowledge(staff_only.name)

		self.assertEqual(
			{d.name for d in governance.pending_for(self.learner)}, {learners.name, everyone.name}
		)
		first = api.acknowledge(learners.name)
		again = api.acknowledge(learners.name)
		self.assertEqual(first["acknowledged_on"], again["acknowledged_on"])  # idempotent
		self.assertEqual(frappe.db.count("TCD Acknowledgment", {"user": self.learner}), 1)
		self.assertTrue(api.get_policy(learners.name)["acknowledged"])

		ack = frappe.get_doc("TCD Acknowledgment", {"user": self.learner})
		ack.statement = "forged"
		with self.assertRaises(frappe.ValidationError):
			ack.save(ignore_permissions=True)
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "TCD Acknowledgment",
					"governance_document": everyone.name,
					"version": 1,
					"user": self.learner,
				}
			).insert(ignore_permissions=True)

		# a new version needs a new acknowledgment
		frappe.set_user("Administrator")
		doc = self.move(learners, "Revision")
		for status in ("Review", "Approval", "Active"):
			doc = self.move(doc, status)
		frappe.set_user(self.learner)
		self.assertIn(learners.name, {d.name for d in governance.pending_for(self.learner)})

		frappe.set_user(self.vip)
		api.acknowledge(staff_only.name)
		frappe.set_user(self.learner)
		self.assertEqual(
			{a.user for a in frappe.get_list("TCD Acknowledgment", fields=["user"])}, {self.learner}
		)
		frappe.set_user(self.reviewer)
		self.assertEqual(len(frappe.get_list("TCD Acknowledgment")), 2)

	def test_acknowledgment_report(self):
		doc = self.activate(self.make_doc(code="POL-R"))
		frappe.set_user(self.learner)
		api.acknowledge(doc.name)
		frappe.set_user("Administrator")
		_c, rows, _m, _ch, summary = ack_report.execute({"document": doc.name})
		by_user = {r["user"]: r for r in rows}
		self.assertEqual(by_user[self.learner]["acknowledged"], 1)
		self.assertEqual(by_user[self.vip]["acknowledged"], 0)  # vip also holds TCD Learner
		_c, missing, *_ = ack_report.execute({"document": doc.name, "only_missing": 1})
		self.assertNotIn(self.learner, {r["user"] for r in missing})
		self.assertEqual({s["label"]: s["value"] for s in summary}["Acknowledged"], 1)

	# ------------------------------------------------------------ scheduler

	def test_daily_job(self):
		expired = self.activate(self.make_doc(code="POL-X"))
		frappe.db.set_value("TCD Governance Document", expired.name, "expiry_date", add_days(nowdate(), -1))
		due = self.activate(self.make_doc(code="POL-Y"))
		frappe.db.set_value("TCD Governance Document", due.name, "next_review_date", add_days(nowdate(), 3))
		no_expiry = self.activate(self.make_doc(code="POL-Z"))
		governance.daily()
		governance.daily()  # runs twice: still one reminder
		self.assertEqual(frappe.db.get_value("TCD Governance Document", expired.name, "status"), "Revision")
		# regression: documents without an expiry date must stay Active
		self.assertEqual(frappe.db.get_value("TCD Governance Document", no_expiry.name, "status"), "Active")
		todos = frappe.get_all("ToDo", filters={"reference_name": due.name}, fields=["allocated_to"])
		self.assertEqual([t.allocated_to for t in todos], [self.author])

	# ------------------------------------------------------------ portal

	def test_portal(self):
		page = lesson(self.space, "Safety lesson")
		doc = self.activate(
			self.make_doc(
				code="SOP-1", doc_kind="SOP", links=[{"target_type": "Content", "content": page.name}]
			)
		)
		hidden = self.activate(self.make_doc(code="SOP-2", roles=("TCD Instructor",)))
		status, html, _ = render("/learn/policies", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("SOP-1", html)
		self.assertNotIn("SOP-2", html)
		status, html, _ = render("/learn/policies/SOP-1", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-ack-btn", html)
		self.assertIn("Safety lesson", html)  # related learning
		self.assertNotIn("<script>alert(1)</script>", html)
		status, _, _ = render(f"/learn/policies/{hidden.name}", self.learner)
		self.assertEqual(status, 404)
		status, html, _ = render(f"/learn/{self.space}/{page.slug}", self.learner)
		self.assertIn("/learn/policies/SOP-1", html)
		status, html, _ = render("/learn/my", self.learner)
		self.assertIn(doc.title, html)  # pending acknowledgment
