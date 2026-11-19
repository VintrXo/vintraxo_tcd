# ADR-0011: Unified search over content, courses and paths

- Status: Accepted
- Date: 2026-11-19

## Context
Search covered TCD Content only. Courses and paths have no derived search text.

## Decision
Add a derived, Arabic-normalized `search_text` to TCD Course (title, summary, chapter titles) and TCD Learning Path
(title, summary, course titles), filled on save and backfilled by a patch. One `search_all` service queries each
type with `get_list` (permission-filtered), scores with the same ranking as content search, and merges the lists.

## Consequences
- One ranking for all types; filters by type and space.
- Chapter title changes refresh the course search text on chapter save.
