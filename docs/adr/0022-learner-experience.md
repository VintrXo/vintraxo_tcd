# ADR-0022: Table of contents, course media, video watching, personal notes, suggested edits

- Status: Accepted (owner: build everything found missing compared with Frappe LMS / Wiki)
- Date: 2026-11-20

## Decision
- **Table of contents:** built on the server from heading blocks and Markdown h2/h3 (`wiki.table_of_contents`);
  generated ids only (`sec-N`), never user text; shown from 3 headings.
- **Course / path media:** `cover_image` (public file) and `intro_video` validated with the same rules as video
  blocks (`media.parse_video`); a link that is no longer allowed is simply not shown.
- **Video watching:** the browser counts seconds actually played (jumps over 2 s do not count) for uploaded videos
  (media events), YouTube and Vimeo (their postMessage player APIs, no extra scripts; messages accepted only from
  their origins) and reports every 15 s and on page hide. The server keeps the maximum per video, caps at the
  duration, and `min_video_percent` on a page blocks completion below that share. Reported by the browser: a
  nudge, not proof (documented like the device output of code questions).
- **Notes:** `TCD Lesson Note` has no role permissions; read/written only through the service for the current user.
- **Suggested edits:** readers change only text fields of existing blocks (heading, paragraph, callout, list,
  Markdown, code) and the title; the proposal goes through the normal block validation. Reviewers accept (applies
  the text to the published page with a new version snapshot — the review is the approval) or reject. A page that
  changed after the proposal (hash of its blocks) turns the request into a Conflict; nothing is overwritten.
  5 suggestions per user per hour; toggle in Learning Settings.
