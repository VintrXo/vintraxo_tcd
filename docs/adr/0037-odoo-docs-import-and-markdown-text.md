# ADR-0037: Odoo 18 documentation in English and Arabic; Markdown in paragraphs; spaces carry menu and files

- Status: Accepted (owner: "load the Odoo documentation, Arabic and English, complete")
- Date: 2026-11-20

## Content and licence
- Source: the Odoo 18.0 user documentation (`content/applications`, 847 pages), published by Odoo S.A. under
  **CC BY-SA 4.0** (LICENSE of github.com/odoo/documentation). Odoo 18.0 is the newest version with an Arabic
  translation (locale/ar: 44 841 of 44 859 strings translated). The eLearning videos on odoo.com/slides state no
  reuse licence and are **not** copied.
- Licence duties met on every page: a source line with the link to the original page, "© Odoo S.A.", the licence name
  and link, and a note that only the format was converted. The spaces' descriptions say the same. Share-alike: the
  imported pages stay under CC BY-SA 4.0.
- How: the published pages of odoo.com (`/documentation/18.0/` and `/18.0/ar/`) are read as data (one request at a
  time; robots.txt allows /documentation) and converted to TCD blocks; images come from the repository clone (same
  files). Odoo's Sphinx build was **not** run: it executes Python from the downloaded repository.
- Two spaces with the same structure and slugs: `odoo-en` and `odoo-ar`. Each page links to the same page in the
  other language at the top, keeps the Odoo page tree (`parent_content`), and the space menu lists the apps by area.
- Tools: `deploy/odoo_docs/` (fetch.py, convert.py, load.py). To another server: `export_spaces` / `import_spaces`.

## Changes in the app found on the way
- Paragraph and callout text with Markdown (bold, italic, code, links, lists, escapes) is rendered by the same
  sanitized renderer as Markdown blocks. The editors already offered a Markdown toolbar and preview for both (Phase 25)
  while the page showed the raw symbols. Plain text renders exactly as before.
- A page's text follows the page's own language direction: an English page on an Arabic site is left-aligned (the
  global RTL stylesheet forced right alignment). Callouts no longer show the template's line breaks as gaps.
- Space import (Phase 13) now rebuilds the space menu (Phase 22) after its targets exist, with remapped links; before,
  a space with a menu could not be imported on another site, and on the same site the copy's menu pointed to the
  original pages.
- `export_spaces` copies the files the pages use (images, file blocks, links to /files/) with a manifest;
  `import_spaces` creates the missing ones first and rewrites URLs that changed.
