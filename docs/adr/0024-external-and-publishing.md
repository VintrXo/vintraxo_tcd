# ADR-0024: Visitors, online meetings, payments, SCORM, GitHub sync, profiles and internal jobs

- Status: Accepted (owner: build everything found missing compared with Frappe LMS / Wiki)
- Date: 2026-11-20

## Decision
- **Visitors (off by default):** Guest gets read permission on spaces, categories, pages, courses, paths and
  chapters, but the TCD permission layer returns rows only when "Allow Visitors" is on, the page is published and
  Public in a Public space, and the request is a portal page render — every `/api/` request from a visitor gets
  nothing (records with owner e-mails never leave through REST). Quizzes, progress, notes, discussions, enrollment
  and all personal pages stay login-only; nothing is written for visitors.
- **Online meetings:** Zoom Server-to-Server OAuth creates / moves / deletes the meeting with the session (host
  link for instructors only); Google Meet goes through Frappe's Google Calendar integration (an Event with video
  conferencing; the Meet link is copied hourly or read when the session is shown). Failures never block the session.
- **Payments:** paid courses / paths with coupons; checkout through the Frappe Payments app with TCD Payment as the
  reference document, whose `on_payment_authorized` enrolls once. 100% coupons need no gateway. Outside redirects
  are refused. Admin enrollment never asks for payment. Without the Payments app: a clear message.
- **SCORM (off by default):** packages run on this origin (required by the SCORM API) with the learner's session,
  so only administrators upload them; the zip is checked before extraction (path escapes, size, file count) and the
  manifest parsed with defusedxml; only `cmi.*` values are stored (size-capped).
- **GitHub sync:** per-space repository / branch / folder / token; push writes Markdown with front matter (skips
  unchanged); pull creates Draft pages or suggested edits — never a direct overwrite. Administrators only.
- **Profiles and internal jobs:** private profiles unless shared with colleagues; job openings with required
  skills and a match percentage from earned skills; applications (note + private CV) visible to admins and the
  job's hiring manager only.

## Consequences
External services (Zoom, Google, payment gateways, GitHub) are tested with their APIs mocked; real use needs the
owner's credentials.
