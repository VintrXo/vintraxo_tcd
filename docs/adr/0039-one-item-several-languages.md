# ADR-0039: One course, several languages — learners switch language on the page

- Status: Accepted (owner: "the learner sees the course once, with the languages on top, and switches freely")
- Date: 2026-11-21

## Context
Library courses and the Odoo documentation existed as separate Arabic and English spaces: the catalog showed every
course twice, a learner who switched language started again, and each new language would multiply the catalog.

## Decision
- `translation_key` (Data, indexed) on TCD Space, TCD Course and TCD Content, and `language` on TCD Space. Items with
  the same key are versions of one item. The structure (spaces per language, pages with one `language`) is unchanged,
  so direction (RTL / LTR), search and every existing feature keep working per page.
- Content language of a learner: user default `tcd_content_language`, else the interface language
  (`core/content_languages.py`).
- One item per group, in the learner's language (another one if it is missing): home space cards, search results,
  recommendations, "My learning".
- Language buttons at the top of space, course and lesson pages (`templates/includes/tcd_lang_switch.html`). Each is
  a plain link to the same item in the other language (works without JavaScript); with JavaScript the click first
  POSTs `api.switch_language`, which saves the choice and follows the course. It is POST because Frappe does not commit
  GET requests: a first GET version looked right (cache) but saved nothing — caught by checking the database.
- Progress follows the learner: a completed page also completes its other versions (`mirror_completion`, no second
  quiz); switching inside a course enrolls in its other version and copies the completions (`sync_course`); only one
  certificate is issued per translation group (`has_sibling_certificate`).
- The library loader writes the keys (`<course>`, `<course>:<slug>`) and no longer adds a "read in the other
  language" link to each lesson; existing spaces are linked on the next run. The Odoo docs are linked by
  `deploy/odoo_docs/link_languages.py` (`odoo:<slug>`, courses `odoo-course:<slug>`); its loaders set the keys too.

## Consequences
- A new language is a new set of pages with the same keys; learners still see one course.
- The course page shows the buttons only when another version exists and the learner may read it.
