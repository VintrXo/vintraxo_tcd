# Progress

Status of [PLAN.md](PLAN.md). Updated at the end of every phase. Test counts are from
`bench --site tcd.localhost run-tests --app vintraxo_tcd` at the commit listed.

## Environment notes

- Development site: `tcd.localhost` (Frappe v16.33.1, only `frappe` + `vintraxo_tcd` installed).
- **Setup wizard was skipped on tcd.localhost**: `Installed Application(frappe).is_setup_complete` was set to 1 by hand
  so the Desk would open (Frappe only checks the `frappe`/`erpnext` rows). Timezone, currency and system defaults
  were never configured through the wizard. Revert by setting the flag back to 0.
- `erpnext.localhost` also has the app installed (before the "tcd.localhost only" rule) at an older migration; it is
  no longer updated.
- PDF: `tcd.localhost` is not resolvable by the system resolver, so `wkhtmltopdf` fails for every document on this
  site (also core ones). The certificate print format uses Frappe's Chrome PDF generator (A4 landscape via
  `page-width`/`page-height` in `.print-format`). Fix for wkhtmltopdf: add `127.0.0.1 tcd.localhost` to `/etc/hosts`.
- Arabic `.po` files of Frappe/ERPNext are not compiled on this bench (`bench compile-po-to-mo` is not run by decision),
  so the app ships its own `translations/ar.csv` (see ADR-0004).
- Browser checks: Administrator password on tcd.localhost was set by the owner's instruction (2026-11-19); Desk and
  portal are checked in headless Chromium as Administrator. Learner views are checked by server-side rendering as the
  learner (changes rolled back).

## Completed

| Phase | Commit | Tests | Summary |
|---|---|---|---|
| Foundation (old P0–P2) | 68ebfb3 | 30 | Roles, settings, spaces, categories, content + blocks + review workflow + versions, relations, tutorials, progress, quizzes |
| Portal (old P3) | b7a49d8 | 39 | /learn pages, RTL, browser playgrounds (Pyodide, sql.js, JS, HTML) |
| Authoring (old P4) | 75dc8aa | 48 | Desk block editor, progress + quiz analytics reports, ranked search, Arabic desk |
| Desk polish | f8bddb7 … 4d16f87 | 48 | VX icon, workspace, sidebar, navbar link, real 404 |
| Phase 0 — cleanup | e553fd6 + this commit | 52 | Arabic names without TCD, short labels, translated badge, translation coverage test, VISION/PROGRESS/ADR docs |
| Phase 1 (partial, previous plan) | 648097e | 65 | Course, Chapter, Learning Path, Learning Item, Enrollment, Student Group, 4 completion rules, roll-up, course/path portal pages |
| Phase 1 — LMS core | 46af804 | 75 | Batch, instructors, enrolled-only access, lesson types + media blocks, assignments with grading, course rating, My Learning + instructor dashboards |
| Phase 2 — Unified experience | c74a3b4 | 83 | Cross-pillar relations, prerequisites, course navigation, unified search, recommendations, MVP test script |
| Phase 3 — Wiki completion | bbbbb24 | 91 | Page tree, tags, templates, Markdown, [[links]] + backlinks, version compare/restore, page feedback, archive banner |
| Phase 4 — Assessment engine | 808a9a8 | 97 | Question bank, 11 question types, papers, time limits, manual review with rubrics |
| Phase 5 — Skills and certificates | fb009c3 | 106 | Skills, competency gap, certificates with PDF, public verification, expiry/renewal |
| Phase 6 — Governance | 2a150a2 | 112 | Policies/SOPs/documents, versions, acknowledgments, reminders, compliance report |
| Phase 7 — Notifications and analytics | 4cdc2a9 | 118 | 7 standard notifications, data-driven notifications, 3 reports, workspace number cards |

## Phase 1 — LMS core: status

| Requirement | State |
|---|---|
| TCD Course, TCD Chapter, TCD Learning Path, TCD Learning Item, TCD Enrollment | Done |
| TCD Batch | Done (renamed from TCD Student Group, ADR-0007) |
| Instructor assignment | Done (`instructors` on course and path) |
| Reuse lesson entity; lesson types | Done (`lesson_type`; video, link and file blocks, ADR-0009) |
| TCD Assignment + Submission, manual grading, feedback | Done (Graded / Returned, private uploads, late flag) |
| Completion rules + roll-up | Done (required assignments also gate completion) |
| Course feedback / rating | Done (TCD Course Feedback) |
| My Learning + Instructor dashboards (portal + report) | Done (/learn/my, /learn/instructor, TCD Instructor Dashboard) |
| Enrollment-based access | Done (course access Enrolled Only + instructor scope, ADR-0008) |

