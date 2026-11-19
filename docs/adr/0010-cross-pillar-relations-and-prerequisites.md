# ADR-0010: Cross-pillar relations and prerequisites

- Status: Accepted
- Date: 2026-11-19

## Context
PLAN Phase 2 connects wiki pages, tutorials, references, courses and paths without duplicating content.
`TCD Content Relation` existed (content → content) but was unused and had no documented direction.

## Decision
- Extend `TCD Content Relation` with `target_type` (Content / Course / Learning Path) and one Link per target type
  (no Dynamic Link, per DATA_MODEL decisions). Direction is from_content → target.
- `Prerequisite` = from_content requires the target. Satisfied when the target content is Completed, or the learner's
  course/path enrollment is Completed.
- Courses get a `prerequisites` table of courses, checked on self-enrollment.
- "Used in" (tutorials, courses, paths containing a content) is computed from structure tables, not stored.
- Enforcement applies to learners only; staff see warnings, never blocks.

## Consequences
- Existing relations keep working (target_type defaults to Content).
- Prerequisite cycles are rejected only for direct reverse pairs; deeper cycles are an authoring error shown as
  unmet prerequisites.
