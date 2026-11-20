# ADR-0028: Scheduled release of chapters and "coming soon" courses

- Status: Accepted (owner: combine Frappe LMS + Wiki + W3Schools; LMS batches release lessons on a schedule)
- Date: 2026-11-20

## Decision
- **Drip:** TCD Chapter `release_after_days` (after the learner's `enrolled_on`) and `release_on` (fixed date).
  An item opens on the later of the two. `courses.drip_lock(user, content)` returns the opening date when every
  active enrollment (Active / Pending Approval) that contains the page still holds it back; one open course is
  enough, and people who are not enrolled are not affected (wiki pages stay readable).
- Enforcement in one place per path: `api.get_lesson` (blocks, quiz and assignment hidden, `opens_on` returned),
  `api._quiz_for_user` (quiz APIs), `progress.complete` (no completion). The course page and the lesson side menu
  show the item as locked with its date.
- Our existing sessions (TCD Session with batch, attendance, Zoom / Meet) already cover the LMS batch timetable;
  course ratings cover batch feedback. They are not duplicated.
- **Coming soon:** TCD Course `coming_soon` + `opens_on`. Self-enrollment is refused while it is set; learners
  ask to be notified (TCD Course Interest, created only by the service). When the course becomes Published and
  not coming soon, everyone who asked is notified once.

## Consequences
Both settings are editable in the Desk and in the portal studio.
