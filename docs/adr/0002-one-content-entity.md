# ADR-0002: One content entity reused by every pillar

- Status: Accepted
- Date: 2026-11-18

## Context
Tutorials, courses and wiki trees all need lessons/articles. Separate lesson DocTypes per pillar would duplicate
content, translations, versions and permissions.

## Decision
`TCD Content` is the only content entity (blocks, versions, review workflow, visibility). Structures reference it:
tutorials through `TCD Tutorial Lesson`, course chapters through `TCD Learning Item`, later wiki trees the same way.

## Consequences
- A lesson is written, reviewed and translated once; progress is per content and rolls up into every structure.
- Rules that depend on the structure (sequence, enrollment) are enforced where the structure is known
  (e.g. sequence gating checks the learner's active enrollments).
