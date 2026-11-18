# VintraXo T-C-D — Execution Plan

**Product:** VintraXo T-C-D (Training, Content & Documentation) — "Learn. Practice. Build. Document."
**One platform, three equal pillars, one unified experience:**
- **W3Schools pillar:** interactive tutorials, references, Try-it, playgrounds, exercises, quizzes, projects.
- **Wiki pillar:** knowledge spaces, page trees, articles, versions, approvals, policies/SOPs.
- **LMS pillar:** courses, chapters, lessons, paths, enrollment, batches, assignments, assessments, certificates.

Vision reference (full scope, long-form): `docs/VISION.md`. This file is the operative plan.

---

## 0. Ground rules (apply to every phase)

**Environment**
- Repo: `~/frappe-bench/apps/vintraxo_tcd`, branch `vintraxo`. Site: `tcd.localhost` ONLY.
- Frappe v16 (Python 3.14, Node 24, MariaDB 11.8). Do not touch other sites/apps on this bench.
- Do not run `bench compile-po-to-mo`. Do not modify Frappe/ERPNext/HRMS core.
- The app must install on a site WITHOUT ERPNext. Any ERPNext/HRMS link must be guarded.

**Working method**
1. Before each phase, AUDIT the repo: list what already exists for that phase and what is missing. Never rebuild existing parts; extend them.
2. Update `docs/DATA_MODEL.md`, `docs/PERMISSIONS.md`, and add an ADR in `docs/adr/` for any important decision.
3. Implement: DocTypes, controllers, services in `vintraxo_tcd/core/`, thin whitelisted API in `api.py`, portal pages and Desk UI.
4. Permissions: extend `core/permissions.py`. Layers may only RESTRICT; never grant more than Frappe role permissions.
5. Arabic first (RTL) + English: update `translations/ar.csv` using the TCD contexts. Code blocks stay LTR inside RTL text.
6. Tests: unit + permission tests for every important feature.
7. Quality gate (all must pass): `uvx ruff@0.14.0 check` + `format`, `node --check` on JS, `bench --site tcd.localhost migrate`, `bench --site tcd.localhost run-tests --app vintraxo_tcd`.
8. Verify the screens manually in Chromium (RTL, Arabic labels, mobile width).
9. Commit: `feat: <phase name>`. Keep `docs/PROGRESS.md` updated (completed / pending / blocked).
10. **STOP** and report in Arabic: what was built, test count, how to verify, risks, and decisions that need me. Wait for my "go" before the next phase.

**Honesty rules**
- Never invent Frappe APIs/hooks; verify against the installed source.
- Never say something is done/tested unless it actually ran and passed.
- If a requirement is unclear, ask only the essential question. If a better design exists, explain the alternative before changing the approved design.

**Security (non-negotiable)**
- Untrusted user code never runs on the Frappe server. Playgrounds run in the browser (sandboxed iframe, Pyodide, SQLite WASM). A server-side sandbox is OUT OF SCOPE unless I approve an isolated security design first.
- Sanitize block content on save and on render (XSS). Validate uploads. Every API checks permissions.
- AI retrieval is permission-filtered BEFORE the model call.

---

## 2. Phases

### Phase 0 — Cleanup (small)
- Arabic DocType labels without the "TCD" prefix (avoids RTL ordering glitches). Fix the truncated Content shortcut and translate the "Published" badge.
- Delete the demo-author password file in `/tmp`. Document that `tcd.localhost` has the setup wizard marked complete.
- Create `docs/VISION.md`, `docs/PROGRESS.md`, `docs/adr/`.

