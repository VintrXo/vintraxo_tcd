"""Convert fetched Odoo doc articles (html/<lang>/<page>.json) into TCD blocks. Pure data: no network, no code
from the downloaded repo is run. Output: pages_<lang>.json = [{page, slug, parent, title, summary, blocks}],
plus images.json = {image key: local file path or remote url}.

python -I convert.py <odoo dir>"""

import json
import pathlib
import posixpath
import re
import sys

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = pathlib.Path(sys.argv[1])
SRC = ROOT / "docs" / "content"
SITE = "https://www.odoo.com/documentation/18.0/"
VARIANT = {
	"alert-primary": "info",  # note
	"alert-info": "info",
	"alert-secondary": "tip",  # see also
	"alert-tip": "tip",
	"alert-success": "tip",  # example
	"alert-warning": "warning",
	"alert-danger": "danger",
}
IMAGE_EXT = (".png", ".gif", ".jpg", ".jpeg", ".svg", ".webp")

# every image in the repo, by basename
LOCAL = {}
for p in (SRC / "applications").rglob("*"):
	if p.suffix.lower() in IMAGE_EXT:
		LOCAL.setdefault(p.name, []).append(p)


def slug_for(page: str) -> str:
	s = page.removeprefix("applications/").replace("/", "-").replace("_", "-").lower()
	return s or "odoo"


def esc(text: str) -> str:
	return re.sub(r"([\\`*_\[\]<>])", r"\\\1", text)


