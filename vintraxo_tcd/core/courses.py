"""Courses, learning paths and enrollments: structure rules, completion rules and roll-up.

Roll-up chain: lesson (TCD Progress) -> chapter (computed) -> course enrollment -> path enrollment.
"""

import frappe
from frappe import _
from frappe.utils import flt, now_datetime

from vintraxo_tcd.core.content import REVIEW_ROLES, require_approval

ITEM_CONTENT_TYPES = ("Lesson", "Article", "Reference")
OFFERINGS = {"Course": ("TCD Course", "course"), "Learning Path": ("TCD Learning Path", "learning_path")}


# ---------------------------------------------------------------- structure


def course_items(course: str) -> list[dict]:
	"""Ordered items of a course: [{chapter, chapter_title, content, is_optional}]."""
	chapters = frappe.get_all(
		"TCD Chapter",
		filters={"course": course},
		fields=["name", "title"],
		order_by="sort_order asc, creation asc",
		ignore_permissions=True,
	)
	items = []
	for ch in chapters:
		for row in frappe.get_all(
			"TCD Learning Item",
			filters={"parent": ch.name, "parenttype": "TCD Chapter"},
			fields=["content", "is_optional"],
			order_by="idx asc",
			ignore_permissions=True,
		):
			items.append(
				{
					"chapter": ch.name,
					"chapter_title": ch.title,
					"content": row.content,
					"is_optional": bool(row.is_optional),
				}
			)
	return items


def path_courses(path: str) -> list[dict]:
	return [
		{"course": r.course, "is_optional": bool(r.is_optional)}
		for r in frappe.get_all(
			"TCD Learning Item",
			filters={"parent": path, "parenttype": "TCD Learning Path"},
			fields=["course", "is_optional"],
			order_by="idx asc",
			ignore_permissions=True,
		)
	]


def courses_with_content(content: str) -> list[str]:
	chapters = frappe.get_all(
		"TCD Learning Item",
		filters={"parenttype": "TCD Chapter", "content": content},
		pluck="parent",
		ignore_permissions=True,
	)
	if not chapters:
		return []
	return list(
		set(
			frappe.get_all(
				"TCD Chapter", filters={"name": ("in", chapters)}, pluck="course", ignore_permissions=True
			)
		)
	)


def paths_with_course(course: str) -> list[str]:
	return list(
		set(
			frappe.get_all(
				"TCD Learning Item",
				filters={"parenttype": "TCD Learning Path", "course": course},
				pluck="parent",
				ignore_permissions=True,
			)
		)
	)


def validate_chapter(doc):
	if frappe.db.get_value("TCD Course", doc.course, "status") == "Published":
		frappe.throw(_("Move the course back to Draft to change its chapters."))
	seen_here = set()
	others = {i["content"] for i in course_items(doc.course) if i["chapter"] != doc.name and i["content"]}
	space = frappe.db.get_value("TCD Course", doc.course, "space")
	for row in doc.items:
		row.course = None
		if not row.content:
			frappe.throw(_("Row {0}: choose a content item.").format(row.idx))
		c = frappe.db.get_value("TCD Content", row.content, ["content_type", "space", "title"], as_dict=True)
		if not c:
			continue
		if c.content_type not in ITEM_CONTENT_TYPES:
			frappe.throw(
				_("Row {0}: {1} cannot be a course item (use a lesson, article or reference).").format(
					row.idx, frappe.bold(c.title)
				)
			)
		if c.space != space:
			frappe.throw(_("Row {0}: {1} must be in the course space.").format(row.idx, frappe.bold(c.title)))
		if row.content in seen_here or row.content in others:
			frappe.throw(_("Row {0}: {1} is already in this course.").format(row.idx, frappe.bold(c.title)))
		seen_here.add(row.content)
		row.item_title = c.title


def validate_path_items(doc):
	seen = set()
	for row in doc.items:
		row.content = None
		if not row.course:
			frappe.throw(_("Row {0}: choose a course.").format(row.idx))
		c = frappe.db.get_value("TCD Course", row.course, ["space", "title"], as_dict=True)
		if not c:
			continue
		if c.space != doc.space:
			frappe.throw(_("Row {0}: {1} must be in the same space.").format(row.idx, frappe.bold(c.title)))
		if row.course in seen:
			frappe.throw(_("Row {0}: {1} is listed twice.").format(row.idx, frappe.bold(c.title)))
		seen.add(row.course)
		row.item_title = c.title


def _is_reviewer() -> bool:
	return bool(set(frappe.get_roles()) & REVIEW_ROLES)


