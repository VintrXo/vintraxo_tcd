# DATA MODEL

## P0 (done)
- TCD Settings (Single): default_language, enable_portal, default_visibility,
  require_approval_before_publish, enable_playgrounds, playground_timeout_seconds,
  pyodide_index_url, sqljs_base_url (P3; https:// or / only, normalized to end with /)

## P1 (done)
| DocType | Naming | Key fields |
|---|---|---|
| TCD Space | `space_name` (lowercase id) | title, visibility (Public/Internal/Restricted), is_active, allowed_roles |
| TCD Space Role (child) | - | role |
| TCD Category | hash | category_name, space, parent_category, sort_order |
| TCD Content | hash | title, slug, content_type, status, language, visibility, space, category, summary, blocks, search_text, current_version, approved_by/on, published_on |
| TCD Content Relation | hash | from_content, relation_type (Prerequisite/Next/Related/See Also), to_content |
| TCD Content Version | `{content}-v{n}` | content, version_number, title, language, summary, blocks, search_text, approved_by/on |

### Rules
- Space ID: 2-80 chars `[a-z0-9_-]`; a space with content cannot be deleted.
- Category: same space as its parent, no loops, unique name per parent.
- Content: category must be in the same space; slug is generated from the title
  (keeps Arabic letters) and is unique per space; language/visibility default from TCD Settings.
- Relation: no self-relation, no duplicates, no reverse Prerequisite/Next pair.
- Deleting content removes its relations and versions.

### Blocks (`TCD Content.blocks`, JSON list)
| type | required | optional |
|---|---|---|
| heading | text | level (1-4) |
| paragraph | text | - |
| code | code | language |
| callout | text | variant (info/tip/warning/danger), title |
| list | items (list of text) | ordered |
| image | url (http(s) or /) | alt, caption |
| playground | language (python/sql/html/javascript), code | expected_output |

Unknown keys are dropped on save. `search_text` = title + summary + block text,
Arabic-normalized (`core/search.py`: no diacritics/tatweel, unified alef/yeh/heh, ASCII digits, lowercase).

### Review workflow
```
Draft -> In Review -> Approved -> Published -> Archived
  ^          |            |           |           |
  +----------+------------+-----------+-----------+   (back to Draft to edit)
```
- Approve / publish: TCD Content Reviewer or admin.
- `require_approval_before_publish = 0` allows Draft -> Published directly (any author).
- Every approval (or direct publish) creates an immutable TCD Content Version and sets `current_version`.
- Approved/Published content is locked (title, summary, blocks, language); move it to Draft to edit.

## P2 (done): tutorials, progress, quizzes
| DocType | Naming | Key fields |
|---|---|---|
| TCD Tutorial Lesson (child of TCD Content) | - | lesson, lesson_title, is_optional |
| TCD Progress | hash | user, content, content_type, space, status (In Progress/Completed), percent, started/last_viewed/completed_on |
| TCD Quiz | hash | title, content, pass_percentage, max_attempts (0 = unlimited), required_to_complete, shuffle_questions, show_answers_after_submit, is_active, questions |
| TCD Quiz Question (child) | - | question, question_type (Single Choice/Multiple Choice/True False), options (one per line), correct_answers ("2" or "1,3"), points, explanation |
| TCD Quiz Submission | hash | quiz, content, user, attempt, answers (JSON), score, max_score, percentage, passed |

### Rules
- A Tutorial is TCD Content with content_type = Tutorial; its lessons are TCD Content of type Lesson
  in the same space, no duplicates. The ordered lesson list is locked once approved and saved in each version.
- Progress is written only by `core/progress.py`: viewing marks In Progress, completing marks Completed
  (never downgraded). A lesson with an active required quiz completes only after a passed attempt.
- Tutorial progress is derived: percent of required (non-optional) lessons the user can see;
  Completed when all are done.
- Quiz grading runs on the server (`core/quiz.py`); a question scores only on an exact answer match.
  Submissions are immutable; passing a required quiz completes its content.
- Playground blocks are removed from `get_lesson` output when TCD Settings > Enable Playgrounds is off.

## Phase 1 (R2): courses, paths, enrollment, cohorts
| DocType | Naming | Key fields |
|---|---|---|
| TCD Course | hash | title, slug, space, category, language, visibility, status (Draft/Published/Archived), summary, completion_rule, minimum_score, self_enrollment |
| TCD Chapter | hash | course, title, sort_order, items (TCD Learning Item) |
| TCD Learning Path | hash | title, slug, space, language, visibility, status, summary, completion_rule, minimum_score, self_enrollment, items (TCD Learning Item) |
| TCD Learning Item (child) | - | content (Link TCD Content, in chapters), course (Link TCD Course, in paths), is_optional |
| TCD Enrollment | hash | user, enrollment_for (Course/Learning Path), course, learning_path, batch, status (Active/Pending Approval/Completed/Withdrawn), percent, score, enrolled_on, due_date, completed_on, approved_by, approved_on |
| TCD Batch (was TCD Student Group) | group_name | batch name, is_active, start_date, end_date, description, members (TCD Batch Member) |
| TCD Batch Member (child) | - | user, full_name |

### Rules
- Lessons stay one entity: chapter items are TCD Content (Lesson, Article or Reference; never Tutorial) in the course space,
  each content at most once per course. Path items are courses of the same space, no duplicates.
- Publishing a course/path needs a reviewer when approval is required, and every required item must already be Published.
- Completion rules (course and path):
  - **All Items**: every required item completed.
  - **Required Sequence**: same, and a required item can only be completed after the previous required items of every
    sequence course the learner is actively enrolled in.
  - **Manual Approval**: when all required items are done the enrollment becomes Pending Approval; an instructor approves.
  - **Minimum Score**: all required items done and the average best quiz score over the course quizzes >= minimum_score
    (no quizzes = satisfied).
- Roll-up: lesson (TCD Progress) -> chapter (computed) -> course enrollment (percent, score, status) -> path enrollment
  (required courses completed). Triggered on lesson completion and quiz grading.
- Enrollment is unique per user and course/path. Enrolling in a path also enrolls in its courses. Self-enrollment only
  when the course/path allows it and is readable; staff can enroll users or a whole student group.

## Phase 1 completion (LMS core)
| DocType / field | Key fields |
|---|---|
| TCD Course: `access` | Open / Enrolled Only |
| TCD Course: `instructors` (TCD Course Instructor child) | user, full_name |
| TCD Learning Path: `instructors` | same child |
| TCD Content: `lesson_type` (Lesson only) | Article, Video, Interactive Tutorial, Playground, Quiz, Assignment, External, Project, Document |
| New blocks | `video` (url, title, caption → embed_url), `link` (url, title, description), `file` (url to an uploaded File, title) |
| TCD Settings | video_domains, allowed_file_extensions, max_upload_mb |
| TCD Assignment | title, content, course, instructions, submission_type (Text / File / Text and File), max_score, pass_score, due_date, allowed_extensions, required_to_complete, is_active |
| TCD Assignment Submission | assignment, user, content, course, answer_text, attachment, status (Submitted / Returned / Graded), score, passed, feedback, submitted_on, graded_by, graded_on |
| TCD Course Feedback | course, user, rating (1-5), comment |

### Rules
- **Enrolled Only**: a content item is restricted when every course containing it is Enrolled Only; learners then need an
  enrollment (any status but Withdrawn) in one of those courses. Staff are not affected. The course page stays visible.
- **Instructor scope**: enrollments, submissions and feedback of a course are visible to its instructors (and admins);
  other staff no longer see them. Approve/grade only on courses you instruct.
- **Video block**: host must be in TCD Settings > video_domains (YouTube, Vimeo by default) or an uploaded file under
  `/files/` (mp4/webm). Rendered as a privacy-friendly embed (youtube-nocookie) in a sandboxed iframe.
- **Uploads** (file block, submissions): must reference an existing File document, extension in the allowed list, size
  under max_upload_mb; submissions use private files owned by the learner.
- **Assignments**: one submission per learner; editable while Submitted/Returned, locked when Graded. Graded with
  score ≥ pass_score passes; a required assignment must pass before its lesson can be completed (like a required quiz).
- **Feedback**: one rating per learner per course, only when enrolled.

## Phase 2: unified experience
| DocType / field | Key fields |
|---|---|
| TCD Content Relation (extended) | from_content, relation_type, target_type (Content / Course / Learning Path), to_content, to_course, to_learning_path, sort_order |
| TCD Course: `prerequisites` (TCD Course Prerequisite child) | course |
| TCD Course / TCD Learning Path: `search_text` | derived on save (title, summary, chapter titles / course titles), Arabic-normalized |

### Rules
- Relation direction: **from_content → target**. `Prerequisite` means "from_content requires the target"; `Next` means
  "after from_content, go to the target". Exactly one target field is set, matching target_type.
- A relation is visible only when both ends are readable.
- Prerequisites are enforced for learners (staff are not blocked):
  - content: a lesson cannot be completed while a prerequisite (content completed / course or path enrollment
    Completed) is missing; the page shows what is missing.
  - course: self-enrollment is refused while a prerequisite course is not Completed; staff enrollment is allowed and
    reported as a warning.
- Unified search: content, courses and learning paths in one ranked, permission-filtered list with type and space filters.
- Recommendations (simple, explainable): next unlocked item of active enrollments, Next/Related targets of completed
  content, popular self-enrollable courses in the learner's spaces.

## Phase 3: wiki completion
| DocType / field | Key fields |
|---|---|
| TCD Content: `parent_content` | page tree inside a space (articles/references/lessons), no cycles |
| TCD Content: `internal_links` | derived JSON list of content names linked with `[[...]]` (backlinks) |
| New block `markdown` | text (Markdown, rendered server-side and sanitized) |
| TCD Content Template | template_name, content_type, lesson_type, description, blocks |
| TCD Content Feedback | content, user, helpful, comment (one per user and content) |
| Tags | Frappe's native tags (`Tag Link`) on TCD Content; shown and filterable in the portal |

### Rules
- Internal links: `[[slug]]` (same space), `[[space/slug]]`, optional label `[[slug|label]]`, inside paragraph,
  callout and markdown text. Rendered as links only when the target exists and is readable; otherwise the label
  is shown as plain text.
- Markdown is converted with `frappe.utils.md_to_html` and then `sanitize_html(always_sanitize=True)` with
  link/meta/style/iframe/form tags disallowed.
- Compare: any two versions (or a version and the current draft), block by block, as a unified text diff.
- Restore: copies a version's title, summary, blocks and lessons into the content and moves it to Draft (normal
  review applies again). Needs write permission.
