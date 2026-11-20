# ADR-0033: Certified learners page, platform statistics, Markdown editor

- Status: Accepted (owner: build the remaining Frappe LMS / Wiki features)
- Date: 2026-11-20

## Decision
- `/learn/certified` (login required): counts (published courses / paths / pages, learners, completions, active
  certificates) and the active certificates of learners whose profile is visible to colleagues — opt-in, nobody is
  listed otherwise. Each card links to the profile and the public verification page. Filter by course.
- Markdown editing helper (`tcd_md.js`): bold / italic / heading / list / link / code buttons and a preview for text
  areas marked `data-md` — the learner "suggest an edit" form (paragraph, callout, Markdown text) and the studio's
  paragraph / callout / Markdown blocks. The preview is rendered by the server (`api.preview_markdown`) with the same
  sanitizing renderer as the pages (logged-in users, 20 000 characters max, space read check for wiki links).
