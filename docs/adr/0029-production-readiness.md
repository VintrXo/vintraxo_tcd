# ADR-0029: Production readiness check and the move to the real server

- Status: Accepted (owner: treat the internal server as the full system so the move needs no rework)
- Date: 2026-11-20

## Decision
- `core/ops.readiness()` — read-only checks: scheduler, host_name, encryption_key, developer_mode, age of the
  latest database backup, outgoing e-mail, portal / guest / SCORM settings, TCD roles, AI key, code runner,
  Zoom credentials, paid courses without a gateway, evaluation courses without evaluators, overdue reviews.
  Shown in the Desk (Learning Settings → Readiness check, admins only) and via `bench execute`.
- The move is "restore the internal site on a new bench with the same apps at the same commits"
  (`docs/MOVE_TO_SERVER.md`), not a rebuild; content moves with the database and files. Space export/import stays
  for moving single spaces.
- Found during the audit (owner action, outside this app): `vintraxo_restaurant` and `vintraxo_smart_cart` are not
  in git, `vintraxo_pos` has no remote, `vintraxo_arabic` has uncommitted work, and Arabic `.po` files of
  frappe / erpnext / hrms and two files in `pdf_on_submit` / `arabic_translations` are edited in place.

## Consequences
A full restore drill needs the MariaDB root password (to create a scratch site); it is listed as a step in the
move guide instead of being run on the internal bench.
