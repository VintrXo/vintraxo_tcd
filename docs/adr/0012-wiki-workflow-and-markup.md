# ADR-0012: Wiki workflow stays in the controller; links and Markdown rendered server-side

- Status: Accepted
- Date: 2026-11-19

## Context
PLAN Phase 3 suggests Frappe Workflow "if not already complete". The content lifecycle
(Draft → In Review → Approved → Published → Archived) already exists in `core/content.py` with role checks,
the "require approval" setting, version snapshots on approval and locked fields.

## Decision
- Keep the controller-based workflow. A Frappe Workflow on top would duplicate the transitions and could not create
  snapshots or honour the approval setting without the same code. Tests cover every transition.
- Wiki markup: `[[...]]` internal links and a `markdown` block, both rendered on the server. Text is escaped first,
  links are produced only for readable targets, Markdown HTML is sanitized with dangerous tags disallowed.
- Tags use Frappe's native Tag Link instead of a custom field.

## Consequences
- One place for lifecycle rules; no Workflow records to keep in sync.
- No raw HTML from authors ever reaches the page unsanitized.
