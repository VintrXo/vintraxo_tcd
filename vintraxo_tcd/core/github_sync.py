"""Docs as code (Phase 16, ADR-0024): sync a space's pages with a GitHub repository as Markdown.

Push writes published pages (front matter + Markdown) through the GitHub Contents API; unchanged files
are skipped. Pull never overwrites: new files become Draft pages and changed pages become suggested
edits (TCD Change Request) that a reviewer accepts. Administrators only."""

import base64
import json
import re

import frappe
import requests
from frappe import _
from frappe.utils import now_datetime

from vintraxo_tcd.core import content as svc
from vintraxo_tcd.core.permissions import is_admin

API = "https://api.github.com"
FRONT = re.compile(r"^---\n(.*?)\n---\n?", re.S)
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _require_admin():
	if not is_admin(frappe.session.user):
		frappe.throw(_("Only administrators can sync with GitHub."), frappe.PermissionError)


def _cfg(space: str) -> dict:
	sp = frappe.get_doc("TCD Space", space)
	token = sp.get_password("github_token", raise_exception=False) if sp.get("github_token") else None
	if not (sp.get("github_repo") and REPO.match(sp.github_repo) and token):
		frappe.throw(_("Set the repository (owner/name) and the access token on the space first."))
	path = (sp.get("github_path") or "").strip("/")
	if ".." in path.split("/"):
		frappe.throw(_("The folder cannot contain '..'."))
	return {
		"space": sp,
		"repo": sp.github_repo,
		"branch": sp.get("github_branch") or "main",
		"path": path,
		"headers": {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
	}


# ---------------------------------------------------------------- Markdown conversion


def to_markdown(doc) -> str:
	lines = []
	for b in svc.parse_blocks(doc.blocks):
		t = b.get("type")
		if t == "heading":
			lines.append("#" * min(int(b.get("level") or 2) + 1, 6) + " " + (b.get("text") or ""))
		elif t in ("paragraph", "markdown"):
			lines.append(b.get("text") or "")
		elif t == "code":
			lines.append(f"```{b.get('language') or ''}\n{b.get('code') or ''}\n```")
		elif t == "playground":
			lines.append(f"```{b.get('language') or ''}\n{b.get('code') or ''}\n```")
		elif t == "list":
			mark = "1." if b.get("ordered") else "-"
			lines.append("\n".join(f"{mark} {i}" for i in b.get("items") or []))
		elif t == "callout":
			title = f"**{b['title']}** " if b.get("title") else ""
			lines.append("> " + title + (b.get("text") or "").replace("\n", "\n> "))
		elif t == "image":
			lines.append(f"![{b.get('alt') or ''}]({b.get('url') or ''})")
		elif t == "exercise":
			lines.append("> **" + (b.get("prompt") or "") + "**")
			lines.append(f"```{b.get('language') or ''}\n{b.get('code') or ''}\n```")
		elif t in ("link", "video", "file"):
			lines.append(f"[{b.get('title') or b.get('url')}]({b.get('url') or ''})")
	front = {
		"title": doc.title,
		"tcd_id": doc.name,
		"content_type": doc.content_type,
		"summary": doc.summary or "",
	}
	head = "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in front.items())
	return f"---\n{head}\n---\n\n" + "\n\n".join(lines).strip() + "\n"


def parse_markdown(text: str) -> tuple[dict, str]:
	meta = {}
	m = FRONT.match(text)
	if m:
		for line in m.group(1).splitlines():
			key, _sep, value = line.partition(":")
			try:
				meta[key.strip()] = json.loads(value.strip())
			except ValueError:
				meta[key.strip()] = value.strip()
		text = text[m.end() :]
	return meta, text.strip()


# ---------------------------------------------------------------- push / pull


def _file_url(cfg, slug: str) -> str:
	path = f"{cfg['path']}/{slug}.md" if cfg["path"] else f"{slug}.md"
	return f"{API}/repos/{cfg['repo']}/contents/{path}"


def push(space: str) -> dict:
	_require_admin()
	cfg = _cfg(space)
	written = skipped = 0
	for name in frappe.get_all("TCD Content", filters={"space": space, "status": "Published"}, pluck="name"):
		doc = frappe.get_doc("TCD Content", name)
		body = to_markdown(doc)
		url = _file_url(cfg, doc.slug)
		r = requests.get(url, headers=cfg["headers"], params={"ref": cfg["branch"]}, timeout=20)
		sha = None
		if r.status_code == 200:
			current = r.json()
			sha = current.get("sha")
			if base64.b64decode(current.get("content") or "").decode(errors="replace") == body:
				skipped += 1
				continue
		elif r.status_code != 404:
			frappe.throw(_("GitHub returned an error ({0}).").format(r.status_code))
		payload = {
			"message": f"VintraXo TCD: update {doc.title}",
			"content": base64.b64encode(body.encode()).decode(),
			"branch": cfg["branch"],
		}
		if sha:
			payload["sha"] = sha
		put = requests.put(url, headers=cfg["headers"], json=payload, timeout=20)
		if put.status_code not in (200, 201):
			frappe.throw(_("GitHub refused the update of {0} ({1}).").format(doc.slug, put.status_code))
		written += 1
	return _done(cfg, {"written": written, "unchanged": skipped})


def pull(space: str) -> dict:
	_require_admin()
	cfg = _cfg(space)
	base = (
		f"{API}/repos/{cfg['repo']}/contents/{cfg['path']}"
		if cfg["path"]
		else f"{API}/repos/{cfg['repo']}/contents"
	)
	r = requests.get(base, headers=cfg["headers"], params={"ref": cfg["branch"]}, timeout=20)
	if r.status_code != 200:
		frappe.throw(_("GitHub returned an error ({0}).").format(r.status_code))
	created = suggested = unchanged = 0
	for entry in r.json():
		if entry.get("type") != "file" or not entry.get("name", "").endswith(".md"):
			continue
		f = requests.get(entry["url"], headers=cfg["headers"], params={"ref": cfg["branch"]}, timeout=20)
		if f.status_code != 200:
			continue
		meta, body = parse_markdown(base64.b64decode(f.json().get("content") or "").decode(errors="replace"))
		slug = entry["name"][:-3]
		name = (
			meta.get("tcd_id")
			if frappe.db.exists("TCD Content", {"name": meta.get("tcd_id") or "", "space": space})
			else None
		)
		name = name or frappe.db.get_value("TCD Content", {"space": space, "slug": slug})
		blocks = [{"type": "markdown", "text": body}] if body else []
		title = (meta.get("title") or slug).strip()[:140]
		if not name:
			frappe.get_doc(
				{
					"doctype": "TCD Content",
					"space": space,
					"title": title,
					"content_type": meta.get("content_type")
					if meta.get("content_type") in ("Article", "Reference", "Lesson")
					else "Article",
					"summary": (meta.get("summary") or "")[:500],
					"status": "Draft",
					"blocks": json.dumps(blocks, ensure_ascii=False),
				}
			).insert()
			created += 1
			continue
		doc = frappe.get_doc("TCD Content", name)
		if to_markdown(doc).split("\n---\n", 1)[-1].strip() == body and doc.title == title:
			unchanged += 1
			continue
		_suggest(doc, title, blocks)
		suggested += 1
	return _done(cfg, {"created": created, "suggested": suggested, "unchanged": unchanged})


def _suggest(doc, title: str, blocks: list):
	from vintraxo_tcd.core.change_requests import DOCTYPE, _hash

	cr = frappe.get_doc(
		{
			"doctype": DOCTYPE,
			"content": doc.name,
			"user": frappe.session.user,
			"status": "Open",
			"summary": _("Changed in GitHub"),
			"proposed_title": title,
			"proposed_blocks": json.dumps(svc.validate_blocks(blocks), ensure_ascii=False),
			"base_hash": _hash(doc.blocks),
		}
	)
	cr.flags.from_service = True
	cr.insert(ignore_permissions=True)


def _done(cfg, result: dict) -> dict:
	cfg["space"].db_set(
		{"github_last_sync": now_datetime(), "github_last_result": json.dumps(result)}, update_modified=False
	)
	return result
