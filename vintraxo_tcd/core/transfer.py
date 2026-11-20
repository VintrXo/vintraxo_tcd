"""Export / import a whole space (Phase 13, ADR-0021).

Export: one JSON bundle with the space and everything that belongs to it (categories, pages, tutorials,
courses + chapters, learning paths, quizzes + bank questions, assignments, relations, skills). Never
exported: enrollments, progress, submissions, certificates, discussions, instructors, uploaded files.
Import: creates a NEW space, recreates every record with new names and rewrites all links. Admins only
(the bundle contains quiz answers)."""

import json

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime

from vintraxo_tcd.core.permissions import is_admin

FORMAT = "vintraxo-tcd-space"
VERSION = 1
MAX_BYTES = 20 * 1024 * 1024
META = {
	"name",
	"owner",
	"creation",
	"modified",
	"modified_by",
	"docstatus",
	"idx",
	"parent",
	"parentfield",
	"parenttype",
	"doctype",
	"_user_tags",
	"_comments",
	"_assign",
	"_liked_by",
	"_seen",
	"amended_from",
}
DERIVED = {
	"TCD Content": {
		"search_text",
		"internal_links",
		"current_version",
		"approved_by",
		"approved_on",
		"published_on",
		"content_owner",
		"last_reviewed_on",
		"next_review_date",
		"ai_generated",
	},
	"TCD Course": {"instructors", "search_text"},
	"TCD Learning Path": {"instructors", "search_text"},
	"TCD Question": {"ai_source", "ai_status"},
}


def _require_admin():
	if not is_admin(frappe.session.user):
		frappe.throw(_("Only administrators can export or import spaces."), frappe.PermissionError)


def _clean(doc) -> dict:
	data = doc.as_dict(no_default_fields=False, convert_dates_to_str=True)
	drop = META | DERIVED.get(doc.doctype, set())
	out = {"_id": doc.name}
	for key, value in data.items():
		if key in drop or key.startswith("__"):
			continue
		if isinstance(value, list):
			value = [
				{k: v for k, v in row.items() if k not in META and not k.startswith("__")} for row in value
			]
		out[key] = value
	return out


def _all(doctype, filters) -> list:
	return [
		frappe.get_doc(doctype, n)
		for n in frappe.get_all(doctype, filters=filters, pluck="name", order_by="creation asc")
	]


# ---------------------------------------------------------------- export


def export_space(space: str) -> dict:
	_require_admin()
	sp = frappe.get_doc("TCD Space", space)
	contents = _all("TCD Content", {"space": space})
	content_names = [c.name for c in contents] or [""]
	courses = _all("TCD Course", {"space": space})
	course_names = [c.name for c in courses] or [""]
	paths = _all("TCD Learning Path", {"space": space})
	quizzes = _all("TCD Quiz", {"content": ("in", content_names)})
	bank_q = {r.question for q in quizzes for r in q.get("bank_items") or [] if r.question}
	bank_cat = {r.category for q in quizzes for r in q.get("bank_items") or [] if r.category}
	question_names = bank_q | set(
		frappe.get_all("TCD Question", filters={"category": ("in", list(bank_cat) or [""])}, pluck="name")
	)
	questions = [frappe.get_doc("TCD Question", n) for n in sorted(question_names)]
	q_categories = {q.category for q in questions if q.category} | bank_cat
	skills = {r.skill for o in courses + paths for r in o.get("skills") or []}
	return {
		"format": FORMAT,
		"version": VERSION,
		"exported_on": str(now_datetime()),
		"source_site": frappe.local.site,
		"space": _clean(sp),
		"categories": [_clean(d) for d in _all("TCD Category", {"space": space})],
		"skills": [_clean(frappe.get_doc("TCD Skill", s)) for s in sorted(skills)],
		"question_categories": [
			_clean(frappe.get_doc("TCD Question Category", c)) for c in sorted(q_categories)
		],
		"contents": [_clean(d) for d in contents],
		"questions": [_clean(d) for d in questions],
		"courses": [_clean(d) for d in courses],
		"chapters": [_clean(d) for d in _all("TCD Chapter", {"course": ("in", course_names)})],
		"paths": [_clean(d) for d in paths],
		"quizzes": [_clean(d) for d in quizzes],
		"assignments": [_clean(d) for d in _all("TCD Assignment", {"content": ("in", content_names)})],
		"relations": [
			_clean(d) for d in _all("TCD Content Relation", {"from_content": ("in", content_names)})
		],
	}


# ---------------------------------------------------------------- import


