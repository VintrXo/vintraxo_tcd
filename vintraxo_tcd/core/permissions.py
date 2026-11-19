"""Space- and visibility-level access for TCD documents.

These hooks only restrict: Frappe role permissions (DocPerm) are checked first and
nothing here can grant access that DocPerm does not.

Space access
  - Admins (System Manager, TCD Administrator, Administrator): everything
  - Inactive space: admins only
  - Public: every user with a TCD read permission
  - Internal: staff only (Author, Reviewer, Instructor)
  - Restricted: users holding one of the space's allowed roles

Content visibility (inside an accessible space)
  - Public: everyone with space access
  - Internal: staff only
  - Restricted: users holding one of the space's allowed roles, plus the owner
  - Non-staff users (learners) only ever see Published content
"""

import frappe

ADMIN_ROLES = {"System Manager", "TCD Administrator"}
STAFF_ROLES = {"TCD Content Author", "TCD Content Reviewer", "TCD Instructor"} | ADMIN_ROLES


def _roles(user: str) -> set:
	return set(frappe.get_roles(user))


def is_admin(user: str) -> bool:
	return user == "Administrator" or bool(_roles(user) & ADMIN_ROLES)


def is_staff(user: str) -> bool:
	return bool(_roles(user) & STAFF_ROLES)


def guest_allowed() -> bool:
	"""Visitors may read only while a portal page is rendered, when the site allows it. Any API request
	(/api/...) gets nothing, so records (with owner e-mails etc.) never leave through REST."""
	if not frappe.db.get_single_value("TCD Settings", "enable_guest_access"):
		return False
	request = getattr(frappe.local, "request", None)
	path = getattr(request, "path", "") or ""
	return not path.startswith("/api/")


def _space_access(user: str) -> tuple[set, set]:
	"""Return (accessible spaces, spaces where the user holds an allowed role)."""
	if user == "Guest" and not guest_allowed():
		return set(), set()
	roles = _roles(user)
	staff = bool(roles & STAFF_ROLES)

	spaces = frappe.get_all(
		"TCD Space", filters={"is_active": 1}, fields=["name", "visibility"], ignore_permissions=True
	)
	role_rows = frappe.get_all(
		"TCD Space Role",
		filters={"parenttype": "TCD Space", "role": ("in", list(roles) or [""])},
		fields=["parent"],
		ignore_permissions=True,
	)
	role_spaces = {r.parent for r in role_rows}

	accessible = set()
	for s in spaces:
		if (
			s.visibility == "Public"
			or (s.visibility == "Internal" and staff)
			or (s.visibility == "Restricted" and s.name in role_spaces)
		):
			accessible.add(s.name)
	return accessible, role_spaces & accessible


def accessible_spaces(user: str) -> set | None:
	"""None means unrestricted."""
	if is_admin(user):
		return None
	return _space_access(user)[0]


def can_access_content(doc, user: str) -> bool:
	if is_admin(user):
		return True
	if user == "Guest" and (
		doc.get("visibility") != "Public" or doc.get("status") not in (None, "Published")
	):
		return False
	accessible, role_spaces = _space_access(user)
	if doc.space not in accessible:
		return False
	staff = is_staff(user)
	if not staff and doc.status != "Published":
		return False
	if doc.visibility == "Internal":
		return staff
	if doc.visibility == "Restricted" and not (doc.space in role_spaces or doc.owner == user):
		return False
	if not staff and doc.doctype == "TCD Content" and doc.name in gated_contents(user):
		return False
	return True


# ---------------------------------------------------------------- SQL helpers


def _in(column: str, values) -> str:
	if not values:
		return "1=0"
	return f"{column} in ({', '.join(frappe.db.escape(v) for v in sorted(values))})"


