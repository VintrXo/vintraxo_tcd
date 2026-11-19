"""Governance documents: policies, SOPs and documents (PLAN Phase 6, ADR-0015)."""

import frappe
from frappe import _
from frappe.utils import add_days, add_months, getdate, now_datetime, nowdate

from vintraxo_tcd.core.permissions import is_admin, is_staff

TRANSITIONS = {
	"Draft": {"Review", "Archived"},
	"Review": {"Approval", "Draft"},
	"Approval": {"Active", "Draft"},
	"Active": {"Revision", "Archived"},
	"Revision": {"Review", "Archived"},
	"Archived": {"Draft"},
}
LOCKED_WHEN_ACTIVE = ("title", "summary", "body", "attachment", "doc_kind")
REVIEWER_ROLES = {"TCD Content Reviewer", "TCD Administrator", "System Manager"}
TCD_ROLES = {
	"TCD Administrator",
	"TCD Content Author",
	"TCD Content Reviewer",
	"TCD Instructor",
	"TCD Learner",
}
ACK_STATEMENT = "I have read and understood version {0} of this document and agree to follow it."


def has_departments() -> bool:
	return bool(frappe.db.exists("DocType", "Employee")) and bool(frappe.db.exists("DocType", "Department"))


# ---------------------------------------------------------------- lifecycle


def validate(doc):
	doc.code = (doc.code or "").strip().upper()
	if doc.expiry_date and doc.effective_date and getdate(doc.expiry_date) <= getdate(doc.effective_date):
		frappe.throw(_("Expiry date must be after the effective date."))
	if (doc.review_cycle_months or 0) < 0:
		frappe.throw(_("Review cycle cannot be negative."))
	for row in doc.links:
		if row.target_type == "Content":
			row.course = None
			if not row.content:
				frappe.throw(_("Row {0}: choose the content.").format(row.idx))
		else:
			row.content = None
			if not row.course:
				frappe.throw(_("Row {0}: choose the course.").format(row.idx))
	if has_departments():
		for row in doc.audience_departments:
			if not frappe.db.exists("Department", row.department):
				frappe.throw(_("Department {0} does not exist.").format(frappe.bold(row.department)))

	before = doc.get_doc_before_save()
	old = before.status if before else None
	if old is None:
		if doc.status not in ("Draft", "Review"):
			frappe.throw(_("New documents start as Draft."))
		return
	if old == doc.status:
		if old == "Active" and any(_changed(before, doc, f) for f in LOCKED_WHEN_ACTIVE):
			frappe.throw(_("Active documents cannot be edited. Start a revision first."))
		return
	if doc.status not in TRANSITIONS[old]:
		frappe.throw(_("Cannot move a document from {0} to {1}.").format(_(old), _(doc.status)))
	user = frappe.session.user
	roles = set(frappe.get_roles(user))
	if old == "Review" and doc.status == "Approval" and not roles & REVIEWER_ROLES:
		frappe.throw(_("Only a reviewer can send a document for approval."), frappe.PermissionError)
	if doc.status == "Active":
		if not (is_admin(user) or (doc.approver and doc.approver == user)):
			frappe.throw(
				_("Only the approver or an administrator can activate the document."), frappe.PermissionError
			)
		doc.version = int(doc.version or 0) + 1
		doc.effective_date = doc.effective_date if old == "Approval" and doc.effective_date else nowdate()
		if doc.review_cycle_months:
			doc.next_review_date = add_months(getdate(doc.effective_date), int(doc.review_cycle_months))
		doc.flags.snapshot = True


def _changed(before, doc, field) -> bool:
	return (before.get(field) or None) != (doc.get(field) or None)


def on_update(doc):
	if doc.flags.snapshot:
		doc.flags.snapshot = False
		version = frappe.get_doc(
			{
				"doctype": "TCD Governance Version",
				"governance_document": doc.name,
				"version": doc.version,
				"title": doc.title,
				"summary": doc.summary,
				"body": doc.body,
				"attachment": doc.attachment,
				"effective_date": doc.effective_date,
				"approved_by": frappe.session.user,
				"approved_on": now_datetime(),
			}
		)
		version.flags.from_governance = True
		version.insert(ignore_permissions=True)
		from vintraxo_tcd.core import integrations, notify

		notify.acknowledgment_due(doc)
		integrations.emit("Policy Activated", doc)


def current_version(name: str):
	"""Latest approved snapshot, or None when never activated."""
	version = frappe.db.get_value("TCD Governance Document", name, "version")
	if not version:
		return None
	return frappe.get_doc("TCD Governance Version", f"{name}-v{version}")


# ---------------------------------------------------------------- audience


def _user_department(user: str) -> str | None:
	if not has_departments():
		return None
	return frappe.db.get_value("Employee", {"user_id": user, "status": "Active"}, "department")


def in_audience(doc, user: str) -> bool:
	if user in ("Guest",):
		return False
	roles = set(frappe.get_roles(user))
	wanted = {r.role for r in doc.audience_roles}
	if wanted and not roles & wanted:
		return False
	if not wanted and not roles & TCD_ROLES:
		return False
	departments = {d.department for d in doc.audience_departments}
	if departments and has_departments():
		return _user_department(user) in departments
	return True


def can_read(doc, user: str) -> bool:
	"""Readers see Active (or under-revision) documents with a snapshot, when in the audience. Staff see all."""
	if is_staff(user) or is_admin(user):
		return True
	return doc.status in ("Active", "Revision") and bool(doc.version) and in_audience(doc, user)


