# ADR-0035: Install on the existing production server; carry content, not the site

- Status: Accepted (owner: the real server already runs; "make it compatible with everything")
- Date: 2026-11-20

## Context
The real server already runs its own site: frappe 16.60.1, erpnext 16.60.0, payments 16.0.1, wiki 3.5.0,
lms 16.1.1, vintraxo_arabic, vintraxo_limt, vintraxo_one_db. The move kit of ADR-0034 restores a full backup onto a
fresh bench, which would overwrite that site. The first install there failed to save a page:
`No module named 'defusedxml'` (fixed in 0.3.1: declared dependency, loaded only for SCORM).

## Decision
- `deploy/install_on_existing.sh <site> [keys.json] [spaces-dir]` on the server's bench: backup, get-app or
  `git pull --ff-only`, `bench setup requirements --python vintraxo_tcd` (and a check that defusedxml and anthropic
  import), install-app or migrate, build, clear cache, keys, content import, readiness. Nothing else on the bench
  is touched.
- Content travels as space exports (Phase 13 format): `vintraxo_tcd.core.move.export_spaces` on the internal server,
  `vintraxo_tcd.core.move.import_spaces` on the server. A space whose name already exists is skipped, so the import
  can be run again safely. Users, enrollments, progress and certificates stay on their own servers (as in Phase 13).
- Every bench-execute entry point starts with `server_keys.cli_setup()`: refuses web requests, runs as
  Administrator, and sets `frappe.local.lang` when it is empty. Frappe 16.33.1 and 16.60.1 share a bug in
  `frappe.locale.get_locale_value` (UnboundLocalError when no language is set) that broke the content import
  through the "TCD Content Review Request" notification; found by importing the real internal export.
- Compatibility with frappe 16.60.1 was checked statically: every `frappe` import and `frappe.<module>.<attr>` used by
  the app exists in the v16.60.1 source. The test suite was not run on 16.60.1 (no MariaDB root password here for a
  second bench). The app imports nothing from lms, wiki, hrms or erpnext at module level; payments and ERPNext /
  HRMS links are guarded.

## Consequences
- ADR-0034's full-restore kit stays for a fresh server (disaster recovery or a second server).
- Never run the TCD test suite on the production site (tests delete TCD tables).
