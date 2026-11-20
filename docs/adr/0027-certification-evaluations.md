# ADR-0027: Certification evaluations with evaluator schedules

- Status: Accepted (owner: combine Frappe LMS + Wiki + W3Schools; LMS has certificate requests and evaluators)
- Date: 2026-11-20

## Decision
- **TCD Evaluator** (one per user): weekly availability rows (day, from, to) and an unavailable period.
- **TCD Course**: `requires_evaluation` (only with `issue_certificate`), `evaluation_minutes` (10–240, default 30)
  and an optional evaluator list; empty = the course instructors who are active evaluators.
- On course completion the certificate is **not** issued when an evaluation is required; the learner is told to
  book. Slots: from tomorrow for 14 days, each schedule window cut into `evaluation_minutes` pieces, minus the
  evaluator's unavailable dates and other Scheduled bookings (max 80 shown).
- **TCD Evaluation** (Scheduled / Passed / Failed / No Show / Cancelled) is created only by `book()` and only for a
  slot that is offered now; one Scheduled booking per learner and course. The learner may cancel before it starts.
- The evaluator (or an admin) records the result after the session starts. Passed issues the certificate
  (`credentials.issue_certificate`) and links it; Failed / No Show lets the learner book again. Results are final.
- Permissions: learner reads own; evaluator reads/writes assigned; admins all (`evaluation_has_permission`,
  `evaluation_query`). All fields are read-only in the Desk; changes go through the service.
- Times are the site time zone (single-site deployment).

## Consequences
Meeting links are pasted by the evaluator (no automatic Zoom/Meet for evaluations yet).
