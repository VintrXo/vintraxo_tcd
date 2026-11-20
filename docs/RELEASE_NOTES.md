# 0.3.1 (fix)
- `defusedxml` is now a declared dependency (it was only present on the internal server through another app). On
  servers where saving a page failed with `No module named 'defusedxml'`: `bench setup requirements --python`, then
  restart. Saving pages no longer loads the SCORM parser at all.

# Release notes — VintraXo T-C-D 0.3.0 (production release)

The release that goes to the real server. Upgrade from 0.2.0 with `bench --site <site> migrate` (no manual steps).

## New since 0.2.0
- **Move kit (`deploy/`):** `export_internal.sh` packs the whole internal server into one private bundle (every app
  at its exact commit, our own apps as they are on disk, local translation edits as patches, full backup with the
  encryption key); `install_prereqs.sh` prepares a fresh Ubuntu 24.04; `setup_server.sh` rebuilds the server from the
  bundle (restore, migrate, production settings, nginx + supervisor, backups, SSL). Guide: `docs/MOVE_TO_SERVER.md`.
- **One keys file:** `keys.json` (from `deploy/keys.example.json`) fills outgoing mail, AI key, Judge0, Zoom / Google
  Meet, payment gateway, GitHub sync, other apps' settings, and disables the trial accounts —
  `bench --site <site> execute vintraxo_tcd.core.server_keys.apply_keys --kwargs "{'path': '...'}"`.
- **Readiness check** warns while the trial accounts are still enabled.

## Quality
- 244 automated tests. All Desk settings of the app live in code (roles, workspace, notifications, print format);
  nothing was customized from the Desk on the internal server.

# 0.2.0

Everything Frappe LMS, Frappe Wiki and W3Schools-style tutorials offer that fits an internal training platform,
in one app. Upgrade from 0.1.0 with `bench --site <site> migrate` (no manual steps).

## New since 0.1.0
- **Learner experience:** new design (light / dark), lesson side menu, previous / next on top, syntax highlighting
  with copy, full-screen "try it yourself", practice exercises with blanks, reference tables with search.
- **Studio (`/learn/studio`):** authors write pages with the block editor and build courses (chapters, items,
  release dates) from the portal; review and publish buttons for reviewers; Markdown toolbar with preview.
- **Courses:** certification evaluations (evaluator schedules, slot booking, results issue certificates),
  chapters released N days after enrollment or on a date, "coming soon" courses with notify-me, prices by country.
- **Batches:** mentors following their batch on My Team, batch feedback, weekly timetable that creates sessions,
  attendance read from Zoom after online sessions.
- **Wiki:** admin-arranged space navigation menu; visitors (optional) can read public pages.
- **Community:** certified learners page (opt-in) with platform statistics, learner profiles, internal job board.
- **Also from 0.1.x:** Zoom / Google Meet sessions, paid courses with coupons (Frappe Payments), SCORM packages,
  GitHub docs sync, video watch tracking, private notes, suggested edits, TOC, course cover and intro video,
  proctoring, negative marking, multiple test cases, badges.
- **Operations:** readiness check (Learning Settings → Readiness check, or `bench execute
  vintraxo_tcd.core.ops.print_readiness`) and a move-to-server guide (`docs/MOVE_TO_SERVER.md`).

## Quality
- 238 automated tests, strict lint, every phase checked in a real browser (desktop, phone, dark mode, RTL).
- Fixes found on the way: portal breadcrumbs now escape page titles; portal script loaded on every learner page.

## Known limits
- Extra code-runner languages need the Judge0 server; the AI assistant needs an API key; Zoom, Google Meet,
  payment gateways and GitHub sync were tested with mocked APIs and need real credentials.
- Prices by country follow the country the learner sets in their profile (a convenience, not a fraud control).

---

# Release notes — VintraXo T-C-D 0.1.0

Training, Content and Documentation in one Frappe app, Arabic-first (RTL), mobile-friendly.

## Highlights
- **Content:** one lesson entity for articles, tutorials, lessons and references; block editor; review workflow
  with versions, compare and restore; wiki tree, tags, templates, Markdown, `[[links]]` and backlinks.
- **Learning:** courses, chapters, learning paths, batches, instructors, four completion rules, prerequisites,
  enrolled-only access, assignments with grading, ratings, My Learning and instructor dashboards.
- **Assessment:** question bank with 11 types, papers, time limits, attempts, manual review with rubrics, and an
  option to have instructors confirm code answers in graded exams.
- **Credentials:** skills, competency gaps, certificates with PDF and public verification, expiry and renewal.
- **Governance:** policies, SOPs and documents with approval, versions, audience, acknowledgments, review reminders.
- **Notifications and analytics:** 7 standard notifications, data-driven ones, 9 reports, workspace cards.
- **Integrations:** signed webhooks (JSON or Slack) with outbox, retries and rate limits; training rules for
  automatic and mandatory enrollment by role and (with ERPNext/HRMS) department, designation and company;
  training compliance report.
- **AI (optional, off by default):** knowledge assistant with cited sources, smart search, summaries, quiz
  questions and lesson drafts that need human review; budget, limits, privacy controls and usage log.
- **Playgrounds:** Python, SQL, JavaScript and HTML run in the learner's browser; with the optional isolated code
  runner (Judge0) also Java, C++, C, Go, C# and Bash, and code questions graded on the server.
- **Sessions:** classroom / online sessions per course or batch, attendance, calendar, minimum attendance rule.
- **People:** manager dashboard (`/learn/team`), lesson discussions, content review cycles, self-withdraw.
- **HRMS:** completed courses recorded as Training Event / Training Result (when HRMS is installed).
- **Portability:** export a space to a file and import it on another site.

## Quality
- 173 automated tests (permissions, XSS, data isolation, guest surface, translations, every feature); CI on every push.
- Full Arabic coverage enforced by tests.

## Known limits
- The code runner host (Judge0 on an isolated VM) is not part of the app; it is set up with the production server.
- The AI provider and the ERPNext/HRMS path were tested with mocks only on the development site.
- CI on GitHub installs the app on a clean site and runs all tests on every push (see the Actions tab); a manual
  restore test is still to be done.
