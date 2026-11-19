# Deployment and upgrade — vintraxo_tcd

## Requirements
- Frappe v16 (tested on 16.33.1), Python 3.14, MariaDB, Redis, a production bench (`bench setup production`:
  nginx + gunicorn with several workers, background workers, scheduler).
- ERPNext / HRMS are **optional**. Without them, HR filters in training rules match nobody and departments are ignored.
- Python dependency: `anthropic` (installed by `bench setup requirements`; used only when AI is enabled).
- PDF certificates use Frappe's Chrome PDF generator (set on the print format; wkhtmltopdf could not resolve the
  site host on the development bench). Check that Frappe's Chrome PDF generation works on the server.

## Install
```bash
bench get-app <repo-url> --branch <branch>
bench --site <site> install-app vintraxo_tcd
bench --site <site> migrate
```
What a new site receives:
| Item | How |
|---|---|
| 60+ DocTypes, fields, permissions | App DocType JSON (no Custom Fields or Property Setters are used) |
| 5 roles (TCD Administrator, Content Author, Content Reviewer, Instructor, Learner) | `after_install` + fixture `fixtures/role.json` (kept on every migrate) |
| 7 notifications, 9 reports, certificate print format, workspace | Standard records in the module folders, synced by migrate |
| 5 number cards | Module folder `number_card/`, synced because of `importable_doctypes = ["Number Card"]` |
| VX desktop icon and sidebar | App folders `desktop_icon/`, `workspace_sidebar/` |
| "Learning" item in the website navbar | `after_install` (removed again by `before_uninstall`) |
| Arabic translations | `translations/ar.csv` |
| Settings defaults | Portal on, Arabic, review before publish, playgrounds on, AI off |

Patches in `patches.txt` are marked as done on a fresh install (they only fix data on older sites).
Then: assign roles, open **VX → Learning Settings**, enable the portal. Optional demo: `vintraxo_tcd.demo.create_demo`.

## Upgrade
```bash
bench --site <site> backup --with-files
cd apps/vintraxo_tcd && git pull && cd ../..
bench setup requirements
bench --site <site> migrate
bench build --app vintraxo_tcd
bench restart
```
Patches in `patches.txt` run during `migrate` (renames before the model sync, data fixes after).

## Background jobs and scheduler
- Must run: scheduler and workers (`short`, `default`, `long`).
- Daily: certificate expiry, governance expiry/review reminders, training rules, purge of sent integration events.
- Every 5 minutes: integration outbox (retries and anything missed).

## Configuration checklist
- Integrations: HTTPS endpoints; set a signing secret; receivers verify `X-TCD-Signature`
  (`sha256=HMAC(secret, "<X-TCD-Timestamp>.<body>")`) and de-duplicate on `X-TCD-Delivery`.
- AI: off by default. Enable in **AI Settings**, set key, prices, monthly budget, daily limit; keep
  "Never send restricted content" and "Remove e-mails and phone numbers" on unless policy allows otherwise.

## Backup and restore
- Backup: `bench --site <site> backup --with-files` (database + public + private files).
- Restore (on a new or the same site):
  `bench --site <site> restore <database.sql.gz> --with-public-files <files.tar> --with-private-files <private-files.tar>`
  then `bench --site <site> migrate`.

## Known limits
- `bench serve` (development server) is single-process: ~11 requests/s locally, and Frappe core's router
  occasionally raises `TypeError: 'NoneType' object is not iterable` under concurrent load (also on `/login`, not
  related to this app). Use the production setup for real traffic.
- Code playgrounds run in the learner's browser unless the code runner is enabled.

## Code runner (optional, Phase 10)
1. On a **separate VM** (not the Frappe server): install Judge0 CE (a patched release, 1.13.1 or later) following
   its docs; firewall: inbound only from the Frappe server on the runner port, outbound denied; set an auth token.
2. In VX → Learning Settings → Code Runner: enable, set the URL and token, keep the limits, click **Test Runner**.
3. Use runner languages in playground blocks and Code questions, or tick "Grade on the Code Runner".
