"""Learner profile and internal job board (Phase 16, ADR-0024).

Profiles are private unless the learner makes them visible to colleagues. Job openings list the skills
they need; learners see how well their earned skills match and apply with a note and an optional CV
(private file). The hiring manager (and admins) see the applications."""

import frappe
from frappe import _
from frappe.utils import getdate, nowdate

from vintraxo_tcd.core.permissions import is_admin

MAX_TEXT = 2000


# ---------------------------------------------------------------- profile


def _profile_doc(user: str):
	if frappe.db.exists("TCD Learner Profile", user):
		return frappe.get_doc("TCD Learner Profile", user)
	doc = frappe.get_doc({"doctype": "TCD Learner Profile", "user": user})
	doc.flags.from_service = True
	return doc


def view(user: str, viewer: str) -> dict:
	"""A profile as the viewer may see it (raises DoesNotExist when it is private)."""
	if viewer == "Guest" or not frappe.db.exists("User", user):
		raise frappe.DoesNotExistError
	doc = _profile_doc(user)
	own = user == viewer
	if not own and not doc.public_profile and not is_admin(viewer):
		raise frappe.DoesNotExistError
	from vintraxo_tcd.core import badges

	skills = frappe.get_all(
		"TCD User Skill", filters={"user": user}, fields=["skill", "level"], order_by="level desc"
	)
	certificates = frappe.get_all(
		"TCD Certificate",
		filters={"user": user, "status": "Active"},
		fields=["title", "issued_on", "verification_code"],
	)
	return {
		"user": user,
		"own": own,
		"full_name": frappe.db.get_value("User", user, "full_name") or user,
		"headline": doc.headline,
		"bio": doc.bio,
		"public_profile": bool(doc.public_profile),
		"education": [
			{"institution": e.institution, "degree": e.degree, "year": e.year} for e in doc.education
		],
		"experience": [
			{"company": e.company, "job_title": e.job_title, "from_year": e.from_year, "to_year": e.to_year}
			for e in doc.experience
		],
		"skills": skills,
		"certificates": certificates,
		"badges": badges.mine(user),
	}


def save(user: str, data: dict) -> dict:
	if user == "Guest":
		raise frappe.PermissionError
	doc = _profile_doc(user)
	doc.headline = (data.get("headline") or "").strip()[:140]
	doc.bio = (data.get("bio") or "").strip()[:MAX_TEXT]
	doc.public_profile = 1 if data.get("public_profile") else 0
	doc.set("education", [])
	for e in (data.get("education") or [])[:20]:
		if (e.get("institution") or "").strip():
			doc.append(
				"education",
				{
					"institution": e["institution"].strip()[:140],
					"degree": (e.get("degree") or "")[:140],
					"year": int(e.get("year") or 0) or None,
				},
			)
	doc.set("experience", [])
	for e in (data.get("experience") or [])[:30]:
		if (e.get("company") or "").strip():
			doc.append(
				"experience",
				{
					"company": e["company"].strip()[:140],
					"job_title": (e.get("job_title") or "")[:140],
					"from_year": int(e.get("from_year") or 0) or None,
					"to_year": int(e.get("to_year") or 0) or None,
				},
			)
	doc.flags.from_service = True
	doc.save(ignore_permissions=True)
	return {"saved": True}


def validate_profile(doc):
	if doc.is_new() and not doc.flags.from_service and not is_admin(frappe.session.user):
		frappe.throw(_("Profiles are edited from the learning portal."))


# ---------------------------------------------------------------- jobs


def match_percent(user: str, job) -> float:
	required = job.get("required_skills") or []
	if not required:
		return 100.0
	have = {
		s.skill: int(s.level or 0)
		for s in frappe.get_all("TCD User Skill", filters={"user": user}, fields=["skill", "level"])
	}
	met = sum(1 for r in required if have.get(r.skill, 0) >= int(r.level or 1))
	return round(met * 100 / len(required), 1)


def open_jobs(user: str) -> list[dict]:
	today = getdate(nowdate())
	out = []
	for name in frappe.get_all(
		"TCD Job Opening", filters={"status": "Open"}, pluck="name", order_by="creation desc"
	):
		job = frappe.get_doc("TCD Job Opening", name)
		if job.closes_on and getdate(job.closes_on) < today:
			continue
		out.append(
			{
				"name": job.name,
				"title": job.title,
				"department": job.department,
				"location": job.location,
				"employment_type": job.employment_type,
				"closes_on": job.closes_on,
				"description": job.description,
				"skills": [{"skill": r.skill, "level": r.level} for r in job.required_skills],
				"match": match_percent(user, job),
				"applied": bool(frappe.db.exists("TCD Job Application", {"job": job.name, "user": user})),
			}
		)
	out.sort(key=lambda j: -j["match"])
	return out


def apply(job_name: str, user: str, cover_note: str = "", resume: str | None = None) -> str:
	if user == "Guest":
		raise frappe.PermissionError
	job = frappe.get_doc("TCD Job Opening", job_name)
	if job.status != "Open" or (job.closes_on and getdate(job.closes_on) < getdate(nowdate())):
		frappe.throw(_("This job opening is closed."))
	if frappe.db.exists("TCD Job Application", {"job": job.name, "user": user}):
		frappe.throw(_("You already applied for this job."))
	if resume:
		from vintraxo_tcd.core import media

		media.validate_file_url(resume, owner=user)  # the applicant's own uploaded file
	app = frappe.get_doc(
		{
			"doctype": "TCD Job Application",
			"job": job.name,
			"user": user,
			"status": "Submitted",
			"cover_note": (cover_note or "").strip()[:MAX_TEXT],
			"resume": resume,
			"match_percent": match_percent(user, job),
		}
	)
	app.flags.from_service = True
	app.insert(ignore_permissions=True)
	from vintraxo_tcd.core import notify

	who = frappe.db.get_value("User", user, "full_name") or user
	notify._send(
		[job.hiring_manager],
		_("New application for {0} from {1}").format(job.title, who),
		"TCD Job Application",
		app.name,
	)
	return app.name


def application_has_permission(doc, ptype=None, user=None, debug=False):
	user = user or frappe.session.user
	if is_admin(user):
		return True
	manager = frappe.db.get_value("TCD Job Opening", doc.job, "hiring_manager")
	return manager == user and ptype in (None, "read", "write", "report", "print")


def application_query(user=None, doctype=None):
	user = user or frappe.session.user
	if is_admin(user):
		return ""
	jobs = frappe.get_all("TCD Job Opening", filters={"hiring_manager": user}, pluck="name")
	if not jobs:
		return "1=0"
	return "`tabTCD Job Application`.job in (" + ", ".join(frappe.db.escape(j) for j in jobs) + ")"


def validate_application(doc):
	if doc.is_new() and not doc.flags.from_service:
		frappe.throw(_("Applications are sent from the job board."))
	before = doc.get_doc_before_save()
	if before and before.status != doc.status:
		from vintraxo_tcd.core import notify

		title = frappe.db.get_value("TCD Job Opening", doc.job, "title")
		notify._send(
			[doc.user],
			_("Your application for {0}: {1}").format(title, _(doc.status)),
			"TCD Job Application",
			doc.name,
		)
