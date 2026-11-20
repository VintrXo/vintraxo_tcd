"""Skills and certificates (PLAN Phase 5, ADR-0014)."""

import secrets

import frappe
from frappe import _
from frappe.utils import add_months, getdate, now_datetime, nowdate

LEVEL_NAMES = {1: "Beginner", 2: "Basic", 3: "Intermediate", 4: "Advanced", 5: "Expert"}
TARGETS = {"Course": ("TCD Course", "course"), "Learning Path": ("TCD Learning Path", "learning_path")}


# ---------------------------------------------------------------- skills


def award_skill(
	user: str, skill: str, level: int, source_type: str = "Manual", source_name: str | None = None
):
	"""Create or raise a user skill (never lowers an existing level)."""
	level = int(level)
	name = frappe.db.get_value("TCD User Skill", {"user": user, "skill": skill})
	if name:
		doc = frappe.get_doc("TCD User Skill", name)
		if int(doc.level or 0) >= level:
			return doc
	else:
		doc = frappe.new_doc("TCD User Skill")
		doc.update({"user": user, "skill": skill})
	doc.update(
		{
			"level": str(level),
			"source_type": source_type,
			"source_name": source_name,
			"awarded_on": now_datetime(),
			"verified_by": frappe.session.user if source_type == "Manual" else None,
		}
	)
	doc.flags.from_credentials = True
	doc.save(ignore_permissions=True)
	return doc


def validate_user_skill(doc):
	if not doc.flags.from_credentials and doc.source_type != "Manual":
		frappe.throw(_("Course and path skills are awarded automatically on completion."))
	if doc.source_type == "Manual":
		doc.verified_by = frappe.session.user
		doc.awarded_on = doc.awarded_on or now_datetime()
	if frappe.db.exists("TCD User Skill", {"user": doc.user, "skill": doc.skill, "name": ("!=", doc.name)}):
		frappe.throw(_("{0} already has this skill; edit the existing record.").format(frappe.bold(doc.user)))


def user_level(user: str, skill: str) -> int:
	return int(frappe.db.get_value("TCD User Skill", {"user": user, "skill": skill}, "level") or 0)


# ---------------------------------------------------------------- completion hook


def on_completed(enrollment):
	"""Called when an enrollment becomes Completed (automatic or approved)."""
	from vintraxo_tcd.core import integrations

	integrations.emit("Enrollment Completed", enrollment)
	from vintraxo_tcd.core import badges, hr_sync

	hr_sync.on_completed(enrollment)
	if enrollment.course:
		badges.check(enrollment.user, "Course Completed", course=enrollment.course)
	else:
		badges.check(enrollment.user, "Learning Path Completed", learning_path=enrollment.learning_path)
	kind = "Course" if enrollment.course else "Learning Path"
	doctype, field = TARGETS[kind]
	target = enrollment.get(field)
	offering = frappe.get_doc(doctype, target)
	for row in offering.get("skills") or []:
		award_skill(enrollment.user, row.skill, int(row.level), kind, target)
	if offering.get("issue_certificate"):
		if kind == "Course" and offering.get("requires_evaluation"):
			# Phase 19: the certificate waits for a passed evaluation
			from vintraxo_tcd.core import notify

			notify._send(
				[enrollment.user],
				_("You completed {0}. Book your certification evaluation on the course page.").format(
					offering.title
				),
				"TCD Course",
				target,
			)
		else:
			from vintraxo_tcd.core import content_languages

			if kind == "Course" and content_languages.has_sibling_certificate(enrollment.user, target):
				return  # Phase 31: one certificate per course, whatever language it was finished in
			issue_certificate(enrollment.user, kind, target)


# ---------------------------------------------------------------- certificates


def _active(user: str, field: str, target: str) -> str | None:
	return frappe.db.get_value("TCD Certificate", {"user": user, field: target, "status": "Active"})