class Importer:
	def __init__(self, bundle: dict, target_space: str | None):
		self.b = bundle
		self.target = (target_space or bundle["space"]["space_name"]).strip()
		self.map: dict[str, dict] = {}
		self.log: list[str] = []
		self.statuses: dict[tuple, str] = {}

	def new(self, doctype: str, old: str | None) -> str | None:
		return self.map.get(doctype, {}).get(old) if old else None

	def put(self, doctype: str, old: str, new: str):
		self.map.setdefault(doctype, {})[old] = new

	def insert(self, doctype: str, data: dict, **override):
		values = {k: v for k, v in data.items() if k != "_id"}
		values.update(override)
		doc = frappe.get_doc({"doctype": doctype, **values})
		doc.insert()
		self.put(doctype, data["_id"], doc.name)
		return doc

	def run(self) -> dict:
		if frappe.db.exists("TCD Space", self.target):
			frappe.throw(
				_("Space {0} already exists. Choose another target space name.").format(
					frappe.bold(self.target)
				)
			)
		space = dict(self.b["space"])
		self.insert("TCD Space", space, space_name=self.target, navigation=[])  # menu: after its targets
		self.natural("TCD Skill", "skills", "skill_name")
		self.natural(
			"TCD Question Category", "question_categories", "category_name", parent="parent_category"
		)
		self.categories()
		self.contents()
		self.questions()
		self.offerings()
		self.quizzes_assignments_relations()
		self.navigation()
		self.restore_statuses()
		counts = {k: len(v) for k, v in self.map.items()}
		return {"space": self.target, "created": counts, "log": self.log}

	def navigation(self):
		"""Space menu (Phase 22): links point to the new pages / courses / paths; others are dropped."""
		rows = self.b["space"].get("navigation") or []
		if not rows:
			return
		targets = {"content": "TCD Content", "course": "TCD Course", "learning_path": "TCD Learning Path"}
		space = frappe.get_doc("TCD Space", self.target)
		for row in rows:
			row = {k: v for k, v in row.items() if k not in ("name", "_id")}
			for field, doctype in targets.items():
				if row.get(field):
					row[field] = self.new(doctype, row[field])
			if row.get("link_type") != "External Link" and not any(row.get(f) for f in targets):
				self.log.append(
					_("Menu item {0} skipped: its target was not exported.").format(row.get("label") or "")
				)
				continue
			space.append("navigation", row)
		space.save()

	def natural(self, doctype, key, field, parent=None):
		for row in self.b.get(key) or []:
			name = row[field]
			if frappe.db.exists(doctype, name):
				self.put(doctype, row["_id"], name)
				continue
			self.insert(doctype, row, **({parent: None} if parent else {}))
		if parent:
			for row in self.b.get(key) or []:
				if row.get(parent) and frappe.db.get_value(doctype, row[field], parent) is None:
					frappe.db.set_value(doctype, row[field], parent, row[parent])

	def categories(self):
		rows = self.b.get("categories") or []
		for row in rows:
			self.insert("TCD Category", row, space=self.target, parent_category=None)
		for row in rows:
			if row.get("parent_category"):
				frappe.db.set_value(
					"TCD Category",
					self.new("TCD Category", row["_id"]),
					"parent_category",
					self.new("TCD Category", row["parent_category"]),
				)

	def contents(self):
		rows = self.b.get("contents") or []
		for row in rows:
			self.statuses[("TCD Content", row["_id"])] = row.get("status") or "Draft"
			self.insert(
				"TCD Content",
				row,
				space=self.target,
				status="Draft",
				category=self.new("TCD Category", row.get("category")),
				parent_content=None,
				lessons=[],
			)
		for row in rows:  # second pass: links between pages
			new = self.new("TCD Content", row["_id"])
			if row.get("parent_content"):
				frappe.db.set_value(
					"TCD Content", new, "parent_content", self.new("TCD Content", row["parent_content"])
				)
			if row.get("lessons"):
				doc = frappe.get_doc("TCD Content", new)
				for lesson in row["lessons"]:
					target = self.new("TCD Content", lesson.get("lesson"))
					if target:
						doc.append("lessons", {**lesson, "lesson": target})
				doc.save()

	def questions(self):
		for row in self.b.get("questions") or []:
			self.insert("TCD Question", row)

	def offerings(self):
		for row in self.b.get("courses") or []:
			self.statuses[("TCD Course", row["_id"])] = row.get("status") or "Draft"
			self.insert(
				"TCD Course",
				row,
				space=self.target,
				status="Draft",
				prerequisites=[],
				category=self.new("TCD Category", row.get("category")),
			)
		for row in self.b.get("courses") or []:
			if row.get("prerequisites"):
				doc = frappe.get_doc("TCD Course", self.new("TCD Course", row["_id"]))
				for p in row["prerequisites"]:
					if self.new("TCD Course", p.get("course")):
						doc.append("prerequisites", {**p, "course": self.new("TCD Course", p["course"])})
				doc.save()
		for row in self.b.get("chapters") or []:
			items = [
				{
					**i,
					"content": self.new("TCD Content", i.get("content")),
					"course": self.new("TCD Course", i.get("course")),
				}
				for i in row.get("items") or []
			]
			self.insert(
				"TCD Chapter",
				row,
				course=self.new("TCD Course", row["course"]),
				space=self.target,
				items=items,
			)
		for row in self.b.get("paths") or []:
			self.statuses[("TCD Learning Path", row["_id"])] = row.get("status") or "Draft"
			items = [
				{
					**i,
					"content": self.new("TCD Content", i.get("content")),
					"course": self.new("TCD Course", i.get("course")),
				}
				for i in row.get("items") or []
			]
			self.insert("TCD Learning Path", row, space=self.target, status="Draft", items=items)

	def quizzes_assignments_relations(self):
		for row in self.b.get("quizzes") or []:
			bank = [
				{**r, "question": self.new("TCD Question", r.get("question"))}
				for r in row.get("bank_items") or []
				if not r.get("question") or self.new("TCD Question", r.get("question"))
			]
			self.insert(
				"TCD Quiz",
				row,
				content=self.new("TCD Content", row["content"]),
				space=self.target,
				bank_items=bank,
			)
		for row in self.b.get("assignments") or []:
			self.insert(
				"TCD Assignment",
				row,
				content=self.new("TCD Content", row.get("content")),
				course=self.new("TCD Course", row.get("course")),
			)
		for row in self.b.get("relations") or []:
			ends = {
				"from_content": self.new("TCD Content", row.get("from_content")),
				"to_content": self.new("TCD Content", row.get("to_content")),
				"to_course": self.new("TCD Course", row.get("to_course")),
				"to_learning_path": self.new("TCD Learning Path", row.get("to_learning_path")),
			}
			if not ends["from_content"] or not any(
				ends[k] for k in ("to_content", "to_course", "to_learning_path")
			):
				self.log.append(f"skipped relation {row['_id']} (target outside the space)")
				continue
			self.insert("TCD Content Relation", row, **ends)

	def restore_statuses(self):
		"""Statuses are set directly (an admin import, like a migration), then published pages get a version
		snapshot and a review date."""
		from vintraxo_tcd.core import content as svc
		from vintraxo_tcd.core import freshness

		now = now_datetime()
		for (doctype, old), status in self.statuses.items():
			name = self.new(doctype, old)
			if not name or status == "Draft":
				continue
			values = {"status": status}
			if doctype == "TCD Content" and status in ("Published", "Approved", "Archived"):
				values.update(approved_by=frappe.session.user, approved_on=now)
				if status == "Published":
					values["published_on"] = now
			frappe.db.set_value(doctype, name, values, update_modified=False)
			if doctype == "TCD Content" and status in ("Published", "Approved"):
				doc = frappe.get_doc("TCD Content", name)
				version = svc.create_snapshot(doc)
				freshness.schedule(doc, getdate(now))
				doc.db_set(
					{
						"current_version": version,
						"content_owner": frappe.session.user,
						"last_reviewed_on": doc.last_reviewed_on,
						"next_review_date": doc.next_review_date,
					},
					update_modified=False,
				)


