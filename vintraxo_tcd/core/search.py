"""Text normalization for search (Arabic-aware)."""

import re

# Harakat, tanween, shadda, sukun, superscript alef, Quranic marks
_DIACRITICS = re.compile(r"[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed]")
_TATWEEL = chr(0x0640)
# Unify letter variants (code points, so the table stays readable in any editor)
_LETTER_MAP = {
	0x0623: 0x0627,  # alef with hamza above -> alef
	0x0625: 0x0627,  # alef with hamza below -> alef
	0x0622: 0x0627,  # alef with madda -> alef
	0x0671: 0x0627,  # alef wasla -> alef
	0x0649: 0x064A,  # alef maqsura -> yeh
	0x0629: 0x0647,  # teh marbuta -> heh
	0x0624: 0x0648,  # waw with hamza -> waw
	0x0626: 0x064A,  # yeh with hamza -> yeh
}
# Arabic-Indic and Extended Arabic-Indic digits -> ASCII digits
_DIGIT_MAP = {base + i: ord("0") + i for base in (0x0660, 0x06F0) for i in range(10)}
_CHAR_MAP = {**_LETTER_MAP, **_DIGIT_MAP}
_WS = re.compile(r"\s+")


def normalize_text(text: str | None) -> str:
	"""Lowercase, strip Arabic diacritics/tatweel, unify letter variants, collapse whitespace."""
	if not text:
		return ""
	text = _DIACRITICS.sub("", str(text)).replace(_TATWEEL, "")
	text = text.translate(_CHAR_MAP).lower()
	return _WS.sub(" ", text).strip()


# ---------------------------------------------------------------- ranked search

MAX_TERMS = 8
CANDIDATES = 200
SNIPPET_RADIUS = 60
RESULT_FIELDS = [
	"name",
	"title",
	"slug",
	"space",
	"content_type",
	"status",
	"language",
	"summary",
	"modified",
]


def tokenize(query: str | None) -> list[str]:
	"""Normalized, de-duplicated terms of 2+ characters (order kept)."""
	seen, terms = set(), []
	for term in normalize_text(query).split():
		if len(term) >= 2 and term not in seen:
			seen.add(term)
			terms.append(term)
	return terms[:MAX_TERMS]


def _like(term: str) -> str:
	escaped = term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
	return f"%{escaped}%"


def _score(row, terms: list[str], phrase: str) -> float:
	title = normalize_text(row.title)
	summary = normalize_text(row.summary)
	body = row.search_text or ""
	title_words = title.split()
	score = 0.0
	if title == phrase:
		score += 100
	elif phrase in title:
		score += 40
	for term in terms:
		if term in title_words:
			score += 15
		elif any(w.startswith(term) for w in title_words):
			score += 10
		elif term in title:
			score += 6
		if term in summary:
			score += 3
		score += min(body.count(term), 5) * 0.5
	if row.content_type == "Tutorial":
		score += 1
	return score


def snippet(text: str, terms: list[str]) -> str:
	"""Short excerpt of normalized text around the first matching term."""
	if not text:
		return ""
	positions = [text.find(t) for t in terms if t in text]
	if not positions:
		return text[: SNIPPET_RADIUS * 2]
	start = max(min(positions) - SNIPPET_RADIUS, 0)
	end = min(start + SNIPPET_RADIUS * 2, len(text))
	return ("..." if start else "") + text[start:end].strip() + ("..." if end < len(text) else "")


def search(query: str | None, space: str | None = None, limit: int = 20) -> list:
	"""Every term must match (AND); results ranked by where the terms match. Permission-aware."""
	import frappe

	terms = tokenize(query)
	if not terms:
		return []
	filters = [["TCD Content", "search_text", "like", _like(t)] for t in terms]
	if space:
		filters.append(["TCD Content", "space", "=", space])
	rows = frappe.get_list(
		"TCD Content",
		filters=filters,
		fields=[*RESULT_FIELDS, "search_text"],
		order_by="modified desc",
		limit_page_length=CANDIDATES,
	)
	phrase = " ".join(terms)
	for row in rows:
		row.score = _score(row, terms, phrase)
		row.snippet = snippet(row.search_text, terms)
		del row["search_text"]
	rows.sort(key=lambda r: (-r.score, -r.modified.timestamp()))
	return rows[: max(1, min(int(limit or 20), 100))]