def issue_certificate(user: str, kind: str, target: str, replaces: str | None = None):
	doctype, field = TARGETS[kind]
	if not replaces and _active(user, field, target):
		return None
	offering = frappe.db.get_value(doctype, target, ["title", "certificate_validity_months"], as_dict=True)
	issued = getdate(nowdate())
	months = int(offering.certificate_validity_months or 0)
	cert = frappe.get_doc(
		{
			"doctype": "TCD Certificate",
			"user": user,
			"full_name": frappe.db.get_value("User", user, "full_name") or user,
			"certificate_for": kind,
			field: target,
			"title": offering.title,
			"status": "Active",
			"issued_on": issued,
			"expires_on": add_months(issued, months) if months > 0 else None,
			"verification_code": _new_code(),
		}
	)
	cert.flags.from_credentials = True
	cert.insert(ignore_permissions=True)
	if replaces:
		frappe.db.set_value("TCD Certificate", replaces, {"status": "Renewed", "renewed_by": cert.name})
	from vintraxo_tcd.core import integrations

	integrations.emit("Certificate Issued", cert)
	from vintraxo_tcd.core import badges

	badges.check(user, "Certificate Earned")
	return cert


def _new_code() -> str:
	while True:
		code = secrets.token_urlsafe(12)[:16].replace("-", "A").replace("_", "B")
		if not frappe.db.exists("TCD Certificate", {"verification_code": code}):
			return code


def renew_certificate(name: str):
	"""Issue a new certificate (new expiry) after the learner refreshed; the old one becomes Renewed."""
	old = frappe.get_doc("TCD Certificate", name)
	if old.status not in ("Active", "Expired"):
		frappe.throw(_("Only active or expired certificates can be renewed."))
	kind = old.certificate_for
	return issue_certificate(old.user, kind, old.get(TARGETS[kind][1]), replaces=old.name)


def revoke_certificate(name: str, reason: str):
	if not (reason or "").strip():
		frappe.throw(_("Give a reason for revoking the certificate."))
	frappe.db.set_value("TCD Certificate", name, {"status": "Revoked", "revoked_reason": reason.strip()})
	from vintraxo_tcd.core import integrations

	integrations.emit("Certificate Revoked", frappe.get_doc("TCD Certificate", name))


def expire_certificates():
	"""Daily scheduler job."""
	for name in frappe.get_all(
		"TCD Certificate",
		# "is set" matters: Frappe compares NULL dates as a very old date
		filters=[["status", "=", "Active"], ["expires_on", "is", "set"], ["expires_on", "<", nowdate()]],
		pluck="name",
	):
		frappe.db.set_value("TCD Certificate", name, "status", "Expired", update_modified=False)


def verify(code: str) -> dict | None:
	"""Public verification payload: no e-mail, no internal ids."""
	if not code or len(code) > 64:
		return None
	row = frappe.db.get_value(
		"TCD Certificate",
		{"verification_code": code},
		["name", "full_name", "title", "certificate_for", "issued_on", "expires_on", "status"],
		as_dict=True,
	)
	if not row:
		return None
	if row.status == "Active" and row.expires_on and getdate(row.expires_on) < getdate(nowdate()):
		row.status = "Expired"
	return row


def validate_certificate(doc):
	if not doc.flags.from_credentials:
		frappe.throw(_("Certificates are issued automatically on completion."))


# ---------------------------------------------------------------- competency gap


def gap_rows(profile_name: str, user: str | None = None) -> list[dict]:
	profile = frappe.get_doc("TCD Competency Profile", profile_name)
	if user:
		users = [user]
	elif profile.role:
		users = frappe.get_all(
			"Has Role", filters={"role": profile.role, "parenttype": "User"}, pluck="parent", distinct=True
		)
		users = [u for u in users if u not in ("Administrator", "Guest")]
	else:
		users = []
	rows = []
	for u in sorted(users):
		full_name = frappe.db.get_value("User", u, "full_name")
		for req in profile.requirements:
			required = int(req.required_level)
			current = user_level(u, req.skill)
			gap = max(required - current, 0)
			rows.append(
				{
					"user": u,
					"full_name": full_name,
					"skill": req.skill,
					"required_level": required,
					"current_level": current,
					"gap": gap,
					"suggested": ", ".join(courses_for_skill(req.skill, required)) if gap else "",
				}
			)
	return rows


def courses_for_skill(skill: str, level: int) -> list[str]:
	parents = frappe.get_all(
		"TCD Skill Award",
		filters={"skill": skill, "parenttype": "TCD Course"},
		fields=["parent", "level"],
		ignore_permissions=True,
	)
	names = [p.parent for p in parents if int(p.level) >= level]
	if not names:
		return []
	return frappe.get_all(
		"TCD Course",
		filters={"name": ("in", names), "status": "Published"},
		pluck="title",
		ignore_permissions=True,
	)
