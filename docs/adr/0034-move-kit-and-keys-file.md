# ADR-0034: Move kit — the real server from one bundle, every key from one file

- Status: Accepted (owner: "prepare everything so the move to a real server is only keys")
- Date: 2026-11-20

## Context
The internal server (`erpnext.localhost`) is treated as production. The move must not rebuild anything by hand.
The Phase 21 audit found blockers outside this app: `vintraxo_restaurant` is not in git, `vintraxo_pos` has no
remote, `vintraxo_arabic` has uncommitted work, and `ar.po` translations were edited inside frappe / erpnext / hrms
(and small edits in `pdf_on_submit`, `arabic_translations`). Keys (mail, AI, Judge0, Zoom/Meet, payment, GitHub)
were entered in several Desk forms.

## Decision
`deploy/` in this app holds four files:
- `export_internal.sh` (internal server): one `.tar.gz` with `manifest.tsv` (every app: git url + branch + exact
  commit), our own apps (`vintraxo_*`) and any app without a pushed commit packed as they are on disk (with `.git` and
  uncommitted work), local edits inside upstream apps as `patches/<app>.diff` (built files such as `yarn.lock`,
  `node_modules`, `public/frontend` excluded), and a full backup with files and `site_config_backup.json`.
  `--dry-run` prints the manifest only. The bundle is `chmod 600` (it holds the database and the encryption key).
- `install_prereqs.sh` (fresh Ubuntu 24.04, once): MariaDB, Redis, nginx, supervisor, Node 24, uv + Python 3.14, bench.
- `setup_server.sh` (real server): bench init with Frappe pinned, each app at its commit or unpacked from the bundle,
  patches re-applied, new site, old site config carried over except database login / host / developer settings
  (so `encryption_key` and other apps' keys survive), restore, migrate, `host_name`, `developer_mode 0`, scheduler on,
  new Administrator password, keys file, readiness; `--production` adds nginx + supervisor, cron backups and SSL.
- `keys.example.json`: every key in one place. `vintraxo_tcd.core.server_keys.apply_keys` (bench execute only, refused
  inside a web request) applies it: outgoing e-mail account, AI key, Judge0 runner, Zoom or Google Meet, payment
  gateway, per-space GitHub sync, settings of other apps (`documents`: any DocType by its Desk field names) and
  disabling the trial accounts. Empty values and values starting with `REPLACE` are skipped, so the file can be filled
  in steps and applied again. Each section runs inside its own savepoint: a bad key fails that section only. Reports
  list field names, never values. Passwords go through normal document saves, so they are stored encrypted.
- The readiness check warns while the trial accounts (learner1..3, author, instructor @vintraxo.local) are enabled.

## Consequences
- The owner's git clean-up of the other vintraxo apps is no longer a blocker for the move (still recommended).
- `setup_server.sh` could not be run end-to-end here (no second server); the export was run for real against the
  development site, the patches were checked with `git apply --check -R`, and the config merge was run on a copy.
- `keys.json` is in `.gitignore`.
