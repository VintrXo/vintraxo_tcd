# ADR-0023: Negative marking, proctoring, test cases, badges

- Status: Accepted
- Date: 2026-11-20

## Decision
- **Negative marking (quiz option):** a wrong answer to a choice question (single, multiple, true/false) takes
  `negative_mark_percent` of its points; a blank answer does not; the total never goes below zero.
- **Proctoring (quiz option):** a proctored quiz always starts an attempt. The browser reports leaving the tab,
  leaving the window and pasting (`api.report_quiz_violation`); each report is logged (TCD Quiz Violation) and
  counted on the attempt. At `max_violations` the browser submits the quiz and the submission is flagged for the
  instructor. Browser-side signals only: a deterrent and an audit trail, not a lock-down browser.
- **Test cases (Code questions):** each case runs on the code runner with its input on stdin; the grade is the share
  of passing cases. Visible cases are shown as examples; hidden ones never leave the server. Needs the runner
  (validation refuses test cases otherwise); a runner outage sends the answer to manual review; learner-sent
  `server_cases` are dropped like `server_output`.
- **Badges:** TCD Badge (event + optional count or course/path) and TCD Badge Award (one per user and badge).
  Awarded automatically on course/path completion, lessons completed, quizzes passed, certificate earned, answers
  accepted in discussions, suggested edits accepted — or manually by an admin. Awarding never blocks the action that
  triggered it (errors go to the Error Log). Shown in My Learning, with a notification.
