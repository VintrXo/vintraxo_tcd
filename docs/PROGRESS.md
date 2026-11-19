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
| Phase 1 — LMS core | 46af804 | 75 | Batch, instructors, enrolled-only access, lesson types + media blocks, assignments with grading, course rating, My Learning + instructor dashboards |
| Phase 2 — Unified experience | c74a3b4 | 83 | Cross-pillar relations, prerequisites, course navigation, unified search, recommendations, MVP test script |
| Phase 3 — Wiki completion | bbbbb24 | 91 | Page tree, tags, templates, Markdown, [[links]] + backlinks, version compare/restore, page feedback, archive banner |
| Phase 4 — Assessment engine | this commit | 97 | Question bank, 11 question types, papers, time limits, manual review with rubrics |

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

## Pending

MVP test with 5 users (owner), then Phases 3–11 (see PLAN.md).

## Blocked / needs decision

- None.