def _content_condition(
	user: str, table: str = "`tabTCD Content`", enrollment_gate: bool | None = None
) -> str:
	if is_admin(user):
		return ""
	accessible, role_spaces = _space_access(user)
	if not accessible:
		return "1=0"
	if enrollment_gate is None:
		enrollment_gate = table in ("`tabTCD Content`", "c")

	space_cond = _in(f"{table}.space", accessible)
	restricted = f"({table}.visibility = 'Restricted' and ({_in(f'{table}.space', role_spaces)} or {table}.owner = {frappe.db.escape(user)}))"

	if is_staff(user):
		vis = f"({table}.visibility in ('Public', 'Internal') or {restricted})"
		return f"({space_cond} and {vis})"

	vis = f"({table}.visibility = 'Public' or {restricted})"
	gate = ""
	if enrollment_gate:
		blocked = gated_contents(user)
		if blocked:
			gate = f" and {table}.name not in ({', '.join(frappe.db.escape(n) for n in sorted(blocked))})"
	return f"({space_cond} and {table}.status = 'Published' and {vis}{gate})"


# ---------------------------------------------------------------- enrollment gate (ADR-0008)


def _contents_of_courses(courses) -> set:
	if not courses:
		return set()
	chapters = frappe.get_all(
		"TCD Chapter", filters={"course": ("in", list(courses))}, pluck="name", ignore_permissions=True
	)
	if not chapters:
		return set()
	return set(
		frappe.get_all(
			"TCD Learning Item",
			filters={"parenttype": "TCD Chapter", "parent": ("in", chapters)},
			pluck="content",
			ignore_permissions=True,
		)
	)


def gated_contents(user: str) -> set:
	"""Contents a learner may not open: used only by Enrolled Only courses the learner is not enrolled in."""
	enrolled_only = set(
		frappe.get_all(
			"TCD Course", filters={"access": "Enrolled Only"}, pluck="name", ignore_permissions=True
		)
	)
	if not enrolled_only:
		return set()
	open_courses = set(
		frappe.get_all(
			"TCD Course", filters={"access": ("!=", "Enrolled Only")}, pluck="name", ignore_permissions=True
		)
	)
	restricted = _contents_of_courses(enrolled_only) - _contents_of_courses(open_courses)
	if not restricted:
		return set()
	mine = set(
		frappe.get_all(
			"TCD Enrollment",
			filters={"user": user, "course": ("is", "set"), "status": ("!=", "Withdrawn")},
			pluck="course",
			ignore_permissions=True,
		)
	)
	return restricted - _contents_of_courses(mine & enrolled_only)


# ---------------------------------------------------------------- permission_query_conditions


def space_query(user=None, doctype=None):
	user = user or frappe.session.user
	spaces = accessible_spaces(user)
	return "" if spaces is None else _in("`tabTCD Space`.name", spaces)


def category_query(user=None, doctype=None):
	user = user or frappe.session.user
	spaces = accessible_spaces(user)
	return "" if spaces is None else _in("`tabTCD Category`.space", spaces)


def content_query(user=None, doctype=None):
	return _content_condition(user or frappe.session.user)


def _via_content(column: str, user: str) -> str:
	cond = _content_condition(user, "c")
	if not cond:
		return ""
	return f"{column} in (select c.name from `tabTCD Content` c where {cond})"


def relation_query(user=None, doctype=None):
	user = user or frappe.session.user
	table = "`tabTCD Content Relation`"
	source = _via_content(f"{table}.from_content", user)
	if not source:
		return ""
	targets = " or ".join(
		[
			f"({table}.target_type = 'Content' and {_via_content(f'{table}.to_content', user)})",
			f"({table}.target_type = 'Course' and {_via('TCD Course', f'{table}.to_course', user)})",
			f"({table}.target_type = 'Learning Path' and {_via('TCD Learning Path', f'{table}.to_learning_path', user)})",
		]
	)
	return f"({source} and ({targets}))"


def version_query(user=None, doctype=None):
	return _via_content("`tabTCD Content Version`.content", user or frappe.session.user)


# ---------------------------------------------------------------- has_permission (must return a bool)


def space_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	spaces = accessible_spaces(user)
	return spaces is None or doc.name in spaces or doc.is_new()


def category_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	spaces = accessible_spaces(user)
	return spaces is None or not doc.space or doc.space in spaces


def content_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if doc.is_new() and not doc.space:
		return True
	return can_access_content(doc, user)


def _content_doc_ok(name, user) -> bool:
	if not name:
		return True
	if not frappe.db.exists("TCD Content", name):
		return True  # let link validation report it
	return can_access_content(frappe.get_cached_doc("TCD Content", name), user)


