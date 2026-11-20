"""Repair pages saved while requests decoded UTF-8 as Latin-1 (lossless: Latin-1 maps every byte)."""
import json, pathlib, sys
fixed = 0
for f in pathlib.Path(sys.argv[1]).rglob("*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))
    try:
        html = d["html"].encode("latin-1").decode("utf-8")
        title = d["title"].encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        continue  # already correct
    d["html"], d["title"] = html, title
    f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    fixed += 1
print("fixed", fixed)