- Archived content is hidden from learners (only Published is visible to them); staff see an archive banner.

## Phase 4: assessment engine
| DocType / field | Key fields |
|---|---|
| TCD Question Category | category_name, parent_category, description |
| TCD Question (bank) | question, scenario, question_type, category, points, options, correct_answers, accepted_answers, pairs, code_language, starter_code, setup_code, expected_output, manual_review, allowed_extensions, rubric (TCD Rubric Criterion), explanation |
| TCD Rubric Criterion (child) | criterion, max_points |
| TCD Quiz: new fields | time_limit_minutes, shuffle_options, bank_items (TCD Quiz Bank Item: question or category + pick_count) |
| TCD Quiz Submission: new fields | status (In Progress / Pending Review / Graded), started_on, submitted_on, deadline, paper, review, graded_by, graded_on |

### Question types and grading
| Type | Learner answers | Grading |
|---|---|---|
| Single / Multiple Choice, True False | option numbers (original numbering, display may be shuffled) | exact match |
| Fill Blank | one text per blank; `accepted_answers` = one line per blank, alternatives separated by `|` | per blank, Arabic-normalized |
| Matching | right item for each left item; `pairs` = lines `left => right` | per pair |
| Ordering | items in order; `options` = correct order | per position |
| Short Answer | text; `accepted_answers` = accepted lines | auto when accepted answers exist, else manual |
| Essay, File | text / uploaded file | manual (rubric) |
| Code (python/javascript), SQL | code + output produced by the in-browser runtime | output compared with `expected_output`; manual when `manual_review` (ADR-0013) |
| Scenario | any type with a `scenario` text shown above the question | as its type |

