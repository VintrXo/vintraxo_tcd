# ADR-0004: Arabic via translations/ar.csv with contexts

- Status: Accepted
- Date: 2026-11-18

## Context
App translations are global for the site. Generic words (Title, Status, Course, Items, Due Date) already exist in
Frappe/ERPNext/Education translations, sometimes with wording that is wrong for us. `.po` files of other apps are
not compiled on this bench.

## Decision
- Ship `translations/ar.csv` (no compile step).
- App-specific strings use plain keys. Generic words keep the upstream wording on the plain key and get our wording
  through a context: the DocType name for Desk labels/options (Frappe passes it automatically), `TCD` for portal and
  report statuses, `TCD Block` for editor labels.
- DocType names are translated without the "TCD" prefix to avoid RTL ordering glitches.
- `tests/test_translations.py` fails when a name, label, description or option lacks Arabic or still shows "TCD".

## Consequences
- Our screens read correctly without changing other apps' screens.
