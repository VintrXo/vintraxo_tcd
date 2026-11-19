"""Learner "My Learning" and instructor dashboard data (portal pages, API and report)."""

import frappe
from frappe.utils import flt, getdate, nowdate

from vintraxo_tcd.core import courses as course_svc
from vintraxo_tcd.core.permissions import instructed, is_admin


def _offering_link(doctype: str, name: str) -> dict | None:
	from vintraxo_tcd.core.portal import course_url, path_url

	if not frappe.has_permission(doctype, "read", name):
		return None
	t = frappe.db.get_value(doctype, name, ["title", "slug", "space"], as_dict=True)
	url = (course_url if doctype == "TCD Course" else path_url)(t.space, t.slug)
	return {"title": t.title, "url": url}


def my_learning(user: str) -> dict:
	today = getdate(nowdate())
	enrollments = []
	for e in frappe.get_list(
		"TCD Enrollment",
		filters={"user": user, "status": ("!=", "Withdrawn")},
		fields=["name", "course", "learning_path", "status", "percent", "score", "due_date", "completed_on"],
		order_by="modified desc",
		limit_page_length=200,
	):
		link = _offering_link("TCD Course" if e.course else "TCD Learning Path", e.course or e.learning_path)
		if not link:
			continue
		e.update(link)
		e.kind = "course" if e.course else "path"
		e.overdue = bool(e.due_date and e.status != "Completed" and getdate(e.due_date) < today)
		enrollments.append(e)

	# assignments in my courses: submitted ones + open ones not submitted yet
	my_courses = [e.course for e in enrollments if e.course]
	contents = set()
	for c in my_courses:
		contents |= {i["content"] for i in course_svc.course_items(c)}
	submissions = {
		s.assignment: s
		for s in frappe.get_list(
			"TCD Assignment Submission",
			filters={"user": user},
			fields=["assignment", "status", "score", "passed", "feedback"],
			limit_page_length=500,
		)
	}
	assignments = []
	if contents or submissions:
		filters = {"is_active": 1}
		rows = frappe.get_list(
			"TCD Assignment",
			filters=filters,
			or_filters={"content": ("in", list(contents) or [""]), "name": ("in", list(submissions) or [""])},
			fields=["name", "title", "content", "due_date", "max_score"],
			limit_page_length=500,
		)
		for a in rows:
			sub = submissions.get(a.name)
			a.status = sub.status if sub else "Not Submitted"
			a.score = sub.score if sub else None
			a.passed = bool(sub and sub.passed)
			a.feedback = sub.feedback if sub else None
			a.overdue = bool(not sub and a.due_date and getdate(a.due_date) < today)
			assignments.append(a)

	quizzes = frappe.get_list(
		"TCD Quiz Submission",
		filters={"user": user},
		fields=["quiz", "percentage", "passed", "creation"],
		order_by="creation desc",
		limit_page_length=5,
	)
	from vintraxo_tcd.core import connect

	tutorials = []
	for row in frappe.get_list(
		"TCD Progress",
		filters={"user": user, "content_type": "Tutorial"},
		fields=["content", "status", "percent"],
		order_by="modified desc",
		limit_page_length=10,
	):
		item = connect._item("TCD Content", row.content, status=row.status, percent=row.percent)
		if item:
			tutorials.append(item)
	recent = []
	for row in frappe.get_list(
		"TCD Progress",
		filters={"user": user, "status": "Completed", "content_type": ("!=", "Tutorial")},
		fields=["content", "completed_on"],
		order_by="completed_on desc",
		limit_page_length=5,
	):
		item = connect._item("TCD Content", row.content, completed_on=row.completed_on)
		if item:
			recent.append(item)
	from urllib.parse import quote

	certificates = frappe.get_list(
		"TCD Certificate",
		filters={"user": user},
		fields=["name", "title", "status", "issued_on", "expires_on", "verification_code"],
		order_by="issued_on desc",
	)
	for c in certificates:
		c.pdf_url = (
			"/api/method/frappe.utils.print_format.download_pdf?doctype=TCD%20Certificate"
			f"&name={quote(c.name)}&format=TCD%20Certificate"
		)
		c.verify_url = f"/verify/{quote(c.verification_code)}"
	skills = frappe.get_list(
		"TCD User Skill",
		filters={"user": user},
		fields=["skill", "level", "source_type"],
		order_by="skill asc",
	)
	return {
		"certificates": certificates,
		"skills": skills,
		"recommendations": connect.recommendations(user),
		"tutorials": tutorials,
		"recent": recent,
		"enrollments": enrollments,
		"assignments": sorted(
			assignments, key=lambda a: (a.status != "Returned", a.status != "Not Submitted")
		),
		"quizzes": quizzes,
		"summary": {
			"active": sum(e.status == "Active" for e in enrollments),
			"pending_approval": sum(e.status == "Pending Approval" for e in enrollments),
			"completed": sum(e.status == "Completed" for e in enrollments),
			"overdue": sum(e.overdue for e in enrollments) + sum(a.overdue for a in assignments),
		},
	}