Not verified: actual YouTube/Vimeo playback (headless Chromium shows the embed with the right URL but does not play it).

## Phase 2 — Unified experience: status

| Requirement | State |
|---|---|
| Unified viewer + navigation | Done: one viewer; course prev/next with ?course=; breadcrumbs through tutorial/course |
| Cross-pillar relations in the UI | Done: relations to content/course/path; "Prerequisites", "Up next", "Related", "Referenced by", "Part of" (ADR-0010) |
| Unified search | Done: content + courses + paths, type and space filters, Arabic-normalized, permission-filtered (ADR-0011) |
| Unified learner dashboard | Done: /learn/my with courses, tutorials, recently completed, assignments, recommendations |
| Prerequisites enforcement | Done: content (completion) and course (self-enrollment); staff warned, not blocked |
| Simple recommendations | Done: continue / follow-up / popular |

**MVP GATE:** test script in [MVP_TEST_SCRIPT.md](MVP_TEST_SCRIPT.md). **Postponed by the owner on 2026-11-19**: continue with Phases 3–9 and 11, run the user test afterwards. Phase 10 still needs explicit approval of an isolation design.

## Phase 3 — Wiki: audit result

| Requirement | State |
|---|---|
| Page tree / sidebar | Done: `parent_content`, tree on the space page, ancestor breadcrumbs, child pages |
| Tags | Done: Frappe native tags, chips on pages, `/learn?tag=` |
| Article templates | Done: TCD Content Template + "Apply Template" in the editor |
| Markdown | Done: `markdown` block, sanitized server-side |
| Revision comparison / restore | Done: compare any two versions or version vs current; restore as Draft |
| Internal links / related articles | Done: `[[slug]]`, "Linked from" backlinks; related via Phase 2 relations |
| Feedback / ratings | Done: "Was this page helpful?" (TCD Content Feedback) |
| Archiving | Existing status; archive banner for staff; hidden from learners |
| Approval workflow | Existing controller workflow kept (ADR-0012) |

## Phase 4 — Assessment engine: status

| Requirement | State |
|---|---|
| Question bank + categories | Done (TCD Question, TCD Question Category) |
| Types: single/multiple, true/false, fill blank, matching, ordering, short answer, essay, code, SQL, file, scenario | Done (scenario = context text on any type) |
| Randomization | Done: shuffle questions and options, random picks per category, fixed paper per attempt |
| Weighted scoring, time limit, attempt limit, passing score | Done (time limit enforced on the server with 60 s grace) |
| Manual grading with rubrics, results + feedback | Done (Pending Review, rubric dialog in Desk, per-question feedback) |
| Assessment analytics | Done (report handles bank questions; pending items excluded) |
| Code/SQL never executed on the server | Done: browser runtime; integrity limitation documented (ADR-0013) |

Verified in Chromium: a mixed quiz (fill blank, matching, ordering, Python, SQL, essay) taken end to end; Python ran in
Pyodide and SQL in sql.js inside the sandbox, essay went to review, rubric dialog opened.

## Phase 5 — Skills and certificates: status

| Requirement | State |
|---|---|
| Skills library, user skills | Done (levels 1–5, highest kept, manual awards by admins) |
| Competency matrix + gap report | Done (profiles per Role, TCD Competency Gap report with suggested courses) |
| Certificate PDF print format | Done (Arabic, RTL, A4 landscape, embedded logo; verified by rendering the PDF) |
| Verification code + public page | Done (`/verify/<code>`, 16-char random code, minimal facts) |
| Expiry / renewal | Done (daily scheduler expiry; instructor renewal issues a new certificate, old one Renewed; admin revoke) |
| Issued automatically on completion | Done (course and path, also after manual approval) |

## Phase 6 — Governance: status

| Requirement | State |
|---|---|
| Document / Policy / SOP with lifecycle, effective and expiry dates | Done (one DocType with a kind, ADR-0015) |
| Scheduled review reminders | Done (daily: ToDo for the owner 7 days before review; expiry moves to Revision) |
| Mandatory acknowledgment with audit log (who / when / version) | Done (append-only TCD Acknowledgment, new version = new acknowledgment) |
| Non-acknowledged report | Done (TCD Acknowledgment Status) |
| Links SOP ↔ tutorial/course | Done (both directions in the portal) |
| Department-based access (guarded) | Done (uses ERPNext Employee.department when installed; ignored otherwise) |