### Phase 1 — LMS core
- DocTypes: TCD Course, TCD Chapter, TCD Learning Path, TCD Learning Item (child), TCD Enrollment, TCD Batch (student groups), instructor assignment.
- REUSE the existing lesson entity (no duplicate lesson DocType). Lesson types: Article, Video, Interactive Tutorial, Playground, Quiz, Assignment, External, Project, Document.
- Assignments: TCD Assignment + TCD Assignment Submission (file/text), manual grading with feedback.
- Completion rules: all items, required sequence, minimum score, manual approval. Progress rolls up lesson → chapter → course → path.
- Course feedback/rating. Learner "My Learning" and Instructor dashboards (portal + report).
- Permissions: enrollment-based access (enrolled learners, instructors of the course, admins).

### Phase 2 — Unified experience (the three pillars connect)
- Unified content viewer + navigation across wiki pages, tutorials, courses, references.
- Cross-pillar relations used in the UI: Wiki ↔ Tutorial ↔ Reference ↔ Course ↔ Path (no content duplication).
- Unified search covering all content types and courses (keep Arabic-normalized, permission-filtered).
- Unified learner dashboard (progress across everything), prerequisites enforcement, simple recommendations.
- **After this phase: MVP GATE.** Prepare a short test script for 5 real users and STOP. I will run it and bring feedback before Phase 3.

### Phase 3 — Wiki completion
- Audit vs requirements, then add what's missing: page tree/sidebar, tags, article templates, Markdown support, revision comparison and restore previous version, internal links, related articles, feedback/ratings, archiving.
- Approval Workflow (Draft → In Review → Approved → Published → Archived) with Frappe Workflow, if not already complete.

### Phase 4 — Assessment engine (full)
- Question Bank, categories, all question types (single/multiple, true/false, fill blank, matching, ordering, short answer, essay, code/SQL by test cases, file submission, scenario).
- Randomization, weighted scoring, time limit, attempt limit, passing score, manual grading with rubrics, results + feedback, assessment analytics.
- Server-side grading for objective types; code/SQL exercises are validated in the browser runtime or by stored test cases, never executed on the server.

### Phase 5 — Skills and Certificates
- Skills library, user skills, competency matrix and gap report.
- TCD Certificate: PDF print format, verification code, public verification page, expiry/renewal. Issued automatically on path/course completion.

### Phase 6 — Governance
- TCD Document, TCD Policy, TCD SOP with lifecycle (Draft / Review / Approval / Active / Revision / Archived), effective and expiry dates.
- Scheduled review reminders (scheduler), mandatory Acknowledgment with audit log (who / when / which version), non-acknowledged report, links SOP ↔ Tutorial/Course.
- Department-based access (guarded: works without HRMS).

### Phase 7 — Notifications and analytics
- Frappe Notifications: review requests, enrollment, deadlines, certificate issued, acknowledgment due.
- Dashboards/reports: course, learner, instructor, knowledge usage, compliance.

### Phase 8 — Integrations (guarded, no core changes)
- Integration layer: connector registry, webhooks, event mapping, logs, retry, rate limits.
- HRMS: Employee ↔ learner, automatic enrollment and mandatory training by role/department, training compliance.
- ERPNext: tutorials by user role, process guides. Add the `company` Link here, only if ERPNext is installed.

### Phase 9 — AI Gateway
- Provider-agnostic (provider, model, token and cost limits, usage logging, privacy controls).
- Permission-filtered retrieval before the model call; every answer cites its sources.
- Features in order: semantic search, knowledge assistant, summarization, quiz generator, lesson drafts. AI output is saved as Draft and needs human review.

### Phase 10 — Advanced playgrounds (REQUIRES explicit approval)
- Before any code: present a written isolation design (containers, resource/time limits, no network to company data, logs, cleanup). Wait for approval.

### Phase 11 — Hardening and release
- Security review (XSS on blocks, uploads, API permissions, data isolation), performance (indexes, caching, search), load test.
- Migration patches, install on a clean site, backup/restore test, Arabic/RTL pass, full docs (user, admin, developer, deployment, upgrade), release notes.

---

## 3. Report format after each phase

1. What was built (DocTypes, screens, APIs).
2. Test results (total count, new tests).
3. How to verify it manually (steps).
4. Risks / decisions needed.
5. Next phase.
