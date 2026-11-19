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
- **Playgrounds:** Python, SQL, JavaScript and HTML run in the learner's browser.

## Quality
- 146 automated tests (permissions, XSS, data isolation, guest surface, translations, every feature).
- Full Arabic coverage enforced by tests.

## Known limits
- Server-side code execution (Phase 10) needs an approved isolation design and a separate VM; not included.
- The AI provider and the ERPNext/HRMS path were tested with mocks only on the development site.
- Restore and clean-site installation were not run on the development bench (single-site rule); see `DEPLOYMENT.md`.