Bug found and fixed in this phase: Frappe's `<` filter treats NULL dates as old dates, so the daily jobs would have
expired every policy and certificate without an expiry date. Both jobs now filter with `is set`; regression tests added.
| Phase 8 — Integrations | 483639f | 129 | Connector registry, signed webhooks with outbox/retry/rate limit, training rules (auto/mandatory enrollment by role and HR), role guides, training compliance |
| Phase 9 — AI gateway | d02dc01 | 140 | Provider-agnostic gateway (Anthropic built in), limits/budget/usage log/privacy, permission-filtered retrieval, cited assistant, smart search, summaries, reviewed question and lesson drafts |
| Phase 11 — Hardening and release | 4accf76 | 146 | Security review + tests, code-answer review option, indexes, load test, backup check, Arabic/RTL pass, user/admin/developer/deployment docs, release notes |
| Phase 10 — Code runner (Frappe side) | 4defe64 | 154 | Judge0 client, run log, practice runs for Java/C++/C/Go/C#/Bash, server grading that ignores device output, Test Runner; runner host not set up |
| Phase 12 — Gaps from the vision review | c931dd8 | 167 | Sessions + attendance + calendar, lesson discussions, content review cycle + freshness report, self-withdraw; fixes: Jinja date crash, withdrawn re-enroll, 12-hour stale JS, unsaved setting defaults |

## Phase 7 — Notifications and analytics: status

| Requirement | State |
|---|---|
| Review requests, enrollment, deadlines, certificate issued, acknowledgment due | Done (7 standard Notifications + data-driven ones in `core/notify.py`, ADR-0016) |
| Course, learner, instructor, knowledge usage, compliance analytics | Done (TCD Course Report, TCD Knowledge Usage, TCD Compliance Overview + earlier reports, number cards) |
| Learners see their notifications | Done (section in /learn/my) |

Found while testing: standard notifications with a `.md` template failed silently (Frappe converts Markdown to HTML
before rendering Jinja). Templates are HTML now.

## Phase 11 — Hardening and release: status

| Requirement | State |
|---|---|
| Security review: XSS on blocks | Done: Markdown sanitized, inline links escaped; stored `html` keys dropped on save and ignored on render (test) |
| Security review: uploads | Done earlier (Phase 1: extension/size validation, private files); unchanged |
| Security review: API permissions | Done: only `verify_certificate` is open to guests; all other 40+ endpoints refuse guests (test) |
| Security review: data isolation | Done: a learner sees only own progress, enrollments, submissions, certificates, skills, acknowledgments; no access to connectors, outbox, AI settings/log (test) |
| Finding: code answers graded on device output | Fixed as an option: "Instructor Reviews Code Answers" on the quiz (full fix needs Phase 10) |
| Performance: indexes | Added on outbox (status, connector, next_attempt_on), AI log (user), content (slug, parent_content), learning item (content, course) |
| Load test | Done on `bench serve`: 1 worker p50 75 ms / p95 174 ms; 20 workers ~10.5 req/s (dev server is single-process), search API p50 311 ms. 1–1.5% of requests failed with a Frappe core router error (`get_dynamic_web_pages` returned None) that also happens on `/login` — Frappe core + dev server, not this app; not changed (core rule). Production (gunicorn) load test not run |
| Migration patches | Reviewed: new fields need no data patch; existing patches unchanged |
| Install on a clean site / restore test | Not run: needs a second site and the rule is tcd.localhost only. Backup verified (gzip OK, all 48 TCD tables with data). Needs owner OK for a throw-away site |
| Arabic/RTL pass | Done: portal and Desk pages swept in Arabic; fixed Select values / table descriptions that Frappe translates without context (63 plain keys, new test); "Slack" upstream mistranslation overridden |
| Docs | USER_GUIDE (ar), ADMIN_GUIDE (ar), DEVELOPER, DEPLOYMENT (install/upgrade/backup), RELEASE_NOTES |

## Phase 9 — AI gateway: status