def instructor_courses(user: str) -> list[str]:
	if is_admin(user):
		return frappe.get_all("TCD Course", pluck="name", ignore_permissions=True)
	return sorted(instructed(user, "TCD Course"))


def instructor_dashboard(user: str) -> dict:
	from vintraxo_tcd.api import course_rating

	rows = []
	names = instructor_courses(user)
	for name in names:
		c = frappe.db.get_value("TCD Course", name, ["title", "status", "completion_rule"], as_dict=True)
		counts = {
			status: frappe.db.count("TCD Enrollment", {"course": name, "status": status})
			for status in ("Active", "Pending Approval", "Completed")
		}
		enrolled = sum(counts.values())
		scores = frappe.get_all(
			"TCD Enrollment",
			filters={"course": name, "score": (">", 0)},
			pluck="score",
			ignore_permissions=True,
		)
		rating = course_rating(name)
		rows.append(
			{
				"course": name,
				"title": c.title,
				"status": c.status,
				"completion_rule": c.completion_rule,
				"enrolled": enrolled,
				"active": counts["Active"],
				"pending_approval": counts["Pending Approval"],
				"completed": counts["Completed"],
				"completion_rate": flt(counts["Completed"] * 100 / enrolled, 1) if enrolled else 0,
				"to_grade": frappe.db.count(
					"TCD Assignment Submission", {"course": name, "status": "Submitted"}
				),
				"average_score": flt(sum(scores) / len(scores), 1) if scores else None,
				"rating": rating["average"],
				"ratings": rating["count"],
			}
		)
	pending = frappe.get_all(
		"TCD Enrollment",
		filters={"course": ("in", names or [""]), "status": "Pending Approval"},
		fields=["name", "user", "course", "modified"],
		order_by="modified asc",
		limit_page_length=50,
		ignore_permissions=True,
	)
	to_grade = frappe.get_all(
		"TCD Assignment Submission",
		filters={"course": ("in", names or [""]), "status": "Submitted"},
		fields=["name", "user", "assignment", "course", "submitted_on", "is_late"],
		order_by="submitted_on asc",
		limit_page_length=50,
		ignore_permissions=True,
	)
	contents = set()
	for name in names:
		contents |= {i["content"] for i in course_svc.course_items(name)}
	quiz_reviews = frappe.get_all(
		"TCD Quiz Submission",
		filters={"content": ("in", list(contents) or [""]), "status": "Pending Review"},
		fields=["name", "user", "quiz", "submitted_on"],
		order_by="submitted_on asc",
		limit_page_length=50,
		ignore_permissions=True,
	)
	titles = {r["course"]: r["title"] for r in rows}
	for row in pending + to_grade:
		row.course_title = titles.get(row.course)
	return {"courses": rows, "pending_approvals": pending, "to_grade": to_grade, "quiz_reviews": quiz_reviews}