def validate_offering_status(doc):
	"""Course/path publishing: reviewer when approval is required; required items must be Published."""
	before = doc.get_doc_before_save()
	old = before.status if before else None
	if doc.status != "Published" or old == "Published":
		return
	if require_approval() and not _is_reviewer():
		frappe.throw(_("Only a reviewer can publish."), frappe.PermissionError)
	if doc.doctype == "TCD Course":
		required = [i["content"] for i in course_items(doc.name) if not i["is_optional"]]
		if not required:
			frappe.throw(_("Add at least one required item before publishing."))
		unpublished = frappe.get_all(
			"TCD Content",
			filters={"name": ("in", required), "status": ("!=", "Published")},
			pluck="title",
			ignore_permissions=True,
		)
	else:
		required = [r.course for r in doc.items if not r.is_optional]
		if not required:
			frappe.throw(_("Add at least one required course before publishing."))
		unpublished = frappe.get_all(
			"TCD Course",
			filters={"name": ("in", required), "status": ("!=", "Published")},
			pluck="title",
			ignore_permissions=True,
		)
	if unpublished:
		frappe.throw(_("Publish these items first: {0}").format(", ".join(unpublished)))


# ---------------------------------------------------------------- status / roll-up


def _completed_contents(user: str, contents: list[str]) -> set:
	if not contents:
		return set()
	return set(
		frappe.get_all(
			"TCD Progress",
			filters={"user": user, "content": ("in", contents), "status": "Completed"},
			pluck="content",
			ignore_permissions=True,
		)
	)


def _best_scores(user: str, contents: list[str]) -> dict:
	"""Best quiz percentage per content that has an active quiz."""
	if not contents:
		return {}
	quizzes = frappe.get_all(
		"TCD Quiz",
		filters={"content": ("in", contents), "is_active": 1},
		fields=["name", "content"],
		ignore_permissions=True,
	)
	best = {}
	for q in quizzes:
		scores = frappe.get_all(
			"TCD Quiz Submission",
			filters={"quiz": q.name, "user": user},
			pluck="percentage",
			ignore_permissions=True,
		)
		best[q.content] = max([flt(s) for s in scores] or [0.0])
	return best


def course_status(user: str, course: str) -> dict:
	"""Per-item and per-chapter state plus the course result under its completion rule."""
	rule, minimum = frappe.db.get_value("TCD Course", course, ["completion_rule", "minimum_score"])
	items = course_items(course)
	contents = [i["content"] for i in items]
	done = _completed_contents(user, contents)
	scores = _best_scores(user, contents)

	blocked = False
	chapters: dict[str, dict] = {}
	for item in items:
		item["completed"] = item["content"] in done
		item["locked"] = rule == "Required Sequence" and blocked and not item["completed"]
		if not item["is_optional"] and not item["completed"]:
			blocked = True
		ch = chapters.setdefault(
			item["chapter"], {"chapter": item["chapter"], "title": item["chapter_title"], "items": []}
		)
		ch["items"].append(item)

	for ch in chapters.values():
		req = [i for i in ch["items"] if not i["is_optional"]]
		ch["percent"] = flt(sum(i["completed"] for i in req) * 100 / len(req), 1) if req else 100.0

	required = [i for i in items if not i["is_optional"]]
	completed_required = sum(i["completed"] for i in required)
	percent = flt(completed_required * 100 / len(required), 1) if required else 0.0
	score = flt(sum(scores.values()) / len(scores), 2) if scores else None
	items_done = bool(required) and completed_required == len(required)
	meets_score = rule != "Minimum Score" or score is None or score >= flt(minimum)
	return {
		"course": course,
		"rule": rule,
		"items": items,
		"chapters": list(chapters.values()),
		"percent": percent,
		"score": score,
		"items_done": items_done,
		"complete": items_done and meets_score,
	}


def path_status(user: str, path: str) -> dict:
	rule = frappe.db.get_value("TCD Learning Path", path, "completion_rule")
	courses = path_courses(path)
	states = {}
	for c in courses:
		states[c["course"]] = frappe.db.get_value(
			"TCD Enrollment",
			{"user": user, "course": c["course"]},
			["status", "percent", "score"],
			as_dict=True,
		) or frappe._dict(status=None, percent=0, score=None)
	blocked = False
	for c in courses:
		st = states[c["course"]]
		c["completed"] = st.status == "Completed"
		c["percent"] = flt(st.percent)
		c["locked"] = rule == "Required Sequence" and blocked and not c["completed"]
		if not c["is_optional"] and not c["completed"]:
			blocked = True
	required = [c for c in courses if not c["is_optional"]]
	done = sum(c["completed"] for c in required)
	scored = [flt(states[c["course"]].score) for c in courses if states[c["course"]].score is not None]
	score = flt(sum(scored) / len(scored), 2) if scored else None
	minimum = frappe.db.get_value("TCD Learning Path", path, "minimum_score")
	items_done = bool(required) and done == len(required)
	return {
		"learning_path": path,
		"rule": rule,
		"courses": courses,
		"percent": flt(done * 100 / len(required), 1) if required else 0.0,
		"score": score,
		"items_done": items_done,
		"complete": items_done and (rule != "Minimum Score" or score is None or score >= flt(minimum)),
	}


def _apply(enrollment, state: dict):
	"""Write roll-up results to an enrollment (never downgrades Completed/Withdrawn)."""
	if enrollment.status in ("Completed", "Withdrawn"):
		return
	values = {"percent": state["percent"], "score": state["score"] or 0}
	if state["complete"]:
		if state["rule"] == "Manual Approval":
			values["status"] = "Pending Approval"
		else:
			values.update(status="Completed", completed_on=now_datetime())
	elif enrollment.status == "Pending Approval":
		values["status"] = "Active"
	enrollment.db_set(values)
	if values.get("status") == "Pending Approval":
		from vintraxo_tcd.core import notify

		notify.enrollment_pending(enrollment)
	if values.get("status") == "Completed":
		from vintraxo_tcd.core import credentials

		credentials.on_completed(enrollment)


