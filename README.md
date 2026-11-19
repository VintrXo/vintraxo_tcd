# VintraXo T-C-D

**Training, Content & Documentation** for Frappe — *Learn. Practice. Build. Document.*
Arabic first (RTL), English second. Works on Frappe v16 with or without ERPNext / HRMS.

| Pillar | What you get |
|---|---|
| Tutorials & practice | Interactive tutorials, references, in-browser playgrounds (Python, SQL, JavaScript, HTML), exercises, quizzes |
| Knowledge | Spaces, page trees, articles, versions with review and approval, Markdown, `[[links]]`, policies / SOPs with acknowledgments |
| Learning | Courses, chapters, learning paths, batches, sessions with attendance, assignments, assessments, certificates, skills |

Plus: mandatory training rules (by role, or department / designation / company with HRMS), manager dashboard,
lesson discussions, content review cycles, notifications, 11 reports, signed webhooks, an optional AI assistant
(off by default) and an optional isolated code runner (Judge0, off by default).

## Install

```bash
cd ~/frappe-bench
bench get-app git@github.com:VintrXo/vintraxo_tcd.git --branch vintraxo
bench --site your-site install-app vintraxo_tcd
bench --site your-site migrate
```

Then in the Desk open **VX → Learning Settings**, give users the TCD roles, and open `/learn`.
Optional demo content: `bench --site your-site execute vintraxo_tcd.demo.create_demo`.

What a new site receives (no Custom Fields or Property Setters are used):

| Item | Source |
|---|---|
| DocTypes, permissions | app DocType JSON |
| 5 roles (TCD Administrator, Content Author, Content Reviewer, Instructor, Learner) | `after_install` + `fixtures/role.json` |
| Notifications, reports, certificate print format, workspace, number cards | standard records in the module folders |
| VX desktop icon and sidebar | `desktop_icon/`, `workspace_sidebar/` |
| Arabic | `translations/ar.csv` |

## Upgrade

```bash
bench --site your-site backup --with-files
cd apps/vintraxo_tcd && git pull && cd ../..
bench setup requirements
bench --site your-site migrate
bench restart
```

## Documentation

| For | Document |
|---|---|
| Learners and instructors (Arabic) | [docs/USER_GUIDE.md](docs/USER_GUIDE.md) |
| Administrators (Arabic) | [docs/ADMIN_GUIDE.md](docs/ADMIN_GUIDE.md) |
| Deployment, upgrade, backup | [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) |
| Developers | [docs/DEVELOPER.md](docs/DEVELOPER.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/DATA_MODEL.md](docs/DATA_MODEL.md), [docs/PERMISSIONS.md](docs/PERMISSIONS.md), [docs/adr/](docs/adr/) |
| Status and history | [docs/PROGRESS.md](docs/PROGRESS.md), [docs/RELEASE_NOTES.md](docs/RELEASE_NOTES.md) |

## Development

- Tests: `bench --site <dev-site> run-tests --app vintraxo_tcd` — never on a production site (tests reset TCD tables).
- Lint: `ruff check` and `ruff format` (ruff 0.14), `pre-commit install` for the hooks.
- CI (GitHub Actions) installs the app on a fresh site and runs all tests on every push to `vintraxo`.

## License

MIT
