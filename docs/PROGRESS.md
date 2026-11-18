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
| Phase 1 — LMS core | this commit | 75 | Batch, instructors, enrolled-only access, lesson types + media blocks, assignments with grading, course rating, My Learning + instructor dashboards |

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

## Pending

Phase 2 (unified experience), then the MVP gate; Phases 3–11 after (see PLAN.md).

## Blocked / needs decision

- None.
