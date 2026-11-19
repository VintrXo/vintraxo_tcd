# ADR-0015: One governance DocType, snapshot versions and an acknowledgment log

- Status: Accepted
- Date: 2026-11-19

## Context
PLAN Phase 6 lists TCD Document, TCD Policy and TCD SOP with the same lifecycle, effective/expiry dates, review
reminders, mandatory acknowledgment with an audit log, and department access that works without HRMS.

## Decision
- One DocType, `TCD Governance Document`, with `doc_kind` = Document / Policy / SOP. The three kinds share every rule;
  three DocTypes would triplicate code, permissions and translations (same reasoning as ADR-0002).
- Activation writes an immutable `TCD Governance Version`. Readers always get the latest snapshot, so a document
  under Revision stays readable in its approved form.
- `TCD Acknowledgment` is an append-only log (user, version, timestamp, statement). It cannot be edited or created
  outside the API.
- Departments are stored as text. Matching uses ERPNext's `Employee.department` only when the Employee DocType exists
  (it belongs to ERPNext, not HRMS); otherwise departments are ignored and documented as such.
- Reminders use ToDo records (visible in the owner's Desk) from a daily scheduler job; e-mail/notification channels
  come in Phase 7.

## Consequences
- Policies, SOPs and documents appear in one list with a kind filter.
- Without ERPNext, department targeting is a no-op (by design, shown in the field description).
