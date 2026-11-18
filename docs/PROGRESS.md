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

## Phase 1 — LMS core: audit against PLAN.md

| Requirement | State |
|---|---|
| TCD Course, TCD Chapter, TCD Learning Path, TCD Learning Item, TCD Enrollment | Done (648097e) |
| TCD Batch (student groups) | Exists as **TCD Student Group** — naming decision pending |
| Instructor assignment | Missing (no course ↔ instructor link) |
| Reuse lesson entity | Done (chapters reference TCD Content) |
| Lesson types: Article, Video, Interactive Tutorial, Playground, Quiz, Assignment, External, Project, Document | Partial: content types are Article / Tutorial / Lesson / Reference; no lesson type, no video/external block |
| TCD Assignment + Submission, manual grading, feedback | Missing |
| Completion rules + roll-up lesson → chapter → course → path | Done |
| Course feedback / rating | Missing |
| Learner "My Learning" (portal) | Partial: "My courses" section on /learn |
| Instructor dashboard (portal + report) | Missing |
| Enrollment-based access (enrolled learners, course instructors, admins) | Partial: course access follows space/visibility; no "enrolled only" mode, instructors see all courses they can read |

## Pending

Phase 1 remainder, then Phases 2–11 (see PLAN.md). MVP gate after Phase 2.

## Blocked / needs decision

- Phase 1 remainder: Batch naming, enrollment-only access mode, lesson types (see the report of 2026-11-19).
