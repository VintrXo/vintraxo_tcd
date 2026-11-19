# ADR-0017: Outbox-based integrations and HR-guarded training rules

- Status: Accepted
- Date: 2026-11-20

## Context
PLAN Phase 8 asks for an integration layer (connector registry, webhooks, event mapping, logs, retry, rate limits),
the HRMS/ERPNext link (Employee ↔ learner, automatic and mandatory enrollment by role/department, training
compliance) and ERPNext tutorials by role. The app must still install and work on a site without ERPNext, and no
Frappe/ERPNext/HRMS core may change.

Frappe's own Webhook (`frappe.integrations.doctype.webhook`) was checked in the installed source: it fires on DocType
events, retries 3 times inline with `sleep`, has no rate limit and cannot see TCD business events such as
"enrollment completed" (the roll-up writes with `db_set`, which runs no doc events). It stays available for admins
who want raw DocType webhooks; TCD events use their own outbox.

## Decision
- **Registry:** `TCD Connector` (admins only): endpoint, payload format (JSON or Slack text), subscribed events,
  signing secret (Password field), max attempts, timeout, rate limit per minute.
- **Event mapping:** services call `integrations.emit(<event>, doc)` at the business moment:
  enrollment created / completed, certificate issued / revoked, policy activated / acknowledged.
  Stable wire names (`enrollment.completed`, …) are mapped from translatable labels.
- **Outbox:** each event becomes a `TCD Integration Event` row in the same transaction as the business change; a
  short-queue job sends it after commit; a 5-minute cron job sends what is due. A rolled-back change never sends.
- **Delivery:** `POST` JSON envelope `{id, event, occurred_on, site, data}`; headers `X-TCD-Event`, `X-TCD-Delivery`,
  `X-TCD-Timestamp`, `X-TCD-Signature: sha256=HMAC(secret, "<timestamp>.<body>")`. Redirects are not followed.
- **Retry:** backoff 1, 5, 15, 60, 240, 720 minutes up to `max_attempts`, then Failed; admins can retry.
  A row locked `FOR UPDATE` is sent once even if the job and the cron overlap.
- **Rate limit:** per connector, counted from Sent rows of the last 60 s; over the limit the event waits without
  using an attempt.
- **SSRF guard:** https and public addresses only (hostnames resolved on every send), unless the admin ticks
  "Allow Private Network" for a trusted internal service.
- **Retention:** Sent rows are purged after 30 days; Failed rows stay until an admin deletes them.
- **HR link (guarded):** `training.hr_available()` = the Employee DocType exists. `employee_profile(user)` reads the
  active Employee with `user_id = user`. Nothing is written into ERPNext/HRMS. `doc_events["Employee"]` simply never
  fires on a site without ERPNext.
- **Training rules:** `TCD Training Rule` targets a Course or Learning Path (enrolls, optionally mandatory, with a due
  date) or a Content page (a tutorial / process guide recommended in "Guides for your role"). Audience = roles
  (empty = any learning role) AND HR filters (department, designation, company; same filter OR, different filters
  AND). Applied on rule save (background), on User / Employee save, daily, and by "Apply Now".
  Existing enrollments, including withdrawn ones, are never touched: an admin decision wins over a rule.
- **Department / designation / company are Data fields validated against ERPNext when it is installed**, not Link
  fields: a Link to a DocType that does not exist breaks forms and migrate on sites without ERPNext. This replaces the
  plan's "company Link only when ERPNext is installed" with the same integrity and no conditional schema.
- **Compliance:** `TCD Training Compliance` report (mandatory enrollments per user, completed, overdue, %; employee,
  department and designation columns only when HR is installed).

## Consequences
- Receivers must verify the signature and de-duplicate on `X-TCD-Delivery` (at-least-once delivery).
- An HR rule on a site without ERPNext matches nobody (a warning is shown on save).
- The ERPNext path is covered by tests with the HR lookup mocked; it has not run against a real ERPNext site
  (tcd.localhost has no ERPNext by design).
