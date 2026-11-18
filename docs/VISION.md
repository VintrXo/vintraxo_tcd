# VintraXo T-C-D — Vision

**Training, Content & Documentation** — *Learn. Practice. Build. Document.*

One Frappe app, three equal pillars, one unified experience. Arabic first (RTL), English second.

## The three pillars

| Pillar | Inspired by | What it gives the organization |
|---|---|---|
| Tutorials & practice | W3Schools | Interactive tutorials, references, Try-it playgrounds, exercises, quizzes, projects |
| Knowledge | Wiki | Knowledge spaces, page trees, articles, versions, approvals, policies and SOPs |
| Learning | LMS | Courses, chapters, lessons, paths, enrollment, batches, assignments, assessments, certificates |

The pillars share one content model: a lesson, an article and a reference page are the same entity
(`TCD Content`) placed in different structures (tutorial, course chapter, wiki tree). Nothing is copied
between pillars; they link.

## Principles

1. **One content entity, many structures.** Tutorials, courses and wiki trees reference content; they never duplicate it.
2. **Permissions only restrict.** Frappe role permissions are the ceiling; space, visibility, enrollment and
   department layers can only narrow access.
3. **Untrusted code never runs on the server.** Playgrounds run in the learner's browser (sandboxed iframe,
   Pyodide, SQLite WASM). A server sandbox needs an approved isolation design first.
4. **Arabic first.** RTL layout, Arabic-normalized search, Arabic labels; code always stays LTR.
5. **Zero core modification.** Hooks, custom DocTypes and public APIs only. Installs without ERPNext/HRMS;
   integrations are guarded.
6. **Review before publish.** Content, courses, policies and AI output go through human review.
7. **Evidence over claims.** Every feature ships with unit and permission tests; compliance actions
   (acknowledgments, approvals, certificates) leave an audit trail.

## Users

- **Learner / employee:** finds answers, follows tutorials and courses, practices in the browser, earns certificates,
  acknowledges policies.
- **Content author:** writes lessons and articles with the block editor, builds tutorials and courses.
- **Reviewer:** approves content and policies before they go live.
- **Instructor:** runs courses and batches, grades assignments, approves completion, follows progress.
- **Administrator / compliance:** spaces, access, mandatory training, reports, integrations.

## Scope by phase

The operative, phase-by-phase scope lives in [PLAN.md](PLAN.md); status in [PROGRESS.md](PROGRESS.md);
decisions in [adr/](adr/).
