# ADR-0008: Enrolled-only courses and instructor scope

- Status: Accepted
- Date: 2026-11-19

## Context
PLAN.md asks for enrollment-based access. Lessons are shared entities (ADR-0002), so a lesson can be in several
courses and tutorials.

## Decision
- Course `access` = Open | Enrolled Only. A lesson is restricted only if **every** course that contains it is Enrolled
  Only; a learner then needs a non-withdrawn enrollment in one of them. If any Open course uses the lesson, it stays
  open. Staff are not restricted by this layer.
- Courses and paths get an `instructors` table. Enrollments, submissions and course feedback are visible to the
  learner, the course/path instructors and admins; approving and grading require being an instructor of the course.

## Consequences
- Courses without instructors are managed by admins only.
- The restricted-content set is computed per request (fine at current size; revisit with caching in Phase 11).
