# PERMISSIONS

| Role | Purpose | Desk access |
|---|---|---|
| TCD Administrator | Full control of TCD settings and content | Yes |
| TCD Content Author | Create and edit content | Yes |
| TCD Content Reviewer | Review and approve content | Yes |
| TCD Instructor | Manage learning material and learners | Yes |
| TCD Learner | Consume content, track progress | No (portal) |

"Staff" = Author, Reviewer, Instructor, Administrator. "Admin" = TCD Administrator, System Manager.

## Layer 1: role permissions (DocPerm)
| DocType | Admin | Author | Reviewer | Instructor | Learner |
|---|---|---|---|---|---|
| TCD Settings | RW | - | - | - | - |
| TCD Space | full | R | R | R | R |
| TCD Category | full | CRW | R | R | R |
| TCD Content | full | CRW | RW | R | R |
| TCD Content Relation | full | CRWD | R | R | R |
| TCD Content Version | R, D | R | R | R | - |
| TCD Quiz | full | CRW | RW | R | - (API only) |
| TCD Course / TCD Learning Path | full | CRW | RW | R | R |
| TCD Chapter | full | CRWD | RW | R | R |
| TCD Enrollment | full | R | R | CRW | R (own; self-enroll via API) |
| TCD Batch | full | - | R | CRWD | - |
| TCD Assignment | full | CRW | RW | CRW | R (via content) |
| TCD Assignment Submission | full | - | - | RW (own courses) | R (own; submit via API) |
| TCD Course Feedback | full | R | R | R (own courses) | R (own; via API) |
| TCD Progress | R, D | - | - | R | R (own) |
| TCD Quiz Submission | R, D | R | R | R | R (own) |

Content versions, progress and quiz submissions are created only by the system and can never be edited by users.
Learners have no read access to TCD Quiz because it holds the correct answers; they use `api.get_quiz`
(questions without answers) and `api.submit_quiz` (server-side grading).

## Layer 2: space access (`core/permissions.py`)
- Inactive space: admins only
- Public: everyone; Internal: staff only; Restricted: users with one of the space's allowed roles

## Layer 3: content visibility
- Public: everyone with space access
- Internal: staff only
- Restricted: users with one of the space's allowed roles, plus the owner
- Learners (non-staff) see Published content only

Layers 2-3 are applied in both `has_permission` (single doc) and
`permission_query_conditions` (lists/reports/search), for Space, Category, Content,
Relation (both ends), Version and Quiz (through their content).
Progress and Quiz Submission: users see their own rows; staff also see rows for content they can access.

## Courses (Phase 1)
- Course and Learning Path use the same space + visibility + status rules as TCD Content (learners: Published only).
- Chapters follow their course. Enrollments: own rows, plus staff for courses/paths they can read.
- Approving a Pending Approval enrollment: an instructor of that course, or admin (`api.approve_enrollment`).
- Instructor scope: enrollment, submission and feedback rows are visible to the learner, the instructors of the
  course/path, and admins only.
- Enrolled Only courses: their lessons are hidden from non-enrolled learners in `has_permission` and list queries.

## Phase 2
- Relations: visible only when the source content and the target (content, course or path) are both readable.
- Search results, "used in" lists, related items and recommendations are built from permission-filtered queries
  (`get_list` / `has_permission`), never from `ignore_permissions` lists shown to the user.

## Phase 4: assessments
- TCD Question and TCD Question Category: staff only (Author, Reviewer, Instructor, Admin). Learners never read the
  bank; they receive question payloads without answers from `api.get_quiz` / `api.start_quiz`.
- Manual review (`api.review_quiz_submission`): admins, TCD Content Reviewer, or instructors of a course that contains
  the quiz's content.

## Phase 5: skills and certificates
- TCD Skill: everyone with a TCD role reads; admins and authors manage. Competency profiles: admins manage, staff read.
- TCD User Skill and TCD Certificate: the owner (user), instructors of the course/path that produced them, admins.
- `/verify/<code>`: public, read-only, minimal fields; unknown codes return 404.

## Phase 6: governance
- TCD Governance Document: staff only in Desk (Author create/edit, Reviewer review, admins all). Learners read the
  Active snapshot through `/learn/policies` and the API, filtered by audience.
- Transitions: Review → Approval needs TCD Content Reviewer (or admin); Approval → Active needs the named approver
  or an admin.
- TCD Acknowledgment: created only through `api.acknowledge`; the user reads own rows; admins and reviewers read all.

## Phase 8: integrations and training rules
- TCD Connector: System Manager and TCD Administrator only. The secret is a Password field (never returned to the
  client). "Send Test" needs write permission on the connector.
