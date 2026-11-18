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


def _space_access(user: str) -> tuple[set, set]:
	"""Return (accessible spaces, spaces where the user holds an allowed role)."""
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
	accessible, role_spaces = _space_access(user)
	if doc.space not in accessible:
		return False
	staff = is_staff(user)
	if not staff and doc.status != "Published":
		return False
	if doc.visibility == "Internal":
		return staff
	if doc.visibility == "Restricted":
		return doc.space in role_spaces or doc.owner == user
	return True


# ---------------------------------------------------------------- SQL helpers


def _in(column: str, values) -> str:
	if not values:
		return "1=0"
	return f"{column} in ({', '.join(frappe.db.escape(v) for v in sorted(values))})"


def _content_condition(user: str, table: str = "`tabTCD Content`") -> str:
	if is_admin(user):
		return ""
	accessible, role_spaces = _space_access(user)
	if not accessible:
		return "1=0"

	space_cond = _in(f"{table}.space", accessible)
	restricted = f"({table}.visibility = 'Restricted' and ({_in(f'{table}.space', role_spaces)} or {table}.owner = {frappe.db.escape(user)}))"

	if is_staff(user):
		vis = f"({table}.visibility in ('Public', 'Internal') or {restricted})"
		return f"({space_cond} and {vis})"

	vis = f"({table}.visibility = 'Public' or {restricted})"
	return f"({space_cond} and {table}.status = 'Published' and {vis})"


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
	cond = _via_content("`tabTCD Content Relation`.from_content", user)
	if not cond:
		return ""
	return f"({cond} and {_via_content('`tabTCD Content Relation`.to_content', user)})"


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
	return is_admin(user) or (
		_content_doc_ok(doc.from_content, user) and _content_doc_ok(doc.to_content, user)
	)


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