def documents_for(user: str, kind: str | None = None) -> list:
	filters = {"status": ("in", ["Active", "Revision"]), "version": (">", 0)}
	if kind:
		filters["doc_kind"] = kind
	out = []
	for name in frappe.get_all(
		"TCD Governance Document",
		filters=filters,
		pluck="name",
		order_by="title asc",
		ignore_permissions=True,
	):
		doc = frappe.get_doc("TCD Governance Document", name)
		if can_read(doc, user):
			doc.acknowledged = has_acknowledged(user, name, doc.version)
			out.append(doc)
	return out


def audience_users(doc) -> list[str]:
	wanted = {r.role for r in doc.audience_roles} or TCD_ROLES
	users = set(
		frappe.get_all(
			"Has Role",
			filters={"role": ("in", list(wanted)), "parenttype": "User"},
			pluck="parent",
			distinct=True,
		)
	)
	users -= {"Administrator", "Guest"}
	enabled = set(
		frappe.get_all("User", filters={"name": ("in", list(users) or [""]), "enabled": 1}, pluck="name")
	)
	return sorted(u for u in enabled if in_audience(doc, u))


# ---------------------------------------------------------------- acknowledgment


def has_acknowledged(user: str, name: str, version: int) -> bool:
	return bool(
		frappe.db.exists(
			"TCD Acknowledgment", {"governance_document": name, "user": user, "version": version}
		)
	)


def acknowledge(name: str, user: str):
	doc = frappe.get_doc("TCD Governance Document", name)
	if not doc.require_acknowledgment:
		frappe.throw(_("This document does not need an acknowledgment."))
	if not doc.version or doc.status not in ("Active", "Revision"):
		frappe.throw(_("Only active documents can be acknowledged."))
	if not in_audience(doc, user):
		frappe.throw(_("This document is not addressed to you."), frappe.PermissionError)
	existing = frappe.db.get_value(
		"TCD Acknowledgment", {"governance_document": name, "user": user, "version": doc.version}
	)
	if existing:
		return frappe.get_doc("TCD Acknowledgment", existing)
	ack = frappe.get_doc(
		{
			"doctype": "TCD Acknowledgment",
			"governance_document": name,
			"version": doc.version,
			"user": user,
			"acknowledged_on": now_datetime(),
			"statement": ACK_STATEMENT.format(doc.version),
		}
	)
	ack.flags.from_governance = True
	ack.insert(ignore_permissions=True)
	from vintraxo_tcd.core import integrations

	integrations.emit("Policy Acknowledged", ack)
	return ack


def pending_for(user: str) -> list:
	return [d for d in documents_for(user) if d.require_acknowledgment and not d.acknowledged]


def acknowledgment_rows(name: str) -> list[dict]:
	doc = frappe.get_doc("TCD Governance Document", name)
	acks = {
		a.user: a
		for a in frappe.get_all(
			"TCD Acknowledgment",
			filters={"governance_document": name, "version": doc.version},
			fields=["user", "acknowledged_on"],
		)
	}
	rows = []
	for user in audience_users(doc):
		ack = acks.get(user)
		rows.append(
			{
				"user": user,
				"full_name": frappe.db.get_value("User", user, "full_name"),
				"version": doc.version,
				"acknowledged": 1 if ack else 0,
				"acknowledged_on": ack.acknowledged_on if ack else None,
			}
		)
	return rows


# ---------------------------------------------------------------- scheduler


def daily():
	"""Expire documents and open review reminders for their owners."""
	today = getdate(nowdate())
	for row in frappe.get_all(
		"TCD Governance Document",
		# "is set" matters: Frappe compares NULL dates as a very old date
		filters=[["status", "=", "Active"], ["expiry_date", "is", "set"], ["expiry_date", "<", today]],
		fields=["name"],
	):
		frappe.db.set_value("TCD Governance Document", row.name, "status", "Revision", update_modified=False)
		frappe.get_doc("TCD Governance Document", row.name).add_comment(
			"Info", _("Expired on its expiry date; moved to Revision.")
		)
	due = frappe.get_all(
		"TCD Governance Document",
		filters=[
			["status", "=", "Active"],
			["next_review_date", "is", "set"],
			["next_review_date", "<=", add_days(today, 7)],
		],
		fields=["name", "title", "document_owner", "next_review_date"],
	)
	for row in due:
		description = _("Review due on {0}: {1}").format(row.next_review_date, row.title)
		if frappe.db.exists(
			"ToDo",
			{
				"reference_type": "TCD Governance Document",
				"reference_name": row.name,
				"allocated_to": row.document_owner,
				"description": description,
			},
		):
			continue
		frappe.get_doc(
			{
				"doctype": "ToDo",
				"allocated_to": row.document_owner,
				"reference_type": "TCD Governance Document",
				"reference_name": row.name,
				"description": description,
				"date": row.next_review_date,
				"priority": "Medium",
			}
		).insert(ignore_permissions=True)


def related_for_content(content: str, user: str) -> list:
	parents = frappe.get_all(
		"TCD Governance Link",
		filters={"parenttype": "TCD Governance Document", "content": content},
		pluck="parent",
		ignore_permissions=True,
	)
	return [d for d in documents_for(user) if d.name in set(parents)]


def related_for_course(course: str, user: str) -> list:
	parents = frappe.get_all(
		"TCD Governance Link",
		filters={"parenttype": "TCD Governance Document", "course": course},
		pluck="parent",
		ignore_permissions=True,
	)
	return [d for d in documents_for(user) if d.name in set(parents)]