- An attempt starts with `api.start_quiz`: the paper (question keys, random picks, option order) and the deadline are
  fixed then. Submitting after deadline + 60 s grace is refused and the attempt is closed with what was saved.
- Points are weights; percentage = score / max_score. Attempts with manual items stay **Pending Review** until an
  instructor of a course containing the quiz's content (or an admin/reviewer) reviews them; then pass/fail and
  lesson completion are applied.

## Phase 5: skills and certificates
| DocType / field | Key fields |
|---|---|
| TCD Skill | skill_name, skill_group, description |
| TCD Skill Award (child of TCD Course / TCD Learning Path) | skill, level (1-5) |
| TCD User Skill | user, skill, level, source_type (Course / Learning Path / Manual), source_name, awarded_on, verified_by |
| TCD Competency Profile | profile_name, role (Link Role, optional), description, requirements (TCD Competency Requirement: skill, required_level) |
| TCD Course / TCD Learning Path: certificate fields | issue_certificate, certificate_validity_months (0 = no expiry) |
| TCD Certificate | naming CERT-.YYYY.-.#####; user, full_name, certificate_for (Course / Learning Path), course, learning_path, title, issued_on, expires_on, status (Active / Expired / Revoked / Renewed), verification_code, revoked_reason, renewed_by |

