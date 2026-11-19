import json
import sys
import typing
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import ai
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson


class FakeProvider:
	"""Stands in for the model: records what would be sent, returns a canned Result."""

	calls: typing.ClassVar[list] = []
	reply = None

	def __init__(self, settings):
		self.settings = settings

	def complete(self, **kwargs):
		FakeProvider.calls.append(kwargs)
		reply = FakeProvider.reply(kwargs) if callable(FakeProvider.reply) else FakeProvider.reply
		return reply or ai.Result(
			text="ok", segments=[{"text": "ok", "sources": []}], input_tokens=1, output_tokens=1
		)


def result(**kw):
	values = {
		"input_tokens": 1000,
		"output_tokens": 500,
		"model": "fake-model",
		"stop_reason": "end_turn",
		**kw,
	}
	return ai.Result(**values)


class TestPhase9AI(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		frappe.get_single("TCD Settings").update({"enable_portal": 1}).save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD AI Usage Log", "TCD Question", "TCD Rule Role", *CLEAN):
			frappe.db.delete(dt)
		self.configure(enabled=1)
		self.space = make_space("ph9-space").name
		self.page = lesson(self.space, "Reading python files", summary="open() reads files")
		self.secret = lesson(
			make_space("ph9-secret", visibility="Restricted", roles=("TCD Instructor",)).name,
			"Secret python salaries",
		)
		self.draft = frappe.get_doc(
			{"doctype": "TCD Content", "space": self.space, "title": "Draft python notes", "blocks": "[]"}
		).insert()
		FakeProvider.calls, FakeProvider.reply = [], None
		patcher = patch.object(ai, "providers", return_value={"Anthropic": FakeProvider})
		patcher.start()
		self.addCleanup(patcher.stop)

	def tearDown(self):
		frappe.set_user("Administrator")

	def configure(self, **values):
		current = frappe.session.user
		frappe.set_user("Administrator")
		s = frappe.get_single("TCD AI Settings")
		s.update(
			{
				"provider": "Anthropic",
				"model": "claude-opus-5-5",
				"input_price_per_mtok": 4,
				"output_price_per_mtok": 20,
				"monthly_budget": 0,
				"daily_requests_per_user": 0,
				"expand_queries": 0,
				"exclude_restricted": 1,
				"redact_personal_data": 1,
				"log_prompts": 0,
				"allowed_roles": [],
				**values,
			}
		)
		s.save()
		frappe.set_user(current)

	def sent_titles(self, call=-1):
		return [d["title"] for d in FakeProvider.calls[call]["documents"]]

	# ------------------------------------------------------------ access

	def test_access_and_switch(self):
		self.configure(enabled=0)
		frappe.set_user(self.learner)
		self.assertFalse(api.ai_status()["enabled"])
		with self.assertRaises(ai.AIError):
			api.ai_ask("python files")
		self.configure(enabled=1, allowed_roles=[{"role": "TCD Instructor"}])
		with self.assertRaises(frappe.PermissionError):
			api.ai_ask("python files")
		frappe.set_user(self.vip)
		self.assertTrue(api.ai_status()["enabled"])
		frappe.set_user("Guest")
		self.assertFalse(ai.can_use("Guest"))
		self.assertEqual(FakeProvider.calls, [])

	# ------------------------------------------------------------ retrieval before the call

	def test_retrieval_is_permission_filtered_before_the_call(self):
		FakeProvider.reply = result(text="Use open().", segments=[{"text": "Use open().", "sources": [0]}])
		frappe.set_user(self.learner)
		answer = api.ai_ask("python files salaries notes")
		self.assertEqual(self.sent_titles(), ["Reading python files"])  # no restricted page, no draft
		self.assertTrue(FakeProvider.calls[0]["cite"])
		self.assertEqual(answer["answer"][0]["sources"], [0])
		self.assertEqual(answer["sources"][0]["title"], "Reading python files")
		self.assertTrue(answer["sources"][0]["url"].startswith("/learn/ph9-space/"))

		# the instructor may read the restricted page, but privacy settings keep it away from the provider
		frappe.set_user(self.vip)
		api.ai_ask("python salaries")
		self.assertNotIn("Secret python salaries", self.sent_titles())
		self.configure(exclude_restricted=0)
		api.ai_ask("python salaries")
		self.assertIn("Secret python salaries", self.sent_titles())

	def test_no_sources_means_no_model_call(self):
		frappe.set_user(self.learner)
		answer = api.ai_ask("kubernetes helm charts")
		self.assertEqual(answer["sources"], [])
		self.assertEqual(FakeProvider.calls, [])
		self.assertEqual(frappe.db.count("TCD AI Usage Log"), 0)

	def test_log_cost_privacy(self):
		frappe.set_user(self.learner)
		FakeProvider.reply = result()
		api.ai_ask("python files: mail me at someone@example.com or +20 100 123 4567")
		prompt = FakeProvider.calls[0]["prompt"]
		self.assertNotIn("someone@example.com", prompt)
		self.assertNotIn("123 4567", prompt)
		self.assertIn("[email]", prompt)
		self.assertNotIn(self.learner, json.dumps(FakeProvider.calls[0]))  # only a hash leaves the site
		frappe.set_user("Administrator")
		log = frappe.get_doc("TCD AI Usage Log", {"user": self.learner})
		self.assertEqual((log.status, log.input_tokens, log.output_tokens), ("Success", 1000, 500))
		self.assertAlmostEqual(log.cost, 0.014)  # 1000 x $4/M + 500 x $20/M
		self.assertIsNone(log.prompt)  # prompts are not kept unless enabled
		self.assertIn(self.page.name, log.sources)
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD AI Usage Log", "read"))

	def test_limits_and_refusal(self):
		self.configure(daily_requests_per_user=1)
		frappe.set_user(self.learner)
		api.ai_ask("python files")
		with self.assertRaises(ai.AIError):
			api.ai_ask("python files")
		self.configure(daily_requests_per_user=0, monthly_budget=0.01)
		FakeProvider.reply = result()
		api.ai_ask("python files")  # spends $0.014: over the budget from now on
		with self.assertRaises(ai.AIError):
			api.ai_ask("python files")
		self.configure(monthly_budget=0)
		FakeProvider.reply = result(stop_reason="refusal")
		with self.assertRaises(ai.AIError):
			api.ai_ask("python files")
		self.assertEqual(
			frappe.get_all(
				"TCD AI Usage Log", filters={"status": "Refused"}, pluck="user", ignore_permissions=True
			),
			[self.learner],
		)

	# ------------------------------------------------------------ features

	def test_semantic_search(self):
		self.configure(expand_queries=1)
		FakeProvider.reply = result(data={"keywords": ["files", "open"]})
		frappe.set_user(self.learner)
		found = api.ai_search("how to read data")
		self.assertEqual(found["keywords"], ["files", "open"])
		self.assertEqual([r["title"] for r in found["results"]], ["Reading python files"])
		self.assertEqual(FakeProvider.calls[0]["documents"], [])  # only the query is sent
		self.configure(enabled=0)  # without AI: plain lexical search, no call
		FakeProvider.calls.clear()
		self.assertEqual(len(api.ai_search("python files")["results"]), 1)
		self.assertEqual(FakeProvider.calls, [])

	def test_summary(self):
		FakeProvider.reply = result(text="- reads files")
		frappe.set_user(self.learner)
		self.assertEqual(api.ai_summarize(self.page.name)["summary"], "- reads files")
		for hidden in (self.secret.name, self.draft.name):
			with self.assertRaises(frappe.PermissionError):
				api.ai_summarize(hidden)

	def test_generated_questions_need_review(self):
		FakeProvider.reply = result(
			data={
				"questions": [
					{
						"question": "What reads a file?",
						"options": ["open()", "print()"],
						"correct": 1,
						"explanation": "x",
					},
					{"question": "Pick one", "options": ["a", "b", "c"], "correct": 3, "explanation": ""},
					{"question": "Broken", "options": ["a", "b"], "correct": 7, "explanation": ""},
				]
			}
		)
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.ai_generate_questions(self.page.name, 3)
		frappe.set_user(self.author)
		names = api.ai_generate_questions(self.page.name, 3)
		self.assertEqual(len(names), 2)  # the broken one is skipped
		q = frappe.get_doc("TCD Question", names[0])
		self.assertEqual((q.ai_status, q.ai_source, q.correct_answers), ("Needs Review", self.page.name, "1"))

		quiz = {
			"doctype": "TCD Quiz",
			"title": "AI quiz",
			"content": self.page.name,
			"pass_percentage": 50,
			"bank_items": [{"question": names[0]}],
		}
		frappe.set_user("Administrator")
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(dict(quiz)).insert()
		frappe.db.set_value("TCD Question", names[0], "ai_status", "Reviewed")
		self.assertTrue(frappe.get_doc(dict(quiz)).insert().name)

	def test_lesson_draft(self):
		FakeProvider.reply = result(
			data={
				"summary": "How to read files",
				"blocks": [
					{"type": "heading", "text": "Opening files", "language": "", "items": []},
					{"type": "paragraph", "text": "Use open().", "language": "", "items": []},
					{"type": "code", "text": "open('a.txt').read()", "language": "python", "items": []},
					{"type": "list", "text": "", "language": "", "items": ["read", "", "close"]},
					{"type": "paragraph", "text": "", "language": "", "items": []},
				],
			}
		)
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.ai_draft_lesson(self.space, "Files")
		frappe.set_user(self.author)
		with self.assertRaises(frappe.PermissionError):
			api.ai_draft_lesson(self.space, "Files", sources=[self.secret.name])
		name = api.ai_draft_lesson(self.space, "Files", "basics", sources=json.dumps([self.page.name]))
		doc = frappe.get_doc("TCD Content", name)
		self.assertEqual((doc.status, doc.ai_generated, doc.content_type), ("Draft", 1, "Lesson"))
		blocks = json.loads(doc.blocks)
		self.assertEqual([b["type"] for b in blocks], ["heading", "paragraph", "code", "list"])
		self.assertEqual(blocks[3]["items"], ["read", "close"])
		self.assertEqual(self.sent_titles(), ["Reading python files"])
		log = frappe.get_all(
			"TCD AI Usage Log",
			filters={"feature": "Lesson Draft"},
			fields=["reference_name"],
			ignore_permissions=True,
		)
		self.assertEqual(log[0].reference_name, name)

	def test_portal_box(self):
		status, html, _ = render("/learn", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-assistant-form", html)
		self.configure(enabled=0)
		_, html, _ = render("/learn", self.learner)
		self.assertNotIn("tcd-assistant-form", html)

	# ------------------------------------------------------------ Anthropic adapter (SDK mocked: no network)

	def test_anthropic_adapter_request(self):
		settings = frappe.get_single("TCD AI Settings")
		provider = ai.AnthropicProvider(settings)
		with self.assertRaises(ai.AIError):
			provider.complete(system="s", prompt="p", max_tokens=100, effort="low", user_hash="h")  # no key
		self.assertIn("API", frappe.local.message_log[-1]["message"])  # shown as a message, not a traceback

		settings.api_key = "sk-test"
		settings.save()
		settings = frappe.get_single("TCD AI Settings")
		response = SimpleNamespace(
			model="claude-opus-5-5",
			stop_reason="end_turn",
			usage=SimpleNamespace(
				input_tokens=10, output_tokens=5, cache_creation_input_tokens=2, cache_read_input_tokens=None
			),
			content=[
				SimpleNamespace(type="thinking", thinking=""),
				SimpleNamespace(
					type="text", text="Use open()", citations=[SimpleNamespace(document_index=0)]
				),
				SimpleNamespace(type="text", text=".", citations=None),
			],
		)
		fake_sdk = MagicMock()
		fake_sdk.Anthropic.return_value.beta.messages.create.return_value = response
		with patch.dict(sys.modules, {"anthropic": fake_sdk}):
			out = ai.AnthropicProvider(settings).complete(
				system="sys",
				prompt="q",
				documents=[{"title": "T", "text": "body"}],
				cite=True,
				schema=None,
				max_tokens=100,
				effort="low",
				user_hash="abc",
			)
		kwargs = fake_sdk.Anthropic.return_value.beta.messages.create.call_args.kwargs
		self.assertEqual(fake_sdk.Anthropic.call_args.kwargs["api_key"], "sk-test")
		self.assertEqual(kwargs["model"], "claude-opus-5-5")
		self.assertEqual(kwargs["fallbacks"], "default")
		self.assertEqual(kwargs["output_config"], {"effort": "low"})
		self.assertEqual(kwargs["metadata"], {"user_id": "abc"})
		doc_block, text_block = kwargs["messages"][0]["content"]
		self.assertEqual(doc_block["source"], {"type": "text", "media_type": "text/plain", "data": "body"})
		self.assertEqual(doc_block["citations"], {"enabled": True})
		self.assertEqual(text_block, {"type": "text", "text": "q"})
		self.assertEqual((out.text, out.input_tokens, out.output_tokens), ("Use open().", 12, 5))
		self.assertEqual(out.segments[0]["sources"], [0])