def relation_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if is_admin(user):
		return True
	if not _content_doc_ok(doc.from_content, user):
		return False
	target_type = doc.get("target_type") or "Content"
	if target_type == "Course":
		return _offering_ok("TCD Course", doc.to_course, user)
	if target_type == "Learning Path":
		return _offering_ok("TCD Learning Path", doc.to_learning_path, user)
	return _content_doc_ok(doc.to_content, user)


def version_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	return is_admin(user) or _content_doc_ok(doc.content, user)


# ---------------------------------------------------------------- P2: quiz, progress, submissions


def quiz_query(user=None, doctype=None):
	return _via_content("`tabTCD Quiz`.content", user or frappe.session.user)


def quiz_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	return is_admin(user) or _content_doc_ok(doc.content, user)


def _own_or_staff(table: str, user: str) -> str:
	if is_admin(user):
		return ""
	own = f"{table}.user = {frappe.db.escape(user)}"
	if not is_staff(user):
		return own
	return f"({own} or {_via_content(f'{table}.content', user)})"


def progress_query(user=None, doctype=None):
	return _own_or_staff("`tabTCD Progress`", user or frappe.session.user)


def submission_query(user=None, doctype=None):
	return _own_or_staff("`tabTCD Quiz Submission`", user or frappe.session.user)


def own_or_staff_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if is_admin(user) or doc.user == user:
		return True
	return is_staff(user) and _content_doc_ok(doc.content, user)


def has_app_permission():
	"""Show the app on the apps screen / desk to TCD staff only (learners use the portal)."""
	user = frappe.session.user
	return user != "Guest" and (is_admin(user) or is_staff(user))


# ---------------------------------------------------------------- Phase 1: courses, paths, enrollments
# Course and Learning Path carry the same space / visibility / status / owner fields as TCD Content,
# so the same rules apply to them.


def course_query(user=None, doctype=None):
	return _content_condition(user or frappe.session.user, "`tabTCD Course`", enrollment_gate=False)


def path_query(user=None, doctype=None):
	return _content_condition(user or frappe.session.user, "`tabTCD Learning Path`", enrollment_gate=False)


def offering_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if doc.is_new() and not doc.space:
		return True
	return can_access_content(doc, user)


def _via(doctype: str, column: str, user: str) -> str:
	cond = _content_condition(user, "c", enrollment_gate=doctype == "TCD Content")
	if not cond:
		return ""
	return f"{column} in (select c.name from `tab{doctype}` c where {cond})"


def chapter_query(user=None, doctype=None):
	return _via("TCD Course", "`tabTCD Chapter`.course", user or frappe.session.user)


def _offering_ok(doctype: str, name: str | None, user: str) -> bool:
	if not name or not frappe.db.exists(doctype, name):
		return True  # link validation reports it
	return can_access_content(frappe.get_cached_doc(doctype, name), user)


def chapter_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	return is_admin(user) or _offering_ok("TCD Course", doc.course, user)


def instructed(user: str, doctype: str) -> set:
	"""Courses or learning paths where `user` is listed as instructor."""
	parents = set(
		frappe.get_all(
			"TCD Course Instructor",
			filters={"parenttype": doctype, "user": user},
			pluck="parent",
			ignore_permissions=True,
		)
	)
	if not parents:
		return parents
	# ignore rows left behind by deleted parents
	return set(
		frappe.get_all(
			doctype, filters={"name": ("in", list(parents))}, pluck="name", ignore_permissions=True
		)
	)


def is_instructor_of(user: str, course: str | None = None, path: str | None = None) -> bool:
	if is_admin(user):
		return True
	if course and course in instructed(user, "TCD Course"):
		return True
	return bool(path and path in instructed(user, "TCD Learning Path"))


def enrollment_query(user=None, doctype=None):
	user = user or frappe.session.user
	if is_admin(user):
		return ""
	table = "`tabTCD Enrollment`"
	parts = [f"{table}.user = {frappe.db.escape(user)}"]
	courses = instructed(user, "TCD Course")
	paths = instructed(user, "TCD Learning Path")
	if courses:
		parts.append(_in(f"{table}.course", courses))
	if paths:
		parts.append(_in(f"{table}.learning_path", paths))
	return "(" + " or ".join(parts) + ")"