### Rules
- Levels: 1 Beginner, 2 Basic, 3 Intermediate, 4 Advanced, 5 Expert. A user skill keeps the highest level earned;
  every award is idempotent per (user, skill).
- On enrollment completion (course or path): award its skills, then issue a certificate when `issue_certificate`
  is set and the user has no Active certificate for it.
- Expiry: a daily scheduler job marks certificates past `expires_on` as Expired. Renewal: an instructor/admin starts
  a renewal (enrollment back to Active, progress kept for history); completing again issues a new certificate and
  marks the old one Renewed.
- Verification: `/verify/<code>` (public, no login) shows holder name, title, dates and status only.
- Gap report: for a profile (and optionally a user), each requirement vs the user's level, plus courses that award
  the missing skill at the required level or higher.

## Phase 6: governance
| DocType | Key fields |
|---|---|
| TCD Governance Document | title, doc_kind (Document / Policy / SOP), code (unique), space, status (Draft / Review / Approval / Active / Revision / Archived), version, document_owner, approver, effective_date, expiry_date, review_cycle_months, next_review_date, summary, body (Markdown), attachment, require_acknowledgment, audience_roles (TCD Governance Role), audience_departments (TCD Governance Department, Data), links (TCD Governance Link: target_type Content / Course, content, course) |
| TCD Governance Version | governance_document, version, title, summary, body, attachment, effective_date, approved_by, approved_on (immutable snapshot) |
| TCD Acknowledgment | governance_document, version, user, acknowledged_on, statement (immutable audit log) |

### Rules
- Transitions: Draft → Review (owner/author) → Approval (reviewer) → Active (approver or admin; snapshot, version + 1,
  effective_date defaults to today, next_review_date = effective + review cycle) → Revision (editing; readers keep
  the last Active snapshot) → Review …; Active/Revision → Archived. Review/Approval can go back to Draft.
- Readers (learners) always see the latest snapshot, never the draft being revised.
- Audience: users holding any audience role; when departments are set and ERPNext's Employee exists, the user's
  Employee.department must match. Without ERPNext, departments are ignored (stored as text, ADR-0015).
- Acknowledgment: one per user per version; a new version needs a new acknowledgment.
- Scheduler (daily): Active documents past expiry move to Revision; documents whose review is due within 7 days get
  an open ToDo for the document owner (once per review date).

## Phase 7: notifications and analytics
No new DocTypes. Standard **Notification** records (System Notification channel, editable by admins) and
code-driven notification logs for recipients that depend on data.

| Event | Recipients | Mechanism |
|---|---|---|
| Content sent for review | TCD Content Reviewer role | Standard Notification (Value Change: status = In Review) |
| Governance document sent for review / approval | Reviewers / the named approver | Standard Notifications |
| Enrollment created | the learner | Standard Notification (New) |
| Enrollment due in 3 days | the learner | Standard Notification (Days Before due_date, Active only) |
| Certificate issued / expiring in 30 days | the learner | Standard Notifications |
| Assignment submitted, enrollment pending approval, quiz waiting for review | instructors of the course | `core/notify.py` (Notification Log, deduplicated) |
| New policy version requiring acknowledgment | the document audience | `core/notify.py` (enqueued, deduplicated) |

