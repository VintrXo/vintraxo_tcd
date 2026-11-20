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
- First course: HTML (18 lessons, 5 chapters, 17 quizzes). Next: CSS, JavaScript, Python, SQL (they run in the
  browser); Java, C#, C++ after the code runner (ADR-0036).

## Fixes found while testing the first course
- Text that looks like HTML in quiz questions (`<title>`) was stored mangled by Frappe's XSS filter. Question text is
  now stored with entities and decoded in `assessment.item_from_*`; the portal renders every question field with
  `textContent`, so nothing is ever interpreted as HTML.
- Quiz questions / options follow their own text direction (`unicode-bidi: plaintext`), so code in Arabic quizzes
  is not scrambled.
- Backlinks list only pages in the same language: the "read in the other language" link of translated pages
  (library, Odoo docs) is not a backlink a reader needs.