def enrollment_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	return doc.user == user or is_instructor_of(user, doc.course, doc.learning_path)


# ---------------------------------------------------------------- assignments and feedback


def assignment_query(user=None, doctype=None):
	return _via_content("`tabTCD Assignment`.content", user or frappe.session.user)


def assignment_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	return is_admin(user) or _content_doc_ok(doc.content, user)


def _own_or_course_instructor(table: str, user: str) -> str:
	if is_admin(user):
		return ""
	parts = [f"{table}.user = {frappe.db.escape(user)}"]
	courses = instructed(user, "TCD Course")
	if courses:
		parts.append(_in(f"{table}.course", courses))
	return "(" + " or ".join(parts) + ")"


def submission_scope_query(user=None, doctype=None):
	return _own_or_course_instructor("`tabTCD Assignment Submission`", user or frappe.session.user)


def feedback_query(user=None, doctype=None):
	return _own_or_course_instructor("`tabTCD Course Feedback`", user or frappe.session.user)


def own_or_course_instructor_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	return doc.user == user or is_instructor_of(user, doc.course)


def content_feedback_query(user=None, doctype=None):
	user = user or frappe.session.user
	if is_admin(user):
		return ""
	table = "`tabTCD Content Feedback`"
	own = f"{table}.user = {frappe.db.escape(user)}"
	if not is_staff(user):
		return own
	return f"({own} or {_via_content(f'{table}.content', user)})"


def content_feedback_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if is_admin(user) or doc.user == user:
		return True
	return is_staff(user) and _content_doc_ok(doc.content, user)


# ---------------------------------------------------------------- Phase 5: skills and certificates


def _learners_of_instructor(user: str) -> str | None:
	courses = instructed(user, "TCD Course")
	paths = instructed(user, "TCD Learning Path")
	parts = []
	if courses:
		parts.append(_in("e.course", courses))
	if paths:
		parts.append(_in("e.learning_path", paths))
	if not parts:
		return None
	return f"select e.user from `tabTCD Enrollment` e where {' or '.join(parts)}"


def user_skill_query(user=None, doctype=None):
	user = user or frappe.session.user
	if is_admin(user):
		return ""
	table = "`tabTCD User Skill`"
	own = f"{table}.user = {frappe.db.escape(user)}"
	learners = _learners_of_instructor(user)
	return f"({own} or {table}.user in ({learners}))" if learners else own


def user_skill_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if is_admin(user) or doc.user == user:
		return True
	learners = _learners_of_instructor(user)
	return bool(learners) and bool(
		frappe.db.sql(f"select 1 from ({learners}) t where t.user = %s limit 1", doc.user)
	)


def certificate_query(user=None, doctype=None):
	user = user or frappe.session.user
	if is_admin(user):
		return ""
	table = "`tabTCD Certificate`"
	parts = [f"{table}.user = {frappe.db.escape(user)}"]
	courses = instructed(user, "TCD Course")
	paths = instructed(user, "TCD Learning Path")
	if courses:
		parts.append(_in(f"{table}.course", courses))
	if paths:
		parts.append(_in(f"{table}.learning_path", paths))
	return "(" + " or ".join(parts) + ")"


def certificate_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	return doc.user == user or is_instructor_of(user, doc.course, doc.learning_path)


# ---------------------------------------------------------------- Phase 6: governance


def acknowledgment_query(user=None, doctype=None):
	user = user or frappe.session.user
	if is_admin(user) or "TCD Content Reviewer" in frappe.get_roles(user):
		return ""
	return f"`tabTCD Acknowledgment`.user = {frappe.db.escape(user)}"


def acknowledgment_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	return doc.user == user or is_admin(user) or "TCD Content Reviewer" in frappe.get_roles(user)


def readable_list(doctype: str, **kwargs) -> list:
	"""`frappe.get_list` for a page section: a role with no read permission on `doctype` (e.g. an author
	opening the portal) gets an empty section instead of a failing page. Still only restricts."""
	if not frappe.has_permission(doctype, "read"):
		return []
	return frappe.get_list(doctype, **kwargs)
