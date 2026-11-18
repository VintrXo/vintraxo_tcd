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
