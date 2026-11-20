"""Carry the learning content to a server that already runs its own site (ADR-0035).

A full restore would overwrite that site, so only the spaces travel, through the space export of Phase 13:

    internal:  bench --site <old> execute vintraxo_tcd.core.move.export_spaces --kwargs "{'out_dir': '/path/spaces'}"
    server:    bench --site <new> execute vintraxo_tcd.core.move.import_spaces --kwargs "{'in_dir': '/path/spaces'}"

Import is safe to run again: a space whose name already exists on the server is skipped, never merged or
overwritten. Command line only (bench execute), never over HTTP."""

import hashlib
import json
import os
import re
import shutil

import frappe

from vintraxo_tcd.core import transfer

# files used by the exported records: image / file blocks, Markdown links, attachments
FILE_URL = re.compile(r"/(?:private/)?files/[^\s\"'()\[\]<>\\]+")


def _cli_only():
	from vintraxo_tcd.core.server_keys import cli_setup

	cli_setup()


def export_spaces(out_dir: str, spaces: list | None = None) -> list[str]:
	_cli_only()
	os.makedirs(out_dir, exist_ok=True)
	names = spaces or frappe.get_all(
		"TCD Space", filters={"is_active": 1}, pluck="name", order_by="creation asc"
	)
	written, urls = [], set()
	for name in names:
		bundle = transfer.export_space(name)
		raw = json.dumps(bundle, ensure_ascii=False, default=str)
		urls |= set(FILE_URL.findall(raw))
		path = os.path.join(out_dir, f"{name}.json")
		with open(path, "w", encoding="utf-8") as f:
			f.write(raw)
		os.chmod(path, 0o600)  # quiz answers inside
		print(f"[EXPORT ] {name} -> {path}")
		written.append(path)
	_export_files(out_dir, urls)
	return written


def _export_files(out_dir: str, urls: set):
	folder = os.path.join(out_dir, "files")
	manifest, missing = {}, []
	for url in sorted(urls):
		row = frappe.db.get_value(
			"File", {"file_url": url}, ["name", "file_name", "is_private"], as_dict=True
		)
		path = frappe.get_doc("File", row.name).get_full_path() if row else None
		if not path or not os.path.exists(path):
			missing.append(url)
			continue
		os.makedirs(folder, exist_ok=True)
		stored = hashlib.sha1(url.encode()).hexdigest()[:12] + "-" + os.path.basename(path)
		shutil.copyfile(path, os.path.join(folder, stored))
		manifest[url] = {"file": stored, "file_name": row.file_name, "is_private": int(row.is_private or 0)}
	if manifest:
		with open(os.path.join(folder, "manifest.json"), "w", encoding="utf-8") as f:
			json.dump(manifest, f, ensure_ascii=False)
		print(f"[FILES  ] {len(manifest)} files -> {folder}")
	for url in missing:
		print(f"[MISSING] {url} (referenced but not found on this site)")


def _import_files(in_dir: str) -> dict:
	"""Create the exported files that this site does not have; returns {old url: new url} when it changed."""
	path = os.path.join(in_dir, "files", "manifest.json")
	if not os.path.exists(path):
		return {}
	with open(path, encoding="utf-8") as f:
		manifest = json.load(f)
	changed, created = {}, 0
	for url, m in manifest.items():
		existing = frappe.db.get_value("File", {"file_url": url}, "name")
		if existing and os.path.exists(frappe.get_doc("File", existing).get_full_path()):
			continue
		with open(os.path.join(in_dir, "files", m["file"]), "rb") as f:
			content = f.read()
		doc = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": m["file_name"],
				"content": content,
				"is_private": m["is_private"],
			}
		).insert(ignore_permissions=True)
		created += 1
		if doc.file_url != url:
			changed[url] = doc.file_url
	frappe.db.commit()
	print(f"[FILES  ] {created} files created, {len(manifest) - created} already here")
	return changed


def import_spaces(in_dir: str) -> dict:
	_cli_only()
	report = {}
	changed = _import_files(in_dir)
	for file in sorted(f for f in os.listdir(in_dir) if f.endswith(".json")):
		with open(os.path.join(in_dir, file), encoding="utf-8") as f:
			raw = f.read()
		for old, new in sorted(changed.items(), key=lambda kv: -len(kv[0])):  # longest first
			raw = raw.replace(old, new)
		bundle = transfer.parse_bundle(raw.encode("utf-8"))
		name = bundle["space"]["space_name"]
		if frappe.db.exists("TCD Space", name):
			report[name] = "skipped (already here)"
		else:
			frappe.db.savepoint("tcd_move")
			try:
				result = transfer.import_bundle(bundle)
				frappe.db.commit()
				report[name] = ", ".join(f"{k}: {v}" for k, v in sorted(result["created"].items()))
			except Exception as e:
				frappe.db.rollback(save_point="tcd_move")
				frappe.clear_messages()
				report[name] = f"failed: {type(e).__name__}: {str(e)[:200]}"
		print(f"[IMPORT ] {name}: {report[name]}")
	return report
