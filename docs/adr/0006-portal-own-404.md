# ADR-0006: Portal pages render their own 404

- Status: Accepted
- Date: 2026-11-18

## Context
Apps such as Builder override `www/404` without setting the status code, so `PageDoesNotExistError` raised from a
page's `get_context` returned HTTP 200 on sites with Builder.

## Decision
`core.portal.portal_page` wraps every `/learn` page: on `PageDoesNotExistError` it sets `http_status_code = 404`
and renders `templates/includes/tcd_not_found.html`.

## Consequences
- Correct 404 regardless of other installed apps.
