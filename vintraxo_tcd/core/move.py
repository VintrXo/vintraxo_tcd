"""Carry the learning content to a server that already runs its own site (ADR-0035).

A full restore would overwrite that site, so only the spaces travel, through the space export of Phase 13:

    internal:  bench --site <old> execute vintraxo_tcd.core.move.export_spaces --kwargs "{'out_dir': '/path/spaces'}"
    server:    bench --site <new> execute vintraxo_tcd.core.move.import_spaces --kwargs "{'in_dir': '/path/spaces'}"

Import is safe to run again: a space whose name already exists on the server is skipped, never merged or
overwritten. Command line only (bench execute), never over HTTP."""

import json
import os

import frappe

from vintraxo_tcd.core import transfer


def _cli_only():
	from vintraxo_tcd.core.server_keys import cli_setup

	cli_setup()


def export_spaces(out_dir: str, spaces: list | None = None) -> list[str]:
	_cli_only()
	os.makedirs(out_dir, exist_ok=True)
	names = spaces or frappe.get_all(
		"TCD Space", filters={"is_active": 1}, pluck="name", order_by="creation asc"
	)
	written = []
	for name in names:
		bundle = transfer.export_space(name)
		path = os.path.join(out_dir, f"{name}.json")
		with open(path, "w", encoding="utf-8") as f:
			json.dump(bundle, f, ensure_ascii=False, default=str)
		os.chmod(path, 0o600)  # quiz answers inside
		print(f"[EXPORT ] {name} -> {path}")
		written.append(path)
	files = frappe.db.count("File", {"attached_to_doctype": ("like", "TCD %")})
	if files:
		print(
			f"note: {files} uploaded files are attached to learning records; copy them with the site files."
		)
	return written


def import_spaces(in_dir: str) -> dict:
	_cli_only()
	report = {}
	for file in sorted(f for f in os.listdir(in_dir) if f.endswith(".json")):
		with open(os.path.join(in_dir, file), "rb") as f:
			bundle = transfer.parse_bundle(f.read())
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
