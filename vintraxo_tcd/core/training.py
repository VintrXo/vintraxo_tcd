"""Training rules and the HR link (PLAN Phase 8, ADR-0017).

Rules enroll matching users automatically (mandatory training) or recommend a tutorial / process
guide by role. HR filters (department, designation, company) use the ERPNext/HRMS Employee and are
guarded: on a site without ERPNext a rule with HR filters matches nobody."""

from collections import defaultdict

import frappe
from frappe import _
from frappe.utils import add_days, now_datetime, nowdate

from vintraxo_tcd.core.governance import TCD_ROLES

HR_FIELDS = {"Department": "department", "Designation": "designation", "Company": "company"}
TARGET_FIELDS = {"Course": "course", "Learning Path": "learning_path", "Content": "content"}


def hr_available() -> bool:
	return bool(frappe.db.exists("DocType", "Employee"))


def employee_profile(user: str):
	"""The active Employee linked to the user (name, department, designation, company), or None."""
	if not user or user in ("Guest", "Administrator") or not hr_available():
		return None
	return frappe.db.get_value(
		"Employee",
		{"user_id": user, "status": "Active"},
		["name", "department", "designation", "company"],
		as_dict=True,
	)


# ---------------------------------------------------------------- rule document


def validate_rule(doc):
	for kind, field in TARGET_FIELDS.items():
		if kind != doc.target_type:
			doc.set(field, None)
	target = doc.get(TARGET_FIELDS[doc.target_type])
	if not target:
		frappe.throw(_("Choose the {0}.").format(_(doc.target_type)))
	if doc.target_type == "Content":
		doc.mandatory = 0
		doc.due_in_days = 0
	if (doc.due_in_days or 0) < 0:
		frappe.throw(_("Due days cannot be negative."))
	roles = [r.role for r in doc.roles]
	if len(roles) != len(set(roles)):
		frappe.throw(_("A role is listed twice."))
	if doc.hr_filters:
		if not hr_available():
			frappe.msgprint(
				_("HR filters need ERPNext/HRMS. Until it is installed this rule matches nobody."),
				indicator="orange",
				alert=True,
			)
		else:
			for row in doc.hr_filters:
				row.value = (row.value or "").strip()
				if not frappe.db.exists(row.filter_type, row.value):
					frappe.throw(
						_("Row {0}: {1} {2} does not exist.").format(
							row.idx, _(row.filter_type), frappe.bold(row.value)
						)
					)


def on_rule_update(doc):
	if doc.enabled and doc.target_type != "Content":
		frappe.enqueue(
			"vintraxo_tcd.core.training.apply_rule",
			queue="long",
			rule=doc.name,
			enqueue_after_commit=True,
		)


# ---------------------------------------------------------------- matching


def rule_matches(rule, user: str) -> bool:
	if user in ("Guest", "Administrator") or not frappe.db.get_value("User", user, "enabled"):
		return False
	roles = set(frappe.get_roles(user))
	wanted = {r.role for r in rule.roles}
	if wanted and not roles & wanted:
		return False
	if not wanted and not roles & TCD_ROLES:
		return False
	if rule.hr_filters:
		profile = employee_profile(user)
		if not profile:
			return False
		groups = defaultdict(set)
		for row in rule.hr_filters:
			groups[row.filter_type].add(row.value)
		return all(profile.get(HR_FIELDS[kind]) in values for kind, values in groups.items())
	return True


def candidate_users(rule) -> list[str]:
	wanted = {r.role for r in rule.roles} or TCD_ROLES
	users = set(
		frappe.get_all(
			"Has Role",
			filters={"role": ("in", list(wanted)), "parenttype": "User"},
			pluck="parent",
			distinct=True,
		)
	) - {"Administrator", "Guest"}
	return sorted(
		frappe.get_all("User", filters={"name": ("in", list(users) or [""]), "enabled": 1}, pluck="name")
	)


# ---------------------------------------------------------------- enrollment


