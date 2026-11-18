# ADR-0007: TCD Student Group renamed to TCD Batch

- Status: Accepted
- Date: 2026-11-19

## Context
PLAN.md names cohorts "TCD Batch". Phase 1 (previous plan) shipped "TCD Student Group"; no production data exists.

## Decision
Rename DocTypes with `frappe.rename_doc("DocType", ...)` in a pre-model-sync patch (tables and Link options follow),
and copy `TCD Enrollment.student_group` to the new `batch` field with `rename_field` after sync. API argument becomes
`batch`.

## Consequences
One-time patch; old column stays in the table (Frappe never drops columns on sync).
