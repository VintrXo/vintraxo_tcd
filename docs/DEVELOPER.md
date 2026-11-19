# Developer guide — vintraxo_tcd

Read first: `VISION.md`, `ARCHITECTURE.md` (services, API, routes), `DATA_MODEL.md`, `PERMISSIONS.md`, `adr/`.

## Layout
- `vintraxo_tcd/core/*.py` — all business rules (DocType controllers stay thin and call these).
- `vintraxo_tcd/api.py` — thin whitelisted endpoints; every endpoint checks permissions or goes through a service
  that does. Only `verify_certificate` allows guests (enforced by `tests/test_ph11_hardening.py`).
- `www/learn/*` — portal pages; `templates/includes/tcd_blocks.html` renders content blocks.
- `public/js/tcd_portal.js` (portal), `tcd_playground.js` (browser runtimes), `tcd_desk.js`, `tcd_ai_*.js` (Desk).
- `translations/ar.csv` — Arabic (see "Translations").

## Rules that keep the app safe
- Permission layers only restrict (`core/permissions.py`, ADR-0003). Use `frappe.get_list` / `has_permission`;
  `ignore_permissions=True` only inside a service after its own check.
- Block HTML: only `wiki.prepare_blocks` produces `html` (sanitized Markdown / escaped inline links); stored `html`
  keys are dropped on save and ignored on render. Templates escape everything else with `|e`.
- Portal JS builds DOM with `textContent` / `createElement`, never `innerHTML` with user data.
- User-facing errors: `frappe.throw(_("..."), SomeError)` (a bare `raise` shows the exception class to users).
- No ERPNext/HRMS import: check `frappe.db.exists("DocType", "Employee")` (`training.hr_available()`).
- AI: call `ai.gateway()` only, with documents that passed `ai.retrieve` / `_sendable` for the user.
- Integrations: call `integrations.emit(event, doc)` at the business moment; never send HTTP inline.

## Translations
- Desk labels: rows with the DocType as context. Portal / statuses: context `TCD`. Editor: `TCD Block`.
- Select values and table descriptions are translated by Frappe **without** context (lists, grids): they also need
  a plain row (`test_grid_and_list_values_have_plain_keys`). Generic words keep the upstream Frappe/ERPNext wording.
- Do not run `bench compile-po-to-mo`.

## Tests
- Every test class extends `tests/base.py: TCDTestCase` (makes `frappe.db.commit` a no-op and rolls back), so tests
  never change site data, even when Frappe code commits internally.
- `bench --site <site> run-tests --app vintraxo_tcd` (146 tests). External services (webhooks, AI) are mocked.
- Quality gate before a commit: `ruff check` + `ruff format --check` (ruff 0.14, py314), `node --check` on JS,
  `bench migrate`, full test run.

## Extending
- New AI provider: a class with `complete(...)` like `ai.AnthropicProvider`, registered in another app's hooks:
  `tcd_ai_providers = {"Name": "my_app.ai.MyProvider"}`.
- New integration event: add it to `integrations.EVENTS`, to the Select options of TCD Connector Event and
  TCD Integration Event, and call `emit()` from the service.