| Requirement | State |
|---|---|
| Provider-agnostic: provider, model, token and cost limits, usage logging, privacy controls | Done (TCD AI Settings, `tcd_ai_providers` hook, TCD AI Usage Log, ADR-0018) |
| Permission-filtered retrieval before the model call | Done (get_list as the user + per-page gate; tested with restricted space, draft, Restricted exclusion) |
| Answers cite their sources | Done (document citations → [n] links on /learn) |
| Semantic search | Done as query expansion over the permission-filtered index; vector embeddings not done (no embedding provider chosen) |
| Knowledge assistant, summarization, quiz generator, lesson drafts | Done (portal box; Desk buttons on TCD Content and its list) |
| AI output saved as Draft, human review | Done (lessons Draft + ai_generated; questions Needs Review blocked from quizzes) |
| Live provider check | Not done: no API key on tcd.localhost; adapter tested with the SDK mocked. AI is off by default |

## Phase 8 — Integrations: status

| Requirement | State |
|---|---|
| Connector registry, webhooks, event mapping, logs, retry, rate limits | Done (TCD Connector, TCD Integration Event outbox, HMAC signature, backoff, per-minute limit, SSRF guard, ADR-0017) |
| Employee ↔ learner | Done, guarded (`Employee.user_id`, read only). tcd.localhost has no ERPNext: tested with the HR lookup mocked, not against a real ERPNext site |
| Automatic / mandatory enrollment by role / department | Done (TCD Training Rule: roles + department/designation/company filters, due date, on save / user change / daily) |
| Training compliance | Done (TCD Training Compliance report, mandatory badge on /learn/my) |
| ERPNext tutorials by role, process guides | Done as Content rules → "Guides for your role" on /learn/my |
| `company` as a Link only with ERPNext | Changed: Data field validated against ERPNext when installed (no conditional schema; see ADR-0017) |
| Writing results back into HRMS (Training Event / Result) | Not done: one-way read; can be a connector later |

## Incident 2026-11-19: test run wiped development data

- What happened: test `setUp` methods delete whole TCD tables and relied on the transaction rollback. The Phase 7 test
  for "due soon" notifications called Frappe's `trigger_daily_alerts`, which commits internally. That commit made the
  deletes permanent on tcd.localhost: demo content/courses/quizzes/policies and **all Notification Logs**.
- Evidence of impact: the automatic backup of 2026-11-19 08:30 contained only Administrator-owned demo data in the
  TCD tables and no Notification Logs. Backups: `sites/tcd.localhost/private/backups/`.
- Fix: `tests/base.py` (`TCDTestCase`) makes `frappe.db.commit` a no-op while a TCD test class runs; every test class
  uses it. Verified: a full run (118 tests) left all record counts unchanged.
- Resolution (owner approved option 1): removed only the committed test leftovers (space `ph7-space` and its course,
  content and enrollment, 4 `tcd-*@test.local` users, 9 orphan child rows / relations, 8 notification error logs) and
  rebuilt the demo with `demo.create_demo`. Notification Logs from before the incident are not recoverable (the 08:30
  backup had none).

## Phase 12 — Gaps found against the vision

| Gap | State |
|---|---|
| Instructors run batches, but no sessions / attendance | Done: TCD Session + attendance, calendar, notifications, portal, TCD Attendance report |
| Learners cannot ask about a page | Done: lesson discussions with moderation and best answers |
| Articles and lessons go stale | Done: owner + review cycle, overdue notice, reminders, TCD Content Freshness report |
| Learners cannot leave an optional course | Done: Withdraw (not for mandatory or completed) |
| Found while building | Fixed: `frappe.format_datetime` is not available in Jinja (lesson page and My Learning crashed for assignments with a due date); withdrawn learners saw no Enroll button; portal JS cached 12 hours after updates; new settings read as off on existing sites |

## Pending

All plan phases (0–11) are built. Open items, each waiting for an input from the owner:

| Item | Needs |
|---|---|
| Install on a clean site + restore test | Owner runs `bench new-site tcd-install-test.localhost --install-app vintraxo_tcd` (MariaDB root password) |
| Production deployment (latest v16 on a fresh bench, SSL) + production load test | Server IP / OS / domain |
| Code runner host (Judge0 on an isolated VM) | The production server (or a separate VM) |
| Live AI check | An API key in AI Settings |

Optional, not in the plan: writing training results back into HRMS; vector (embedding) search, which needs an
embedding provider.

## Blocked / needs decision

- Phase 10 runner host: Frappe side built (ADR-0019); the isolated Judge0 VM is to be set up with the production
  server, then enabled in Learning Settings. Until then code runs in the browser (and graded exams can use
  "Instructor Reviews Code Answers").
