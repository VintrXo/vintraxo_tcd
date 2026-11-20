# ADR-0038: Programming library — original W3Schools-style courses from source files

- Status: Accepted (owner: "a complete library of programming courses, like W3Schools")
- Date: 2026-11-20

## Context
The owner asked for an exact copy of W3Schools. Its tutorials, examples and exercises are copyrighted and their terms
forbid copying, so they are not copied. The learner experience (short lessons, try-it editor, fill-in exercises,
reference tables, quizzes, certificate) already exists in the platform (Phases 17–17b); what was missing is content.

## Decision
- Courses are written as original text, Arabic and English, in source files under `library/<course>/` (format in
  `library/README.md`), versioned in git with the app.
- `core/authoring.py` (pure functions) turns the files into page blocks and choice questions;
  `core/library.py` builds a space bundle per language and imports it with the space importer (Phase 13): pages in
  course order, one menu group per chapter, a quiz per lesson with questions (pass 60 %, required to complete),
  one published course (self-enrollment, "All Items", certificate without expiry), and a link at the top of each
  lesson to the same lesson in the other language.
- Re-running on an existing space refreshes only the pages' title / summary / blocks by slug, the way an accepted
  suggested edit does (`flags.change_request`, new version in the history); learners keep their progress.
- Courses: HTML (18 lessons), CSS (18), JavaScript (18), Python (18), SQL (16) — 88 lessons and 81 quizzes per
  language, each course with a certificate. Next: Java, C#, C++ after the code runner (ADR-0036).
- "Try it" blocks can carry hidden `setup` code (`` ```try sql shop ``, named in course.json, one file per language):
  the SQL course runs every example on a ready-made shop database (customers, products, orders, order lines).

## Fixes found while testing the courses
- JavaScript runs ended as soon as the main code finished, so `setTimeout` / `await` examples printed only half. The
  worker now waits for pending timers (checked after promise jobs run); the page's time limit still stops endless code,
  and an error inside a timer is reported.
- A reference entry could not contain `|` (e.g. the operator `||`). Entries now split on " | " when present, plain
  "|" otherwise (older entries), in both the validation (`content.reference_parts`) and the template.
- Text that looks like HTML in quiz questions (`<title>`) was stored mangled by Frappe's XSS filter. Question text is
  now stored with entities and decoded in `assessment.item_from_*`; the portal renders every question field with
  `textContent`, so nothing is ever interpreted as HTML.
- Quiz questions / options follow their own text direction (`unicode-bidi: plaintext`), so code in Arabic quizzes
  is not scrambled.
- Backlinks list only pages in the same language: the "read in the other language" link of translated pages
  (library, Odoo docs) is not a backlink a reader needs.
