# ADR-0030: Space navigation menu (wiki sidebar)

- Status: Accepted (owner: combine Frappe LMS + Wiki + W3Schools; Wiki has an admin-arranged sidebar)
- Date: 2026-11-20

## Decision
- TCD Space gets a `navigation` table (TCD Space Nav Item: group, link type Page / Course / Learning Path /
  External Link, target, optional label). Order = row order; rows with the same group show together.
- Validation: targets must belong to the same space; external links start with `https://` or `/` and need a label;
  fields of other link types are cleared. At most 200 rows.
- Rendering (`core.navigation.outline`) is per user: items the user cannot read, or unpublished items they cannot
  edit, are left out. It is shown on the space page and as the side menu of wiki pages opened without a course or
  tutorial; a course / tutorial menu always wins.
- The side menu markup moved to `templates/includes/tcd_outline.html` (shared).
- Found while testing: my learning, policies, team, space and verify pages did not load `tcd_portal.js`
  (no theme button); they now do.
