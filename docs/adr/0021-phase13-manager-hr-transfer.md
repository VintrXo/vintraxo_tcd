# ADR-0021: Manager dashboard, attendance rule, HRMS write-back, space export/import

- Status: Accepted (owner chose all four options)
- Date: 2026-11-20

## Decision
- **Attendance rule:** `TCD Course.minimum_attendance` (%). Attendance = attended (Present/Late) / (held − Excused)
  over sessions that have started; with no session held yet the rule is not met. Saving attendance re-checks the
  completion of the listed learners.
- **Manager dashboard (`/learn/team`):** team = members of the TCD Teams the user manages + (with HRMS) active direct
  reports (`Employee.reports_to`). A new read path: managers see training *status* of their team (mandatory
  done/overdue, active/completed, certificates expiring in 30 days, documents not acknowledged, last activity) — no
  answers, grades of single questions or submissions. Admins can pick any team. Not a Frappe role: access follows
  data (being a team manager or having direct reports).
- **HRMS write-back:** on course completion (setting on by default, HRMS only): Training Program per course (reused),
  a submitted Training Event (employee Completed / Present, mandatory flag) and a submitted Training Result with the
  score; runs in the background after commit, failures go to the Error Log; the event is stored on the enrollment
  so it is never written twice. Record builders are pure functions (tested); the HRMS insert path is not run on
  tcd.localhost (no HRMS).
- **Export / import:** a space bundle (JSON, versioned format) of the space, categories, pages, tutorials, courses,
  chapters, paths, quizzes with bank questions, assignments, relations, skills, question categories. Not included:
  people data (enrollments, progress, submissions, certificates, discussions), instructors, uploaded files (links to
  `/files/...` stay as they are). Import creates a new space (name must be free), recreates records with new names,
  rewrites every link, restores statuses (with a version snapshot and review date for published pages) — all or
  nothing (savepoint). Administrators only, because bundles contain quiz answers. Importing on the same site copies
  bank questions (duplicates in the same question category).
- "team" joins the reserved space names (it is a portal route).
