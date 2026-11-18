# ADR-0003: Permission layers only restrict; hidden means 404

- Status: Accepted
- Date: 2026-11-18

## Context
Frappe evaluates DocPerm first and then `has_permission` / `permission_query_conditions` hooks.

## Decision
DocPerm is the ceiling. App layers (space access, visibility, status for learners, own-records, enrollment) are
implemented in `core/permissions.py` as both `has_permission` (single doc, always returning a bool — `None` counts
as deny in v16) and `permission_query_conditions` (lists, reports, search). Portal pages answer 404 for anything not
readable, so hidden spaces and content are not revealed.

## Consequences
- Same answer from API, Desk lists, reports and portal; every phase ships permission tests.
