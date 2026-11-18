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

## Decisions
- One lesson entity, reused by tutorials and courses: TCD Content with content_type = Lesson
- Blocks stored as JSON with a fixed schema; `search_text` derived on save
- Avoid Dynamic Link where a plain Link works
