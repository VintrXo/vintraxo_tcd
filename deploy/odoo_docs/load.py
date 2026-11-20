"""Load converted Odoo docs into a site as two spaces (EN + AR). Run inside the site:

    bench --site <site> execute? no: bench --site <site> console < this file  (after setting CONFIG below)

Idempotent per space: a space that already exists is skipped; images already uploaded are reused."""

import json
import os
import pathlib

import frappe

from vintraxo_tcd.core import transfer

CONFIG = json.loads(os.environ.get("ODOO_LOAD", "{}")) or globals().get("CONFIG_OVERRIDE")
ROOT = pathlib.Path(CONFIG["root"])
SPACES = CONFIG["spaces"]  # {"en": "odoo-en", "ar": "odoo-ar"}
ONLY = CONFIG.get("only")  # optional list of page prefixes (pilot)

TEXT = {
	"en": {
		"title": "Odoo 18 documentation (English)",
		"desc": "Odoo 18.0 user documentation. Source: odoo.com/documentation, © Odoo S.A., CC BY-SA 4.0.",
		"switch": "اقرأ هذه الصفحة بالعربية",
		"source": "Source: [Odoo 18.0 documentation — {title}]({url}), © Odoo S.A., licensed under "
		"[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Converted to this platform's "
		"format; content unchanged.",
	},
	"ar": {
		"title": "وثائق أودو 18 (عربي)",
		"desc": "وثائق المستخدم لأودو 18.0. المصدر: odoo.com/documentation، © Odoo S.A.، برخصة CC BY-SA 4.0.",
		"switch": "Read this page in English",
		"source": "المصدر: [وثائق أودو 18.0 — {title}]({url})، © Odoo S.A.، مرخّصة بموجب "
		"[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). تم تحويل التنسيق لهذه المنصة "
		"دون تغيير المحتوى.",
	},
}


def wanted(page):
	return not ONLY or any(page == p or page.startswith(p + "/") for p in ONLY)


def upload_images(keys):
	images = json.loads((ROOT / "images.json").read_text())
	cache_path = ROOT / f"image_urls_{frappe.local.site}.json"
	cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
	for n, key in enumerate(sorted(keys), 1):
		if key in cache and frappe.db.exists("File", {"file_url": cache[key]}):
			continue
		source = images[key]
		if source.startswith("https://www.odoo.com/"):  # not in the repository clone: the published copy
			import requests

			r = requests.get(source, timeout=30)
			r.raise_for_status()
			content = r.content
		else:
			content = pathlib.Path(source).read_bytes()
		f = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": "odoo-" + pathlib.Path(key).name,
				"content": content,
				"is_private": 0,
				"folder": "Home",
			}
		).insert(ignore_permissions=True)
		cache[key] = f.file_url
		if n % 200 == 0:
			frappe.db.commit()
			cache_path.write_text(json.dumps(cache))
			print(f"  images {n}/{len(keys)}", flush=True)
	frappe.db.commit()
	cache_path.write_text(json.dumps(cache))
	return cache


def build(lang, pages, urls):
	other = SPACES["ar" if lang == "en" else "en"]
	t = TEXT[lang]
	contents = []
	for p in pages:
		blocks = []
		blocks.append({"type": "paragraph", "text": f"[[{other}/{p['slug']}|{t['switch']}]]"})
		for b in p["blocks"]:
			b = dict(b)
			if b["type"] == "image":
				b["url"] = urls[b["url"][4:]]
			blocks.append(b)
		blocks.append({"type": "paragraph", "text": t["source"].format(title=p["title"].replace("[", "").replace("]", ""), url=p["url"])})
		contents.append(
			{
				"_id": p["page"],
				"title": p["title"],
				"slug": p["slug"],
				"content_type": "Article",
				"language": lang,
				"visibility": "Public",
				"status": "Published",
				"summary": p["summary"],
				"blocks": json.dumps(blocks, ensure_ascii=False),
				"parent_content": p["parent"],
				"skip_review": 1,
			}
		)
	return {
		"format": transfer.FORMAT,
		"version": transfer.VERSION,
		"space": {"_id": SPACES[lang], "space_name": SPACES[lang], "title": t["title"], "visibility": "Public", "is_active": 1, "description": t["desc"]},
		"contents": contents,
	}


def navigation(lang, pages):
	"""Menu: one group per Odoo area (Finance, Sales…), listing its apps."""
	space = frappe.get_doc("TCD Space", SPACES[lang])
	by_page = {p["page"]: p for p in pages}
	space.navigation = []
	for area in sorted(p["page"] for p in pages if p["page"].count("/") == 1):
		group = by_page[area]["title"]
		children = [p for p in pages if p["parent"] == area]
		for child in sorted(children, key=lambda c: c["title"]):
			name = frappe.db.get_value("TCD Content", {"space": space.name, "slug": child["slug"]})
			if name:
				space.append("navigation", {"group_title": group[:140], "link_type": "Page", "content": name})
	space.save(ignore_permissions=True)


def main():
	frappe.set_user("Administrator")
	if not getattr(frappe.local, "lang", None):
		frappe.local.lang = "en"
	data = {lang: [p for p in json.loads((ROOT / f"pages_{lang}.json").read_text()) if wanted(p["page"])] for lang in ("en", "ar")}
	keys = {b["url"][4:] for pages in data.values() for p in pages for b in p["blocks"] if b["type"] == "image"}
	print(f"pages: en {len(data['en'])}, ar {len(data['ar'])}; images {len(keys)}", flush=True)
	urls = upload_images(keys)
	for lang in ("en", "ar"):
		if frappe.db.exists("TCD Space", SPACES[lang]):
			print(f"{SPACES[lang]}: already here, skipped")
			continue
		result = transfer.import_bundle(build(lang, data[lang], urls))  # pages go in as Draft, then statuses
		frappe.db.commit()
		navigation(lang, data[lang])
		frappe.db.commit()
		print(SPACES[lang], result["created"], "log:", result["log"][:5], flush=True)


main()
