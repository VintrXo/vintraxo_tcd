# ADR-0016: Standard Notifications where possible, code only for data-driven recipients

- Status: Accepted
- Date: 2026-11-19

## Context
PLAN Phase 7 asks for notifications (review requests, enrollment, deadlines, certificate issued, acknowledgment
due) and course / learner / instructor / knowledge usage / compliance analytics.

## Decision
- Events with fixed recipients (a role or a field on the document) ship as standard `Notification` records in the
  module folder, channel **System Notification** (works without an e-mail account). Admins can add an Email channel
  or edit text without code.
- Recipients that depend on data (instructors of a course, the audience of a policy) are notified from
  `core/notify.py` with `enqueue_create_notification` and `dedupe_on`, so repeated events never spam.
- "Knowledge usage" counts unique readers from `TCD Progress` (no raw page-view log is kept; privacy and table size).
- Workspace number cards use standard Number Card records; the compliance percentage uses a whitelisted method card.

## Consequences
- Notification wording is translatable and editable in the Desk.
- Page-view totals are "unique learners", not hits; a view log can be added later if needed.