def parse_bundle(raw: bytes | str) -> dict:
	if isinstance(raw, bytes):
		if len(raw) > MAX_BYTES:
			frappe.throw(_("The file is larger than 20 MB."))
		raw = raw.decode("utf-8")
	try:
		bundle = json.loads(raw)
	except ValueError:
		frappe.throw(_("The file is not a valid export (JSON)."))
	if not isinstance(bundle, dict) or bundle.get("format") != FORMAT:
		frappe.throw(_("The file is not a VintraXo TCD space export."))
	if int(bundle.get("version") or 0) > VERSION:
		frappe.throw(_("The file was made by a newer version of the app. Update the app first."))
	return bundle


def import_bundle(bundle: dict, target_space: str | None = None) -> dict:
	_require_admin()
	return Importer(bundle, target_space).run()


def run_import(name: str) -> dict:
	"""Run a TCD Content Import document (all or nothing)."""
	_require_admin()
	doc = frappe.get_doc("TCD Content Import", name)
	if doc.status == "Completed":
		frappe.throw(_("This import is already done."))
	from frappe.utils.file_manager import get_file

	_file_name, raw = get_file(doc.import_file)
	bundle = parse_bundle(raw)
	savepoint = "tcd_import"
	frappe.db.savepoint(savepoint)
	try:
		result = import_bundle(bundle, doc.target_space)
	except Exception as e:
		frappe.db.rollback(save_point=savepoint)
		doc.db_set({"status": "Failed", "log": f"{type(e).__name__}: {e}"})
		frappe.db.commit()
		raise
	summary = "\n".join(f"{k}: {v}" for k, v in sorted(result["created"].items()))
	doc.db_set(
		{
			"status": "Completed",
			"created_space": result["space"],
			"log": summary + ("\n\n" + "\n".join(result["log"]) if result["log"] else ""),
		}
	)
	return result
