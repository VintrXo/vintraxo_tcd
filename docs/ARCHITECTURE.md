# ARCHITECTURE

## Target
- Frappe v16 (Python 3.14, Node 24, MariaDB 11.8)
- Modular monolith: one app `vintraxo_tcd`, one module `VintraXo TCD` at first
- Zero core modification: hooks, custom DocTypes and public APIs only

## Layers
1. DocTypes + controllers (business rules)
2. Services in `vintraxo_tcd/core/` (content, progress, search, permissions)
3. Whitelisted API in `api.py` (thin, delegates to services)
4. Desk (authors/admins) and Portal (learners)

## Principles
- Learner-facing vertical slice first: Space > Tutorial > Lesson (blocks) > Playground > Progress > Quiz > Search
- Untrusted code never runs on the Frappe server; MVP playgrounds run in the browser (sandboxed iframe, Pyodide, SQLite WASM)
- Arabic/RTL first: page direction, LTR code inside RTL text, Arabic-normalized search
- Reuse Frappe: Version, Workflow, Notification, Scheduler

## Naming
- DocTypes: `TCD <Name>`; fieldnames snake_case; roles: `TCD <Role>`

## Services (`vintraxo_tcd/core/`)
| Module | Responsibility |
|---|---|
| search.py | Arabic-aware normalization and ranked search (all terms required, title > summary > body, snippets) |
| content.py | Block schema, slugs, search_text, tutorial lessons, review workflow, version snapshots |
| permissions.py | Space/visibility access (has_permission + permission_query_conditions) |
| progress.py | Lesson/tutorial progress and roll-up |
| quiz.py | Quiz validation, attempts (start/resume/deadline), learner payload, grading, manual review |
| governance.py | Policies/SOPs/documents: lifecycle, snapshots, audience, acknowledgments, daily expiry + review reminders |
| notify.py | Data-driven notifications (instructors, policy audiences), deduplicated |
| analytics.py | Course report, knowledge usage, compliance overview, number card methods |
| credentials.py | Skills (award/keep highest), certificates (issue, expire, renew, revoke, verify), competency gaps |
| assessment.py | Question items (inline + bank), papers, payloads without answers, grading per type, rubric points |
| portal.py | Context for /learn pages (login/portal guards, listings, lesson, course, path pages) |
| courses.py | Course/path structure rules, completion rules, roll-up, enrollment, sequence gating |
| assignments.py | Assignment validation, submission, grading, completion |
| media.py | Video/link/file blocks, video host allowlist, upload validation |
| dashboards.py | My Learning and instructor dashboard data |
| wiki.py | Internal links, Markdown (sanitized), page tree, backlinks, version compare/restore, page feedback, tags, templates |
| connect.py | Cross-pillar relations, prerequisites, used-in, course navigation, unified search, recommendations |

## Public API (`vintraxo_tcd.api.*`)
| Method | HTTP | Purpose |
|---|---|---|
| set_content_status(name, status) | POST | Move content through the review workflow |
| search_content(query, space?, limit?) | GET | Normalized search over readable content |
| get_lesson(name, tutorial?) | GET | Blocks, direction, playground config, quiz, progress, prev/next |
| track_view(name) | POST | Mark content In Progress |
| complete_lesson(name) | POST | Complete a lesson (needs a passed required quiz) |
| get_tutorial_progress(name) | GET | Lessons with status and percent |
| get_quiz(name) | GET | Questions without answers, attempts left |
| submit_quiz(name, answers) | POST | Grade on the server; answers = {question_id: [option numbers]} |
| get_course(name) | GET | Outline with completed/locked items, chapter and course percent, enrollment |
| get_learning_path(name) | GET | Courses with state, path percent, enrollment |
| enroll(enrollment_for, name) | POST | Self-enrollment (Course / Learning Path; path also enrolls in its courses) |
| enroll_batch(batch, enrollment_for, name, due_date?) | POST | Instructor of the course: enroll a batch; returns enrolled + skipped with reasons |
| approve_enrollment(name) | POST | Instructor of the course: approve a Pending Approval enrollment |
| get_assignment(name) | GET | Assignment details + the learner's submission |
| submit_assignment(name, answer_text?, attachment?) | POST | Create/update the learner's submission (file must be the learner's own upload) |
| grade_submission(name, action, score?, feedback?) | POST | Instructor of the course: Graded or Returned |
| rate_course(name, rating, comment?) | POST | Enrolled learner: 1-5 rating, one per course |
| search_all(query, types?, space?, limit?) | GET | Unified search over content, courses and paths |
| get_related(name) | GET | Prerequisites (with state), next, related, referenced by, part of |
| get_recommendations(limit?) | GET | Continue / follow-up / popular suggestions |
| compare_versions(old, new) | GET | Diff of two versions or a version and the current content |
| restore_version(name) | POST | Copy a version into the content and move it to Draft |
| content_feedback(name, helpful, comment?) | POST | "Was this page helpful?" |
| get_templates(content_type?) / get_template(name) | GET | Content templates for authors |
| start_quiz(name) | POST | Open/resume a timed or randomized attempt |
| get_review_items(name) / review_quiz_submission(name, reviews) | GET / POST | Manual grading with rubrics |
| get_policy(code) / my_policies() | GET | Approved version for readers (audience-filtered) |
| acknowledge(code) | POST | Append-only acknowledgment of the current version |
| set_governance_status(code, status) | POST | Lifecycle transition (approver may activate without write permission) |
| my_credentials() | GET | The learner's certificates and skills |
| renew_certificate(name) / revoke_certificate(name, reason) | POST | Instructor renews; admin revokes |
| verify_certificate(code) | GET (guest) | Public minimal certificate facts |
| my_learning() / instructor_dashboard() | GET | Dashboard data (also used by /learn/my, /learn/instructor and the TCD Instructor Dashboard report) |