def apply_rule(rule, users: list[str] | None = None) -> int:
	"""Enroll matching users who have no enrollment in the target yet. Returns the number enrolled.
	Existing enrollments (also withdrawn ones) are left alone: an admin decision wins over the rule."""
	from vintraxo_tcd.core import courses

	if isinstance(rule, str):
		rule = frappe.get_doc("TCD Training Rule", rule)
	if not rule.enabled or rule.target_type == "Content":
		return 0
	field = TARGET_FIELDS[rule.target_type]
	target = rule.get(field)
	status = frappe.db.get_value("TCD Course" if field == "course" else "TCD Learning Path", target, "status")
	if status != "Published":
		return 0
	due = add_days(nowdate(), int(rule.due_in_days)) if rule.due_in_days else None
	count = 0
	for user in users if users is not None else candidate_users(rule):
		if frappe.db.exists("TCD Enrollment", {"user": user, field: target}):
			continue
		if not rule_matches(rule, user):
			continue
		savepoint = "tcd_rule_" + frappe.generate_hash(length=8)
		frappe.db.savepoint(savepoint)
		try:
			courses.enroll(
				user,
				rule.target_type,
				target,
				due_date=due,
				extra={"mandatory": rule.mandatory, "training_rule": rule.name},
			)
			count += 1
		except Exception:
			frappe.db.rollback(save_point=savepoint)
			frappe.log_error(title=f"TCD training rule {rule.name}: cannot enroll {user}")
	frappe.db.set_value(
		"TCD Training Rule", rule.name, "last_applied_on", now_datetime(), update_modified=False
	)
	return count


def apply_for_user(user: str) -> int:
	count = 0
	for name in frappe.get_all(
		"TCD Training Rule", filters={"enabled": 1, "target_type": ("!=", "Content")}, pluck="name"
	):
		count += apply_rule(name, [user])
	return count


def on_user_update(doc, method=None):
	if doc.name in ("Administrator", "Guest") or not doc.enabled:
		return
	if frappe.db.exists("TCD Training Rule", {"enabled": 1, "target_type": ("!=", "Content")}):
		apply_for_user(doc.name)


def on_employee_update(doc, method=None):
	if doc.get("user_id") and doc.get("status") == "Active":
		on_user_update(frappe.get_doc("User", doc.user_id))


def daily():
	"""Catch new hires, role changes and HR moves that happened without a save hook."""
	for name in frappe.get_all(
		"TCD Training Rule", filters={"enabled": 1, "target_type": ("!=", "Content")}, pluck="name"
	):
		apply_rule(name)


# ---------------------------------------------------------------- role guides


def role_guides(user: str) -> list[dict]:
	"""Tutorials and process guides recommended by Content rules that match the user."""
	from vintraxo_tcd.core import portal
	from vintraxo_tcd.core.permissions import can_access_content

	out, seen = [], set()
	for name in frappe.get_all(
		"TCD Training Rule",
		filters={"enabled": 1, "target_type": "Content"},
		pluck="name",
		order_by="title asc",
	):
		rule = frappe.get_doc("TCD Training Rule", name)
		if rule.content in seen or not frappe.db.exists("TCD Content", rule.content):
			continue  # a rule pointing to a deleted page must not break My Learning
		if not rule_matches(rule, user):
			continue
		content = frappe.get_doc("TCD Content", rule.content)
		if content.status != "Published" or not can_access_content(content, user):
			continue
		seen.add(content.name)
		done = frappe.db.get_value(
			"TCD Progress", {"user": user, "content": content.name, "status": "Completed"}
		)
		out.append(
			{
				"title": content.title,
				"content_type": content.content_type,
				"url": portal.content_url(content.space, content.slug),
				"completed": bool(done),
			}
		)
	return out


# ---------------------------------------------------------------- compliance


def compliance_rows(filters) -> list[dict]:
	"""Mandatory training per user. Goes through get_list so permission layers apply."""
	conditions = {"mandatory": 1, "status": ("!=", "Withdrawn")}
	if filters.get("training_rule"):
		conditions["training_rule"] = filters["training_rule"]
	today = nowdate()
	per_user = {}
	for e in frappe.get_list(
		"TCD Enrollment",
		filters=conditions,
		fields=["user", "full_name", "status", "due_date"],
		limit_page_length=0,
	):
		row = per_user.setdefault(
			e.user, {"user": e.user, "full_name": e.full_name, "assigned": 0, "completed": 0, "overdue": 0}
		)
		row["assigned"] += 1
		if e.status == "Completed":
			row["completed"] += 1
		elif e.due_date and str(e.due_date) < today:
			row["overdue"] += 1
	rows = []
	for row in per_user.values():
		profile = employee_profile(row["user"]) or {}
		row.update(
			employee=profile.get("name"),
			department=profile.get("department"),
			designation=profile.get("designation"),
			compliance=round(row["completed"] * 100 / row["assigned"], 1),
		)
		if filters.get("department") and row["department"] != filters["department"]:
			continue
		rows.append(row)
	rows.sort(key=lambda r: (r["compliance"], r["user"]))
	return rows
