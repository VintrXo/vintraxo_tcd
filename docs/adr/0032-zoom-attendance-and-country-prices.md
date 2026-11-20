# ADR-0032: Attendance from Zoom and prices by country

- Status: Accepted (owner: build the remaining Frappe LMS features)
- Date: 2026-11-20

## Decision
- **Zoom attendance:** after a Zoom session ends, `meetings.take_zoom_attendance` reads
  `GET /v2/past_meetings/{id}/participants` (paged), adds up the seconds per e-mail (rejoins), and fills only the
  attendance rows that are still empty: Present when the learner stayed at least `zoom_attendance_percent` of the
  session (default 50 %), else Absent, with a "Zoom: N min" note. Rows marked by hand are never changed.
  The session becomes Completed and `attendance_synced` is set. An hourly job does this for sessions that ended in
  the last 48 hours (one commit per session); instructors can also press "Attendance from Zoom". Participants
  without an e-mail (phone, guests) cannot be matched and are ignored.
- **Country prices:** paid courses / paths get an optional table of prices by country (own currency). The learner's
  country comes from their profile (new field). Checkout, the quote and the course / path page use that price;
  otherwise the default price. The country is chosen by the learner, so this is a pricing convenience, not a
  fraud control; coupons apply on top as before.