## Learner portal (P3)
| Route | Page | Content |
|---|---|---|
| `/learn` | `www/learn/index` | Spaces, "continue learning", search (`?q=`) |
| `/learn/<space>` | `www/learn/space` | Content grouped by category; tutorials first |
| `/learn/policies[?kind=]` | `www/learn/policies` | Policies, SOPs and documents addressed to the user |
| `/learn/policies/<code>` | `www/learn/policy` | Approved version, related learning, acknowledgment |
| `/verify/<code>` | `www/verify` | Public certificate verification (no login) |
| `/learn/my` | `www/learn/my` | My Learning: enrollments, due/overdue, assignments |
| `/learn/instructor` | `www/learn/instructor` | Instructor dashboard: courses, approvals, grading queue |
| `/learn/<space>/course/<slug>` | `www/learn/course` | Outline, progress, enroll button, locked items |
| `/learn/<space>/path/<slug>` | `www/learn/path` | Courses of the path with state |
| `/learn/<space>/<slug>[?tutorial=&course=]` | `www/learn/content` | Blocks, tutorial lessons, quiz, complete button, prev/next |

- Guests get a 302 to `/login?redirect-to=...`; `TCD Settings > Enable Learner Portal` off = 404.
- Hidden spaces/content return 404 (never 403) so their existence is not revealed. Staff see a preview banner on unpublished content.
- Blocks are rendered server-side (`templates/includes/tcd_blocks.html`). Frappe www templates are **not autoescaped**:
  every value is escaped with `|e`; JSON for scripts goes through `portal.json_for_script`.
- Page direction follows the content language (`ar` = RTL); code, editors and output are always LTR. CSS uses logical properties only.
- UI strings are translated server-side (`translations/ar.csv`) and passed to JS as a JSON blob.
- Demo content: `bench --site <site> execute vintraxo_tcd.demo.create_demo` (space `demo-python`).

## Playground runtime (`public/js/tcd_playground.js`)
```
page (site origin)
 └─ <iframe sandbox="allow-scripts"> per run   opaque origin: no cookies, no DOM/API access as the learner
     └─ Web Worker (blob)                       python: Pyodide | sql: sql.js | javascript: plain worker
```
- Time limit (`playground_timeout_seconds`) starts after the runtime loads; the worker is terminated on timeout and the parent
  removes the iframe as a last resort (timeout + 90 s load grace). Stop button kills it immediately.
- `html` blocks render as a preview in a sandboxed iframe (`allow-scripts` only).
- Runtimes load from `TCD Settings > Pyodide Base URL / SQL.js Base URL` (pinned CDN versions by default; set a `/assets/...`
  path to self-host for offline sites). Output is capped at 100k characters; SQL tables at 500 rows.
- `window.TCDPlayground.run(language, code, {setup})` runs code headless in the same sandbox (used by code/SQL quiz
  questions; output is sent to the server for comparison, see ADR-0013).
- Verified in headless Chromium: JS/Python infinite loops are killed, `fetch` to the site from the sandbox is blocked
  (origin `null`), HTML preview cannot touch the parent page.

## Authoring and instructor tools (P4)
- **Block editor** (`tcd_content.js`): visual editor for `blocks` (add, edit, move, copy, delete), synced to the JSON field,
  which stays available under "Blocks JSON (advanced)". Locked (read-only) for Approved/Published content.
  Status group buttons call `api.set_content_status` (Submit for Review, Approve, Publish, Archive, Back to Draft);
  "View in Portal" and "Approved Version" shortcuts. Flags come from `TCDContent.onload`.
- **Reports** (Instructor, Reviewer, Administrator; permission-aware via `get_list`):
  - TCD Learner Progress: progress per learner and content, best quiz score, attempts; completion summary and chart.
  - TCD Quiz Analytics: per-question correct rate and most common wrong answer, attempts, pass rate, average score.
    Uses `TCD Quiz Submission.results` (correctness stored at grading time), so editing the answer key later does not
    rewrite history.
- **Search**: every term must match; ranking = exact/phrase title > title word > title prefix > summary > body frequency;
  LIKE wildcards in the query are escaped. Used by `api.search_content` and the portal.

## Translations
`translations/ar.csv` (no compile step). App translations are global, so:
- app-specific strings use plain keys;
- generic words (Title, Status, Published...) are translated with a **context**: the DocType name for desk labels and
  select options (Frappe passes it automatically), `TCD Block` for editor labels, `TCD` for statuses/types in the portal
  and reports. This keeps our wording without changing other apps' screens.
- Frappe/ERPNext Arabic `.po` files are only active after `bench compile-po-to-mo` (not run on this bench by decision).
- DocType/report names are translated without the "TCD" prefix (e.g. TCD Content = محتوى تعليمي).
- `tests/test_translations.py` fails the build when any DocType name, report name, field label, description or
  Select option lacks Arabic, or when Arabic text still contains "TCD". Every phase must keep it green.

## Testing safety
All test classes inherit `vintraxo_tcd.tests.base.TCDTestCase`, which turns `frappe.db.commit` into a no-op while
the class runs. Tests clean tables in `setUp` and depend on the final rollback; a Frappe function that commits
internally must never make that cleanup permanent on a development site.
