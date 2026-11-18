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
