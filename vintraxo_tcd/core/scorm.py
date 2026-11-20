"""SCORM 1.2 / 2004 packages (Phase 16, ADR-0024).

Security: a package is HTML + JavaScript that must run on this origin to reach the SCORM API, so it
runs with the learner's session. Therefore: off by default, administrators only, the zip is checked
before extraction (no path escapes, size limits), the manifest is parsed with defusedxml, and only the
SCORM data model values are stored (size-capped)."""

import hashlib
import json
import os
import posixpath
import shutil
import zipfile

import frappe
from frappe import _

MAX_ZIP_BYTES = 200 * 1024 * 1024
MAX_FILES = 5000
MAX_DATA_CHARS = 64 * 1024
DONE = {"completed", "passed"}


def allowed() -> bool:
	return bool(frappe.db.get_single_value("TCD Settings", "allow_scorm"))


def _zip_path(file_url: str) -> str:
	name = frappe.db.get_value("File", {"file_url": file_url}, "name")
	if not name:
		frappe.throw(_("Upload the SCORM package first."))
	return frappe.get_doc("File", name).get_full_path()


def _launch_href(z: zipfile.ZipFile) -> str:
	from defusedxml import ElementTree  # only needed when a SCORM package is parsed

	try:
		root = ElementTree.fromstring(z.read("imsmanifest.xml"))
	except KeyError:
		frappe.throw(_("This is not a SCORM package (imsmanifest.xml is missing)."))
	except Exception:
		frappe.throw(_("The SCORM manifest could not be read."))
	resources = {}
	for el in root.iter():
		if el.tag.split("}")[-1] == "resource" and el.get("href"):
			resources[el.get("identifier")] = el.get("href")
	for el in root.iter():  # first item of the default organization that points to a resource
		if el.tag.split("}")[-1] == "item" and el.get("identifierref") in resources:
			return resources[el.get("identifierref")]
	if resources:
		return next(iter(resources.values()))
	frappe.throw(_("The SCORM manifest has no launch page."))


def _safe_members(z: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
	members = z.infolist()
	if len(members) > MAX_FILES:
		frappe.throw(_("The SCORM package has too many files."))
	if sum(m.file_size for m in members) > MAX_ZIP_BYTES:
		frappe.throw(_("The SCORM package is too large."))
	for m in members:
		name = m.filename.replace("\\", "/")
		norm = posixpath.normpath(name)
		if name.startswith("/") or norm.startswith("..") or "/../" in f"/{name}" or ":" in name.split("/")[0]:
			frappe.throw(_("The SCORM package contains an unsafe path: {0}").format(m.filename))
	return members


def install(doc):
	"""Called from TCD Content.validate when the package changes: check, extract, set the launch URL."""
	if not doc.get("scorm_package"):
		doc.scorm_launch = None
		return
	before = doc.get_doc_before_save()
	if before and before.get("scorm_package") == doc.scorm_package and doc.scorm_launch:
		return
	if not allowed():
		frappe.throw(
			_("SCORM packages are not allowed. An administrator can allow them in Learning Settings.")
		)
	if not set(frappe.get_roles()) & {"TCD Administrator", "System Manager"}:
		frappe.throw(_("Only administrators can upload SCORM packages."), frappe.PermissionError)
	path = _zip_path(doc.scorm_package)
	if not zipfile.is_zipfile(path):
		frappe.throw(_("The SCORM package must be a .zip file."))
	with zipfile.ZipFile(path) as z:
		members = _safe_members(z)
		href = _launch_href(z)
		digest = hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]
		folder = f"scorm/{frappe.scrub(doc.name or 'new')}-{digest}"
		target = frappe.get_site_path("public", "files", folder)
		if os.path.isdir(target):
			shutil.rmtree(target)
		os.makedirs(target, exist_ok=True)
		for m in members:
			if m.is_dir():
				continue
			dest = os.path.realpath(os.path.join(target, m.filename))
			if not dest.startswith(os.path.realpath(target) + os.sep):
				frappe.throw(_("The SCORM package contains an unsafe path: {0}").format(m.filename))
			os.makedirs(os.path.dirname(dest), exist_ok=True)
			with z.open(m) as src, open(dest, "wb") as out:
				shutil.copyfileobj(src, out)
	href = posixpath.normpath(href.split("?")[0]).lstrip("/")
	if href.startswith(".."):
		frappe.throw(_("The SCORM launch page is outside the package."))
	doc.scorm_launch = f"/files/{folder}/{href}"
	doc.lesson_type = "SCORM"


def get_data(user: str, content: str) -> dict:
	raw = frappe.db.get_value("TCD Progress", {"user": user, "content": content}, "scorm_data")
	try:
		return json.loads(raw) if raw else {}
	except ValueError:
		return {}


def commit(user: str, content: str, data: dict) -> dict:
	"""Store the SCORM values; a completed / passed status completes the lesson."""
	from vintraxo_tcd.core import progress

	if isinstance(data, str):
		data = json.loads(data or "{}")
	values = {str(k)[:255]: str(v)[:4096] for k, v in (data or {}).items() if str(k).startswith("cmi.")}
	merged = {**get_data(user, content), **values}
	blob = json.dumps(merged, ensure_ascii=False)
	if len(blob) > MAX_DATA_CHARS:
		frappe.throw(_("The SCORM data is too large."))
	doc = progress.get_progress(user, content) or progress.track_view(user, content)
	doc.db_set("scorm_data", blob, update_modified=False)
	status = (
		merged.get("cmi.core.lesson_status")
		or merged.get("cmi.success_status")
		or merged.get("cmi.completion_status")
		or ""
	).lower()
	completed = False
	if status in DONE and doc.status != "Completed":
		progress.complete(user, content, from_quiz=True)  # requirements unmet: stays open, no error
		completed = frappe.db.get_value("TCD Progress", doc.name, "status") == "Completed"
	return {"saved": True, "completed": completed}
