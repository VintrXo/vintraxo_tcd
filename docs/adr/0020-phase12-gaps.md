# ADR-0020: Sessions and attendance, lesson discussions, knowledge freshness, self-withdrawal

- Status: Accepted (owner: "find what the app is missing and complete it")
- Date: 2026-11-20

## Context
A gap review against VISION.md found: instructors "run batches" but there were no sessions or attendance; learners
"find answers" but could not ask about a page; policies had review cycles but articles and lessons did not; learners
could not leave an optional course (and a course withdrawn by an admin showed no Enroll button).

## Decision
- **Sessions:** `TCD Session` (course, optional batch, classroom/online, start/end, location or meeting link,
  instructor, status) with `TCD Session Attendance` rows (Present/Late/Absent/Excused). Invited = active enrollments
  of the course, narrowed to the batch when set. Instructors manage sessions of their courses only
  (`session_has_permission` / `session_query`); attendance only after the session starts. Learners see upcoming
  sessions and their own attendance on the course page and in My Learning; the meeting link only for invited
  learners. New / moved / cancelled sessions notify the invited learners. Report: TCD Attendance (Late counts as
  attended, Excused is left out of the rate). Calendar view in the Desk.
- **Discussions:** `TCD Discussion Post` (question or reply), plain text only, created only through the service
  (`api.discussion_*`). Readers of a published page post (10 per hour); moderators are the page owner, instructors
  of courses using the page, reviewers and admins (answer, hide; the asker or a moderator picks the best answer).
  Notifications to owner/instructors (questions) and the asker (replies). Toggle in Learning Settings.
- **Freshness:** content owner + review cycle (page value, else Learning Settings default 12 months, or "No Review
  Needed"). Publishing counts as a review; "Mark as Reviewed" confirms without republishing; a ToDo reminds the
  owner a week before; readers see a notice when the date has passed; report TCD Content Freshness.
- **Withdraw:** `api.withdraw` for the user's own non-mandatory, not-completed enrollment; withdrawn enrollments are
  treated as "not enrolled" on course/path pages so the learner can enroll again.
- **Settings added later:** a patch stores their defaults, because Frappe reads a missing Check/Int single value as 0.
- **Asset versions:** portal pages load the app's JS/CSS with `?v=<file mtime>` (`asset_version()` Jinja method);
  `/assets` is served with a 12-hour cache, so without it learners kept old code after an update.

## Consequences
- Course completion does not depend on attendance (can be added as a completion rule later).
- Discussion posts cannot be edited by their authors (moderators can hide them).
