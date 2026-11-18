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

Rule: extra layers only restrict further; they never bypass Frappe permissions.
Every phase ships a permission test (`tests/test_p1.py`, `tests/test_p2.py`).
