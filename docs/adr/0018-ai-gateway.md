# ADR-0018: One AI gateway, retrieval as the user before the call, AI output as drafts

- Status: Accepted
- Date: 2026-11-20

## Context
PLAN Phase 9: a provider-agnostic AI gateway (provider, model, token and cost limits, usage logging, privacy
controls); retrieval filtered by permissions before the model call; answers cite sources; features in order:
semantic search, knowledge assistant, summarization, quiz generator, lesson drafts; AI output saved as Draft and
reviewed by a person.

## Decision
- **Gateway:** every model call goes through `core/ai.py: gateway()`: AI enabled, user role allowed, daily request
  limit per user, monthly budget (sum of logged cost), then privacy redaction, provider call, `TCD AI Usage Log`
  (tokens, cost from the configured prices, sources, status). Prompt text is kept only if the admin enables it.
- **Providers:** a provider is a class with `complete(system, prompt, documents, cite, schema, max_tokens, effort,
  user_hash)`. Built in: Anthropic through the official `anthropic` SDK (default model `claude-opus-5-5`, effort from
  settings, server-side refusal fallback enabled for models that support it). Other providers are added by any app
  through the `tcd_ai_providers` hook; no provider-specific code outside its class.
- **Retrieval before the call:** candidate pages come from `frappe.get_list` run as the asking user (all permission
  layers apply), then every page passes a second gate (`has_permission` read, Published unless staff, and — with
  "Never Send Restricted Content" — not Restricted and not inside a Restricted space). Only pages that pass are sent.
  The assistant first searches with the plain terms; only if nothing matches is the query (alone) sent for keyword
  expansion. If still no page passes, it answers "not found" without sending any page.
- **Citations:** pages are sent as document blocks with citations enabled; the answer comes back as segments with the
  indexes of the pages they cite, shown as [n] links to the pages.
- **Semantic search:** query expansion — only the query is sent; the model returns keywords, and results come from
  the same permission-filtered index. No vector embeddings (no embedding provider chosen yet).
- **Privacy:** e-mails and phone numbers are removed from prompts and pages; the provider receives a hash instead of
  the user id; restricted content can be excluded completely. Long pages are cut at 12,000 characters each.
- **Drafts:** lesson drafts are inserted as `TCD Content` with status Draft and `ai_generated = 1` (normal permissions
  and block sanitizing apply; publishing still needs the review workflow). Generated questions get
  `ai_status = Needs Review`; a quiz rejects them and category picks skip them until a person marks them Reviewed.
  Invalid generated questions are dropped, never repaired by guessing.

## Consequences
- With AI off (default) nothing changes for users and no data leaves the site.
- Cost is an estimate from configured prices; the monthly budget stops calls after it is reached (the call that
  crosses it still completes).
- Not verified against the live provider on tcd.localhost (no API key configured); the adapter is tested with the
  SDK mocked.
