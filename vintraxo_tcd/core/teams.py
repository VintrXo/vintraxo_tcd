"""Manager dashboard (Phase 13, ADR-0021): a manager follows the training status of their team.

Team = members of the TCD Teams they manage, plus (with ERPNext/HRMS) their active direct reports
(Employee.reports_to). Managers see status only (mandatory training, overdue, certificates, pending
acknowledgments, last activity), never answers, scores of single questions or submissions."""

import frappe
from frappe import _
from frappe.utils import add_days, getdate, nowdate

from vintraxo_tcd.core.permissions import is_admin
from vintraxo_tcd.core.training import employee_profile, hr_available

MAX_MEMBERS = 300


def direct_reports(user: str) -> set[str]:
	if not hr_available():
		return set()
	me = employee_profile(user)
	if not me:
		return set()
	return {
		u
		for u in frappe.get_all(
			"Employee",
			filters={"reports_to": me.name, "status": "Active", "user_id": ("is", "set")},
			pluck="user_id",
		)
		if u
	}


def teams_of(user: str) -> list[str]:
	filters = {} if is_admin(user) else {"manager": user}
	return frappe.get_all("TCD Team", filters=filters, pluck="name", order_by="team_name asc")


def members(user: str, team: str | None = None) -> list[str]:
	"""Users the given manager may follow. `team` narrows to one TCD Team (or "direct" for direct reports)."""
	allowed_teams = teams_of(user)
	if team == "direct":
		found = direct_reports(user)
	elif team:
		if team not in allowed_teams:
			raise frappe.PermissionError
		found = set(
			frappe.get_all(
				"TCD Team Member", filters={"parent": team, "parenttype": "TCD Team"}, pluck="user"
			)
		)
	else:
		mine = frappe.get_all("TCD Team", filters={"manager": user}, pluck="name")
		found = set(
			frappe.get_all(
				"TCD Team Member",
				filters={"parent": ("in", mine or [""]), "parenttype": "TCD Team"},
				pluck="user",
			)
		)
		found |= direct_reports(user)
	found.discard(user)
	return sorted(found)[:MAX_MEMBERS]


def is_manager(user: str) -> bool:
	if user == "Guest":
		return False
	return bool(frappe.db.exists("TCD Team", {"manager": user})) or bool(direct_reports(user))


def _member_row(user: str, today) -> dict:
	from vintraxo_tcd.core import governance

	enrollments = frappe.get_all(
		"TCD Enrollment",
		filters={"user": user, "status": ("!=", "Withdrawn")},
		fields=["status", "mandatory", "due_date", "course", "learning_path"],
	)
	mandatory = [e for e in enrollments if e.mandatory]
	overdue = [
		e for e in enrollments if e.status != "Completed" and e.due_date and getdate(e.due_date) < today
	]
	expiring = frappe.db.count(
		"TCD Certificate",
		[
			["user", "=", user],
			["status", "=", "Active"],
			["expires_on", "is", "set"],
			["expires_on", "<=", add_days(today, 30)],
		],
	)
	last = frappe.get_all(
		"TCD Progress",
		filters={"user": user},
		fields=["last_viewed_on"],
		order_by="last_viewed_on desc",
		limit=1,
	)
	profile = employee_profile(user) or {}
	done_mandatory = sum(1 for e in mandatory if e.status == "Completed")
	return {
		"user": user,
		"full_name": frappe.db.get_value("User", user, "full_name") or user,
		"department": profile.get("department"),
		"active": sum(1 for e in enrollments if e.status in ("Active", "Pending Approval")),
		"completed": sum(1 for e in enrollments if e.status == "Completed"),
		"mandatory": len(mandatory),
		"mandatory_done": done_mandatory,
		"compliance": round(done_mandatory * 100 / len(mandatory), 1) if mandatory else 100.0,
		"overdue": len(overdue),
		"expiring_certificates": expiring,
		"pending_acknowledgments": len(governance.pending_for(user)),
		"last_activity": last[0].last_viewed_on if last else None,
	}


def overview(user: str, team: str | None = None) -> dict:
	if not (is_manager(user) or is_admin(user)):
		raise frappe.PermissionError
	today = getdate(nowdate())
	rows = [_member_row(u, today) for u in members(user, team)]
	mandatory = sum(r["mandatory"] for r in rows)
	done = sum(r["mandatory_done"] for r in rows)
	return {
		"teams": teams_of(user),
		"has_direct_reports": bool(direct_reports(user)),
		"team": team,
		"members": sorted(rows, key=lambda r: (-r["overdue"], r["compliance"], r["full_name"])),
		"summary": {
			"members": len(rows),
			"compliance": round(done * 100 / mandatory, 1) if mandatory else 100.0,
			"overdue": sum(r["overdue"] for r in rows),
			"expiring_certificates": sum(r["expiring_certificates"] for r in rows),
			"pending_acknowledgments": sum(r["pending_acknowledgments"] for r in rows),
		},
	}


def validate_team(doc):
	seen = set()
	for row in doc.members:
		if row.user in seen:
			frappe.throw(_("{0} is listed twice.").format(frappe.bold(row.user)))
		if row.user == doc.manager:
			frappe.throw(_("The manager is not a member of their own team."))
		seen.add(row.user)
