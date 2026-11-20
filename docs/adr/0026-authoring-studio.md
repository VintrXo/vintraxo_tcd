# ADR-0026: Authoring studio in the learning portal

- Status: Accepted (owner: combine Frappe LMS + Wiki + W3Schools; LMS and Wiki let authors write from the portal)
- Date: 2026-11-20

## Decision
- `/learn/studio` (home), `/learn/studio/page` and `/learn/studio/course` for users who can create or write
  TCD Content / TCD Course (authors, reviewers, administrators). Everyone else gets a 404.
- **No new permission path:** every save is `doc.save()` / `insert()` / `delete_doc()` with the normal DocType
  permissions, our `has_permission` hooks and the existing validations (block schema, review workflow, locked
  fields of Approved / Published pages, chapters locked once a course leaves Draft). Status changes reuse
  `api.set_content_status` (only reviewers approve / publish when review is required).
- The block form is defined once on the server (`studio.block_spec`, translated there) and rendered by
  `tcd_studio.js`; all user text is set through value / textContent.
- Course outline: chapters (add / rename / reorder / delete) and items (search readable pages, add, reorder,
  optional flag). Limits: 100 chapters, 300 items.
- Found while testing: Frappe's breadcrumb template prints page and parent titles unescaped, and Frappe keeps
  harmless tags such as `<b>` in Data fields. `portal_page` now escapes `title` and every parent title once.

## Consequences
The Desk editor stays for administrators and for fields the studio does not show (SCORM, GitHub, governance
links). No new DocTypes.
