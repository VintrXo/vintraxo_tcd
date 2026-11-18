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
| search.py | Arabic-aware text normalization |
| content.py | Block schema, slugs, search_text, tutorial lessons, review workflow, version snapshots |
| permissions.py | Space/visibility access (has_permission + permission_query_conditions) |
| progress.py | Lesson/tutorial progress and roll-up |
| quiz.py | Quiz validation, learner payload (no answers), grading |
| portal.py | Context for /learn pages (login/portal guards, listings, lesson page) |

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

## Learner portal (P3)
| Route | Page | Content |
|---|---|---|
| `/learn` | `www/learn/index` | Spaces, "continue learning", search (`?q=`) |
| `/learn/<space>` | `www/learn/space` | Content grouped by category; tutorials first |
| `/learn/<space>/<slug>[?tutorial=]` | `www/learn/content` | Blocks, tutorial lessons, quiz, complete button, prev/next |

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
- Verified in headless Chromium: JS/Python infinite loops are killed, `fetch` to the site from the sandbox is blocked
  (origin `null`), HTML preview cannot touch the parent page.