- TCD Integration Event: read/delete for the same roles; nobody creates or edits it by hand (outbox written by the
  services). Retry needs write permission on its connector. Payloads contain user ids, so learners never see them.
- TCD Training Rule: admins full; TCD Instructor read only. "Apply Now" needs write permission on the rule.
- Rule enrollments go through `courses.enroll`, so the course/path access check (space, visibility, roles) still
  applies; a user who cannot access the course is skipped and an Error Log is written.
- TCD Training Compliance report: System Manager, TCD Administrator, TCD Instructor; rows come from `get_list`, so
  instructors see only enrollments their permission layer allows.
- Role guides on /learn/my are filtered by `can_access_content` and Published status.

## Phase 9: AI gateway
- TCD AI Settings and TCD AI Usage Log: System Manager and TCD Administrator only (the API key is a Password field).
- Assistant and smart search: users with an allowed role (default: any TCD role); Guests never.
- Retrieval runs as the asking user (`get_list`) plus a per-page read check before any page is sent to a provider.
- Summaries: only pages the user may read (and that the privacy settings allow).
- Quiz questions: need create permission on TCD Question; saved as "Needs Review", unusable in quizzes until reviewed.
- Lesson drafts: need create permission on TCD Content and read on the space; inserted with normal permissions.

## Phase 10: code runner
- `api.run_code`: logged-in users only, per-user runs per minute; `api.test_runner`: write on TCD Settings.
- TCD Code Run: System Manager and TCD Administrator read/delete; stores a hash, not the code.
- Grading output comes from the runner only; a learner cannot supply it.

## Phase 12
- TCD Session: admins full; TCD Instructor create/read/write only for sessions of courses they instruct (or where
  they are the session instructor); reviewers read. Learners have no Desk access; they see their sessions through
  the portal, and the meeting link only when invited.
- TCD Discussion Post: created only by `api.discussion_post` for readers of a published page; Desk edits limited to
  moderation (hidden); moderators = page owner, instructors of courses using the page, reviewers, admins.
- `api.withdraw`: own enrollment only, not mandatory, not completed. `api.confirm_content_review`: write on the page.
- Reports: TCD Attendance (admins, instructors — rows from their sessions only), TCD Content Freshness (admins,
  reviewers).

## Phase 13
- `/learn/team` and `api.team_overview`: managers of a TCD Team (or with HRMS direct reports) see training status of
  those people only; admins any team. TCD Team and TCD Content Import: admins only.
- `api.export_space` / `api.run_content_import`: administrators only (bundles include quiz answers).

## Phase 14
- TCD Lesson Note: no role permissions; only the author reads/writes through `api.save_note` and the page.
- TCD Change Request: proposed by readers of the published page (`api.propose_change`); accepted or rejected by
  TCD Content Reviewer / admins only; authors and reviewers read the list; learners cannot read it in the Desk.
- `api.video_progress`: logged-in readers of the page.

## Phase 15
- TCD Quiz Violation: admins read/delete, instructors read; created only by `api.report_quiz_violation` for the
  user's own open attempt.
- TCD Badge: admins manage, everyone with a TCD role reads; TCD Badge Award: admins manage, instructors read,
  learners see their own in My Learning.

## Phase 16
- Guest: read role on portal DocTypes, narrowed by `guest_allowed()` (setting on + portal render, never `/api/`) to
  published Public content in Public spaces; never write.
- TCD Payment: admins read; created only by checkout; the gateway confirms through `on_payment_authorized`.
- TCD Coupon: admins. SCORM upload and GitHub sync: administrators only.
- TCD Learner Profile: owner edits through the portal; others see it only when shared. TCD Job Application: admins
  and the job's hiring manager (`application_has_permission` / `application_query`).

## Phase 18 — studio
- `/learn/studio*`: only users with create/write on TCD Content or write on TCD Course; others get 404.
- Saves use the normal DocType permissions and validations (no `ignore_permissions`); reviewers alone approve
  and publish when review is required. Course items must be readable by the author.
- Portal page and breadcrumb titles are escaped in `portal_page`.

## Reports (P4)
TCD Learner Progress and TCD Quiz Analytics: System Manager, TCD Administrator, TCD Instructor, TCD Content Reviewer.
Rows come from `get_list`, so the space/visibility layers apply; Quiz Analytics also checks read access on the quiz.

## Portal (P3)
`/learn` pages use the same checks (`frappe.has_permission` / `get_list`), so a page shows exactly what the API allows.
Guests are redirected to login; anything not readable is a 404.

Rule: extra layers only restrict further; they never bypass Frappe permissions.
Every phase ships a permission test (`tests/test_p1.py`, `tests/test_p2.py`, `tests/test_p3.py`, `tests/test_p4.py`).
