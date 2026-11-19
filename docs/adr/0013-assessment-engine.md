# ADR-0013: Assessment engine on a question bank; browser-checked code questions

- Status: Accepted
- Date: 2026-11-19

## Context
PLAN Phase 4 asks for a question bank, many question types, randomization, time limits and manual grading.
Quizzes already existed with inline objective questions and server grading. Code must never run on the server.

## Decision
- `TCD Question` is the bank. A quiz uses inline questions (kept for compatibility) and/or bank items: a fixed
  question or "pick N from a category".
- Every attempt has a server-side paper fixed at `start_quiz` (random picks, option order, deadline). Grading uses
  the paper, never what the browser claims was asked.
- Objective types are graded on the server. Essay/File (and Short Answer without accepted answers) go to manual
  review with rubrics.
- Code and SQL questions run in the learner's browser runtime (ADR-0001). The browser sends the code **and** the
  output; the server compares the output with `expected_output`. This is **not tamper-proof**: a learner can forge
  the output. Questions marked `manual_review` are therefore always reviewed by a person; use that for anything
  high-stakes. Real server-side execution is Phase 10 and needs an approved isolation design.

## Consequences
- Old quizzes and their analytics keep working; results are keyed by inline row name or bank question name.
- Integrity of auto-checked code answers is "honest learner" level by design, documented in the UI help text.