def refresh_course(user: str, course: str):
	name = frappe.db.get_value("TCD Enrollment", {"user": user, "course": course})
	if not name:
		return None
	enrollment = frappe.get_doc("TCD Enrollment", name)
	_apply(enrollment, course_status(user, course))
	for path in paths_with_course(course):
		refresh_path(user, path)
	return enrollment


def refresh_path(user: str, path: str):
	name = frappe.db.get_value("TCD Enrollment", {"user": user, "learning_path": path})
	if not name:
		return None
	enrollment = frappe.get_doc("TCD Enrollment", name)
	_apply(enrollment, path_status(user, path))
	return enrollment


def on_content_changed(user: str, content: str):
	"""Called after lesson completion or quiz grading."""
	for course in courses_with_content(content):
		refresh_course(user, course)


def sequence_blockers(user: str, content: str) -> list[str]:
	"""Titles of required items that must be completed before `content`, across the learner's
	active enrollments in Required Sequence courses that contain it."""
	blockers = []
	for course in courses_with_content(content):
		if frappe.db.get_value("TCD Course", course, "completion_rule") != "Required Sequence":
			continue
		if not frappe.db.exists(
			"TCD Enrollment",
			{"user": user, "course": course, "status": ("in", ["Active", "Pending Approval"])},
		):
			continue
		items = course_items(course)
		done = _completed_contents(user, [i["content"] for i in items])
		for item in items:
			if item["content"] == content:
				break
			if not item["is_optional"] and item["content"] not in done:
				blockers.append(item["content"])
	if not blockers:
		return []
	return frappe.get_all(
		"TCD Content", filters={"name": ("in", blockers)}, pluck="title", ignore_permissions=True
	)


# ---------------------------------------------------------------- enrollment


def offering_of(doc) -> tuple[str, str]:
	doctype, field = OFFERINGS[doc.enrollment_for]
	return doctype, doc.get(field)


def validate_enrollment(doc):
	doctype, target = offering_of(doc)
	other_field = "learning_path" if doc.enrollment_for == "Course" else "course"
	doc.set(other_field, None)
	if not target:
		frappe.throw(_("Choose what to enroll in."))
	status, space = frappe.db.get_value(doctype, target, ["status", "space"]) or (None, None)
	if doc.is_new() and status != "Published":
		frappe.throw(_("You can only enroll in published courses and learning paths."))
	doc.space = space
	field = OFFERINGS[doc.enrollment_for][1]
	if frappe.db.exists("TCD Enrollment", {"user": doc.user, field: target, "name": ("!=", doc.name)}):
		frappe.throw(_("{0} is already enrolled.").format(frappe.bold(doc.user)))
	if doc.is_new():
		doc.enrolled_on = doc.enrolled_on or now_datetime()
	before = doc.get_doc_before_save()
	if before and before.status != doc.status and doc.status == "Completed":
		if before.status != "Pending Approval" and not doc.flags.from_rollup:
			frappe.throw(_("Enrollments complete automatically or through approval."))


def enroll(user: str, enrollment_for: str, target: str, batch: str | None = None, due_date=None):
	"""Create (or return) an enrollment; a path enrollment also enrolls in its courses."""
	field = OFFERINGS[enrollment_for][1]
	existing = frappe.db.get_value("TCD Enrollment", {"user": user, field: target})
	if existing:
		doc = frappe.get_doc("TCD Enrollment", existing)
		if doc.status == "Withdrawn":
			doc.status = "Active"
			doc.save(ignore_permissions=True)
	else:
		doc = frappe.get_doc(
			{
				"doctype": "TCD Enrollment",
				"user": user,
				"enrollment_for": enrollment_for,
				field: target,
				"batch": batch,
				"due_date": due_date,
			}
		).insert(ignore_permissions=True)
	if enrollment_for == "Learning Path":
		for c in path_courses(target):
			if frappe.db.get_value("TCD Course", c["course"], "status") == "Published":
				enroll(user, "Course", c["course"], batch, due_date)
		refresh_path(user, target)
	else:
		refresh_course(user, target)
	return frappe.get_doc("TCD Enrollment", doc.name)


def approve(enrollment_name: str):
	doc = frappe.get_doc("TCD Enrollment", enrollment_name)
	if doc.status != "Pending Approval":
		frappe.throw(_("Only enrollments pending approval can be approved."))
	doc.flags.from_rollup = True
	doc.update(
		{
			"status": "Completed",
			"completed_on": now_datetime(),
			"approved_by": frappe.session.user,
			"approved_on": now_datetime(),
		}
	)
	doc.save(ignore_permissions=True)
	from vintraxo_tcd.core import credentials

	credentials.on_completed(doc)
	if doc.course:
		for path in paths_with_course(doc.course):
			refresh_path(doc.user, path)
	return doc
