# ADR-0014: Certificates and skills are awarded by completion, verified by public code

- Status: Accepted
- Date: 2026-11-19

## Context
PLAN Phase 5: skills library, user skills, competency matrix and gap report; certificates with PDF, verification
code, public page, expiry and renewal, issued automatically on completion. HRMS is optional.

## Decision
- Skills are attached to courses and paths (skill + level). Completion awards them; manual awards by admins exist
  for prior experience.
- Competency profiles target a Frappe **Role** (works without HRMS); Phase 8 can add department/designation when
  HRMS is installed.
- Certificates are documents with a random 16-character verification code (secrets.token_urlsafe), not guessable
  sequence numbers. The public page shows only holder name, title, dates and status.
- PDF uses a standard Print Format rendered by Frappe's PDF pipeline; no custom PDF code.
- Expiry runs as a daily scheduler event; renewal re-opens the enrollment instead of copying progress.

## Consequences
- Certificates can be revoked (status) without deleting history.
- The verification page is public by design; it must never show e-mail or other personal data.