Reports: TCD Course Report (all courses: enrollments, completion, time to complete, overdue, rating),
TCD Knowledge Usage (per page: unique readers, completions, helpful %, backlinks), TCD Compliance Overview
(per acknowledged document + certificate expiries). Number cards on the VX workspace.

## Phase 8: integrations and training rules
| DocType | Purpose | Key fields |
|---|---|---|
| TCD Connector | Integration registry (admins) | connector_name (name), enabled, endpoint_url, payload_format (JSON/Slack), secret (Password), allow_private_network, events (TCD Connector Event), max_attempts, timeout_seconds, rate_limit_per_minute |
| TCD Connector Event (child) | Subscribed event | event (Enrollment Created/Completed, Certificate Issued/Revoked, Policy Activated/Acknowledged) |
| TCD Integration Event | Outbox + delivery log (read-only) | connector, event, status (Queued/Sent/Failed), attempts, next_attempt_on, sent_on, response_code, reference_doctype/name, payload (JSON), last_error |
| TCD Training Rule | Automatic / mandatory enrollment, role guides | title, enabled, target_type (Course/Learning Path/Content), course / learning_path / content, mandatory, due_in_days, roles (TCD Rule Role), hr_filters (TCD Rule HR Filter), last_applied_on |
| TCD Rule HR Filter (child) | HR criterion | filter_type (Department/Designation/Company), value (Data, validated against ERPNext when installed) |

TCD Enrollment gains `mandatory` and `training_rule` (read-only, set by rules).
Employee ↔ learner: ERPNext `Employee.user_id` (read only, guarded by `training.hr_available()`).

## Phase 9: AI gateway
| DocType | Purpose | Key fields |
|---|---|---|
| TCD AI Settings (single) | Provider and limits | enabled, provider, model, api_key (Password), effort, max_output_tokens, expand_queries, input/output price per million tokens, monthly_budget, daily_requests_per_user, exclude_restricted, redact_personal_data, log_prompts, allowed_roles (TCD Rule Role) |
| TCD AI Usage Log | One row per model call (read-only) | user, feature, status (Success/Refused/Error), provider, model, input/output tokens, cost, sources (JSON), reference_doctype/name, prompt (only if enabled), error |

TCD Content gains `ai_generated`; TCD Question gains `ai_status` (Needs Review / Reviewed) and `ai_source`.

## Phase 10: code runner client
| DocType | Purpose | Key fields |
|---|---|---|
| TCD Code Run | Log of every run on the runner (read-only, admins) | user, language, purpose (Practice/Grading), status, time_ms, memory_kb, code_hash, output, error, reference |
| TCD Runner Language (child of TCD Settings) | Language → runner id | language, label, runner_language_id |

TCD Settings gains the Code Runner section (enabled, URL, token, limits, languages). TCD Question gains
`grade_on_server`; `code_language` adds java, cpp, c, go, csharp, bash.

## Phase 12: sessions, discussions, freshness
| DocType | Purpose | Key fields |
|---|---|---|
| TCD Session | Classroom / online session of a course | title, course, batch, status (Scheduled/Completed/Cancelled), session_type, starts_on, ends_on, location, meeting_url, instructor, attendance (TCD Session Attendance) |
| TCD Session Attendance (child) | One learner's attendance | user, status (Present/Late/Absent/Excused), note |
| TCD Discussion Post | Question (no thread) or reply under a page | content, thread, user, body (plain text), status, is_staff_answer, accepted, hidden |

TCD Content gains content_owner, review_cycle_months, skip_review, last_reviewed_on, next_review_date.
TCD Settings gains default_review_months and enable_discussions.

## Phase 13
| DocType | Purpose | Key fields |
|---|---|---|
| TCD Team / TCD Team Member | A manager and the people they follow | team_name, manager, members (user) |
| TCD Content Import | One import of a space bundle | import_file, target_space, status, created_space, log |

TCD Course gains minimum_attendance; TCD Enrollment gains hr_training_event; TCD Settings gains sync_training_to_hr.

## Decisions
- One lesson entity, reused by tutorials and courses: TCD Content with content_type = Lesson
- Blocks stored as JSON with a fixed schema; `search_text` derived on save
- Avoid Dynamic Link where a plain Link works
