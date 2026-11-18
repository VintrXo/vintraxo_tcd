# ADR-0009: Lesson types, media blocks and upload validation

- Status: Accepted
- Date: 2026-11-19

## Context
PLAN.md lists lesson types (Article, Video, Interactive Tutorial, Playground, Quiz, Assignment, External, Project,
Document). `content_type` already means the structure role (Article / Tutorial / Lesson / Reference).

## Decision
- Add `lesson_type` on TCD Content (only for content_type = Lesson) instead of widening `content_type`.
- New blocks: `video` (YouTube/Vimeo or uploaded mp4/webm; host allowlist in settings; normalized to an embed URL on
  save), `link` (https external link, opened with rel="noopener noreferrer"), `file` (uploaded File only).
- Uploads must reference an existing File doc, pass the extension allowlist and size limit; learner submissions use
  private files they own.

## Consequences
- No arbitrary iframes or HTML in content; every embed URL is produced by our code from a validated id.
