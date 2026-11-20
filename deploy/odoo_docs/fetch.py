"""Download the article body of every Odoo 18.0 user-doc page (EN + AR) from odoo.com. Data only."""
import json, pathlib, sys, time
import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(sys.argv[1])            # scratchpad/odoo
SRC = ROOT / "docs" / "content"
OUT = ROOT / "html"
BASE = "https://www.odoo.com/documentation/18.0/"
pages = sorted(str(p.relative_to(SRC))[:-4] for p in (SRC / "applications").rglob("*.rst"))
pages.insert(0, "applications")
s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (internal training import; CC BY-SA docs)"
failed = []
for i, page in enumerate(pages, 1):
    for lang in ("en", "ar"):
        out = OUT / lang / (page + ".json")
        if out.exists():
            continue
        url = BASE + ("ar/" if lang == "ar" else "") + page + ".html"
        for attempt in range(3):
            try:
                r = s.get(url, timeout=30)
                if r.status_code == 404:
                    break
                r.raise_for_status()
                r.encoding = "utf-8"  # the server sends no charset: requests would guess Latin-1
                soup = BeautifulSoup(r.text, "html.parser")
                art = soup.select_one("article#o_content")
                if art is None:  # redirect stub page
                    break
                out.parent.mkdir(parents=True, exist_ok=True)
                title = (soup.title.get_text() if soup.title else "").split(" — ")[0]
                out.write_text(json.dumps({"page": page, "url": url, "title": title, "html": str(art)}, ensure_ascii=False))
                break
            except Exception as e:
                time.sleep(3 * (attempt + 1))
        else:
            failed.append(url)
        if not out.exists() and url not in failed:
            failed.append(url + " (no article)")
        time.sleep(0.4)
    if i % 50 == 0:
        print(f"{i}/{len(pages)} pages", flush=True)
print("done", len(pages), "pages; failed:", len(failed))
(ROOT / "fetch_failed.txt").write_text("\n".join(failed))