class Page:
	def __init__(self, lang, data, pages, images):
		self.lang, self.page, self.url = lang, data["page"], data["url"]
		self.pages, self.images = pages, images
		self.soup = BeautifulSoup(data["html"], "html.parser")
		self.blocks = []
		self.title = data["title"]

	# ------------------------------------------------------------ links and images
	def resolve(self, href: str) -> str | None:
		"""Relative .html link of the built site -> our page id."""
		if not href or href.startswith(("http:", "https:", "mailto:", "#")):
			return None
		path = href.split("#")[0]
		if not path.endswith(".html"):
			return None
		target = posixpath.normpath(posixpath.join(posixpath.dirname(self.page), path))[:-5]
		return target if target in self.pages else None

	def image(self, src: str) -> str | None:
		name = posixpath.basename(src.split("?")[0])
		page_dir = SRC / posixpath.dirname(self.page) / posixpath.basename(self.page)
		candidates = LOCAL.get(name) or LOCAL.get(re.sub(r"\d+(\.\w+)$", r"\1", name)) or []
		local = None
		if len(candidates) == 1:
			local = candidates[0]
		elif candidates:  # same name in several folders: the one next to this page
			near = [c for c in candidates if str(c).startswith(str(page_dir))] or [
				c for c in candidates if str(c).startswith(str(SRC / posixpath.dirname(self.page)))
			]
			local = (near or candidates)[0]
		key = str(local.relative_to(SRC)) if local else "remote/" + name
		self.images[key] = str(local) if local else posixpath.normpath(
			posixpath.join(posixpath.dirname(self.url), src)
		).replace("https:/", "https://")
		return key

	# ------------------------------------------------------------ inline Markdown
	def inline(self, node) -> str:
		if isinstance(node, NavigableString):
			return esc(str(node))
		if not isinstance(node, Tag):
			return ""
		cls = node.get("class") or []
		if node.name == "a" and "headerlink" in cls:
			return ""
		if node.name == "i" and any(c.startswith(("fa", "i-")) for c in cls):
			return ""
		if node.name == "img":
			return ""
		inner = "".join(self.inline(c) for c in node.children)
		text = inner.strip()
		if not text:
			return inner
		glued = self.glued(node)
		if node.name in ("strong", "b") or (node.name == "span" and ({"guilabel", "menuselection"} & set(cls))):
			return f"<strong>{text}</strong>" if glued else f"**{text}**"
		if node.name in ("em",) or (node.name == "i"):
			return f"<em>{text}</em>" if glued else f"*{text}*"
		if node.name in ("code", "kbd", "tt") or "pre" in cls:
			plain = node.get_text()
			return f"`{plain}`" if "`" not in plain else plain
		if node.name == "a":
			href = node.get("href") or ""
			target = self.resolve(href)
			label = text.replace("[", "").replace("]", "").replace("|", " ")
			if target:
				return f"[[{slug_for(target)}|{label}]]"
			if href.startswith(("http://", "https://")):
				return f"[{label}]({href})"
			if "download" in cls and not href.startswith("#"):
				full = posixpath.normpath(posixpath.join(posixpath.dirname(self.url), href)).replace("https:/", "https://")
				return f"[{label}]({full})"
			return inner
		if node.name == "br":
			return "  \n"
		return inner

	@staticmethod
	def glued(node) -> bool:
		"""Emphasis touching a letter (Arabic 'و**الدفع**'): Markdown would not see it, use HTML."""
		before = node.previous_sibling
		after = node.next_sibling
		b = str(before)[-1:] if isinstance(before, NavigableString) else ""
		a = str(after)[:1] if isinstance(after, NavigableString) else ""
		return bool(re.match(r"\w", b) or re.match(r"\w", a))

	def text_of(self, node) -> str:
		text = re.sub(r"[ \t\r\n]+", " ", self.inline(node)).strip()
		# translators sometimes typed Markdown bold into the source text ("**word**"): show it as bold
		text = re.sub(r"\\\*\\\*([^*\n]+?)\\\*\\\*", r"<strong>\1</strong>", text)
		return re.sub(r"\\\*\\\*", "", text)  # unmatched leftovers of such typos

	# ------------------------------------------------------------ lists
	def md_list(self, node, depth=0) -> str:
		lines, n = [], 0
		for li in node.find_all("li", recursive=False):
			n += 1
			bullet = f"{n}." if node.name == "ol" else "-"
			parts, subs = [], []
			for child in li.children:
				if isinstance(child, Tag) and child.name in ("ul", "ol"):
					subs.append(self.md_list(child, depth + 1))
				elif isinstance(child, Tag) and child.name == "img":
					self.pending_images.append(child)
				elif isinstance(child, Tag) and child.name == "div" and "alert" in (child.get("class") or []):
					parts.append(self.text_of(child))
				else:
					if isinstance(child, Tag):
						for img in child.find_all("img"):
							self.pending_images.append(img)
					parts.append(self.text_of(child) if isinstance(child, Tag) else esc(str(child)).strip())
			line = " ".join(p for p in parts if p)
			lines.append("   " * depth + f"{bullet} {line}")
			lines.extend(s for s in subs if s)
		return "\n".join(lines)

	# ------------------------------------------------------------ blocks
	def add(self, block):
		self.blocks.append(block)

	def add_image(self, img, caption=""):
		src = img.get("src")
		if not src or src.startswith("data:"):
			return
		key = self.image(src)
		block = {"type": "image", "url": "IMG:" + key, "alt": (img.get("alt") or "")[:300]}
		if caption:
			block["caption"] = caption[:500]
		self.add(block)

	def table(self, node):
		for tag in node.find_all(True):
			keep = {k: v for k, v in tag.attrs.items() if k in ("colspan", "rowspan")}
			tag.attrs = keep
		for tag in node.find_all(["col", "colgroup"]):
			tag.decompose()
		for cell in node.find_all(["td", "th"]):
			for img in cell.find_all("img"):
				img.decompose()
			text = re.sub(r"\s+", " ", cell.get_text()).strip()
			cell.clear()
			cell.append(text)  # plain text: Markdown is not parsed inside raw HTML
		return str(node)

	def walk(self, node):
		for child in node.children:
			if isinstance(child, NavigableString):
				if str(child).strip():
					self.add({"type": "paragraph", "text": esc(str(child).strip())})
				continue
			if not isinstance(child, Tag):
				continue
			cls = child.get("class") or []
			name = child.name
			if name in ("section", "article") or (name == "div" and (child.get("role") == "main" or not cls)):
				self.walk(child)
			elif name == "h1":
				continue  # page title
			elif name in ("h2", "h3", "h4", "h5", "h6"):
				text = self.text_of(child).replace("**", "")
				if text:
					self.add({"type": "heading", "text": text, "level": min(int(name[1]), 4)})
			elif name == "p":
				imgs = child.find_all("img")
				text = self.text_of(child)
				if text:
					self.add({"type": "paragraph", "text": text})
				for img in imgs:
					self.add_image(img)
			elif name in ("ul", "ol"):
				self.pending_images = []
				text = self.md_list(child)
				if text.strip():
					self.add({"type": "markdown", "text": text})
				for img in self.pending_images:
					self.add_image(img)
			elif name == "img":
				self.add_image(child)
			elif name == "figure":
				cap = child.find("figcaption")
				for img in child.find_all("img"):
					self.add_image(img, self.text_of(cap) if cap else "")
			elif name == "div" and "alert" in cls:
				variant = next((VARIANT[c] for c in cls if c in VARIANT), "info")
				title_el = child.find("p", class_="alert-title")
				title = self.text_of(title_el).replace("**", "") if title_el else ""
				if title_el:
					title_el.decompose()
				self.pending_images = []
				parts = []
				for c in child.children:
					if isinstance(c, Tag) and c.name in ("ul", "ol"):
						parts.append(self.md_list(c))
					elif isinstance(c, Tag):
						self.pending_images += c.find_all("img") if c.name != "img" else [c]
						t = self.text_of(c)
						if t:
							parts.append(t)
				text = "\n\n".join(p for p in parts if p)
				if text:
					block = {"type": "callout", "variant": variant, "text": text}
					if title:
						block["title"] = title[:200]
					self.add(block)
				for img in self.pending_images:
					self.add_image(img)
			elif name == "div" and "highlight" in " ".join(cls) or name == "pre":
				pre = child if name == "pre" else child.find("pre")
				if pre:
					lang = next((c[len("highlight-"):] for c in cls if c.startswith("highlight-")), "")
					block = {"type": "code", "code": pre.get_text().rstrip("\n")}
					if lang and lang not in ("default", "none"):
						block["language"] = lang
					self.add(block)
			elif name == "table":
				self.add({"type": "markdown", "text": self.table(child)})
			elif name == "dl":
				lines = []
				for dt in child.find_all("dt", recursive=False):
					dd = dt.find_next_sibling("dd")
					lines.append(f"- **{self.text_of(dt).replace('**', '')}**: {self.text_of(dd) if dd else ''}")
				if lines:
					self.add({"type": "markdown", "text": "\n".join(lines)})
			elif name == "div" and "sphinx-tabs" in cls:
				labels = [self.text_of(b) for b in child.find_all("button", class_="sphinx-tabs-tab")]
				panels = child.find_all("div", class_="sphinx-tabs-panel")
				for label, panel in zip(labels, panels):
					self.add({"type": "heading", "text": label.replace("**", "") or "—", "level": 4})
					self.walk(panel)
			elif name == "div" and "toctree-wrapper" in cls or (name == "div" and "o_toctree_cards" in " ".join(cls)):
				self.toc_links(child)
			elif name == "a" and "o_toctree_card" in cls:
				self.toc_links(child)
			elif name == "iframe" or (name == "div" and child.find("iframe")):
				frame = child if name == "iframe" else child.find("iframe")
				src = frame.get("src") or ""
				if src.startswith("//"):
					src = "https:" + src
				if "youtube" in src or "vimeo" in src:
					self.add({"type": "video", "url": src})
			elif name in ("blockquote", "div", "span", "center", "details"):
				self.walk(child)
			elif name in ("hr", "script", "style", "button", "a", "i"):
				continue
			else:
				text = self.text_of(child)
				if text:
					self.add({"type": "paragraph", "text": text})

	def toc_links(self, node):
		lines = []
		cards = node.find_all("a", class_="o_toctree_card") if "o_toctree_card" not in (node.get("class") or []) else [node]
		if cards:
			for a in cards:
				target = self.resolve(a.get("href") or "")
				title_el = a.find(class_="card-title")
				desc_el = a.find(class_="card-text")
				title = self.text_of(title_el).replace("**", "") if title_el else self.text_of(a)
				desc = self.text_of(desc_el) if desc_el else ""
				if target:
					lines.append(f"- [[{slug_for(target)}|{title}]]" + (f" — {desc}" if desc else ""))
		else:
			lines = self.md_list(node.find("ul")).splitlines() if node.find("ul") else []
		if lines:
			self.add({"type": "markdown", "text": "\n".join(lines)})

	def convert(self):
		art = self.soup.select_one("article") or self.soup
		h1 = art.find("h1")
		if h1:
			self.title = self.text_of(h1).replace("**", "").replace("\\", "") or self.title
		self.pending_images = []
		self.walk(art)
		# merge runs of tiny blocks is not needed; drop empty ones
		self.blocks = [b for b in self.blocks if any(str(v).strip() for k, v in b.items() if k != "type")]
		merged = []
		for b in self.blocks:  # consecutive lists (e.g. one per app card) -> one list
			prev = merged[-1] if merged else None
			if (
				prev and b["type"] == prev["type"] == "markdown"
				and re.match(r"\s*(-|\d+\.) ", b["text"]) and re.match(r"\s*(-|\d+\.) ", prev["text"])
			):
				prev["text"] += "\n" + b["text"]
			else:
				merged.append(b)
		self.blocks = merged
		summary = next((b["text"] for b in self.blocks if b["type"] == "paragraph"), "")
		summary = re.sub(r"\[\[[^|\]]*\|([^\]]*)\]\]", r"\1", summary)
		summary = re.sub(r"[*`\\]", "", summary)
		return {
			"page": self.page,
			"slug": slug_for(self.page),
			"parent": parent_of(self.page, self.pages),
			"title": self.title.replace("\\", "")[:140],
			"summary": summary if len(summary) <= 300 else summary[:299].rsplit(" ", 1)[0] + "…",
			"url": self.url,
			"blocks": self.blocks,
		}


def parent_of(page, pages):
	parts = page.split("/")
	while len(parts) > 1:
		parts = parts[:-1]
		candidate = "/".join(parts)
		if candidate in pages:
			return candidate
	return None


def main():
	images = {}
	for lang in ("en", "ar"):
		files = sorted((ROOT / "html" / lang).rglob("*.json"))
		pages = {json.loads(f.read_text())["page"] for f in files}
		out = []
		for f in files:
			data = json.loads(f.read_text())
			out.append(Page(lang, data, pages, images).convert())
		(ROOT / f"pages_{lang}.json").write_text(json.dumps(out, ensure_ascii=False))
		blocks = sum(len(p["blocks"]) for p in out)
		print(lang, len(out), "pages,", blocks, "blocks")
	(ROOT / "images.json").write_text(json.dumps(images, ensure_ascii=False))
	remote = sum(1 for v in images.values() if v.startswith("http"))
	print(len(images), "images,", remote, "not found locally (will be downloaded)")


if __name__ == "__main__":
	main()
