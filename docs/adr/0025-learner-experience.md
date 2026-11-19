# ADR-0025: Learner experience closer to W3Schools-style tutorials

- Status: Accepted (owner: "what are we missing compared with W3Schools" → build items 1–5 + dark mode)
- Date: 2026-11-20

## Decision
- **Lesson side menu:** when a lesson is opened from a course (`?course=`) or a tutorial (`?tutorial=`), the page
  shows every item of that course / tutorial the learner can read, with its state (done / open / locked) and the
  overall percent. Unreadable items are left out (same permission checks as the course page). No side menu otherwise.
- **Previous / next on top** of the lesson as well as at the bottom.
- **Syntax highlighting + copy:** our own small highlighter (`tcd_highlight.js`, no third-party code) for Python,
  SQL, JavaScript, HTML and C-like languages. Every token is escaped. Our blocks carry `nohighlight` so Frappe's
  site-wide highlight.js leaves them alone (it re-rendered the exercise inputs). The playground editor is a
  transparent textarea over a highlighted copy. Copy falls back to selecting the code when the clipboard is refused.
- **"Try it yourself" full screen:** the playground opens over the whole window with the editor and the result side
  by side (stacked on phones); Esc closes it. The code still runs in the same browser sandbox.
- **Practice exercise block** (`exercise`: prompt, code with `___` blanks, one answer per blank, `a | b` for
  alternatives, optional hint). Checked in the browser and never recorded — it is practice, not assessment, so the
  answers being in the page is acceptable. Graded work stays in quizzes.
- **Dark mode:** a toggle on every portal page, remembered per browser (localStorage); default is light. Code panels
  stay dark in both themes.

- **Reference table block** (`reference`: optional title and language, entries "name | description | example").
  Rendered as an escaped table with a filter box (more than 8 rows), highlighted examples, a link anchor per row,
  and cards instead of columns on phones.

## Consequences
No new DocTypes or fields. More server-run languages (W3Schools item 8) wait for the Judge0 server.
