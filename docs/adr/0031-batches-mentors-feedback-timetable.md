# ADR-0031: Batch mentors, batch feedback and timetable templates

- Status: Accepted (owner: build the remaining Frappe LMS batch features)
- Date: 2026-11-20

## Decision
- **Mentors:** TCD Batch `mentors` (TCD Batch Mentor). A mentor is treated like a team manager for the batch
  members: `/learn/team` (status only — never answers or scores of single questions), a `batch:<name>` filter,
  and access only to their own batches (admins: all).
- **Batch feedback:** TCD Batch Feedback (content, instructor, overall 1–5, comment) — one per member and batch,
  sent and updated from My Learning, created only by the service. Averages and comments are shown to the batch
  mentors and admins on My Team; instructors can read the list in the Desk.
- **Timetable template:** TCD Batch `course`, `instructor` and `timetable` (day, from, to, title, type, location).
  "Generate Sessions" creates one TCD Session per row and matching day between the batch dates with normal
  permissions (course instructors / admins); sessions that already exist at the same start are skipped, so it can
  be run again after extending the dates. Max 300 sessions per run. Sessions keep their existing behaviour
  (invitations, Zoom / Meet, attendance).
