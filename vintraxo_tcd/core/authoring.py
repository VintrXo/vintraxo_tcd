"""Course source files -> TCD blocks and questions (Phase 30, ADR-0038).

A course is written as plain text, one file per language (`library/<course>/<lang>.md`). Lessons are separated by
`# @lesson <slug>` lines, followed by `key: value` header lines (title, summary, type) and a `---` line. The body is
Markdown with a few fenced extras:

    ```html                      code block (any language)
    ```try html                  "try it yourself" playground (python, sql, html, javascript, ...)
    ```try sql shop              ... with the hidden setup code "shop" from course.json ("setups")
    ```exercise html             practice: first line "? prompt", code with ___ blanks, then "= answer" lines,
                                 optional "! hint"
    ```reference html            reference table, one "name | description | example" per line
    ```quiz                      questions (see parse_quiz)
    :::tip Title                 callout (info, tip, warning, danger) until a line ":::"

Headings (`##`, `###`), paragraphs, lists and tables become heading / paragraph / markdown blocks. Pure functions:
no database access, so the parser is easy to test and to run anywhere."""

import re

LESSON = re.compile(r"^# @lesson\s+(\S+)\s*$", re.M)
FENCE = re.compile(r"^```(\S*)(?:[ \t]+(\S+))?(?:[ \t]+(\S+))?[ \t]*$")
CALLOUT = re.compile(r"^:::(info|tip|warning|danger)(?:[ \t]+(.*))?$")
HEADING = re.compile(r"^(#{2,4})\s+(.*)$")


class SourceError(ValueError):
	pass


def split_lessons(text: str) -> list[dict]:
	"""-> [{slug, title, summary, type, body}] in file order."""
	parts = LESSON.split(text)
	lessons = []
	for i in range(1, len(parts), 2):
		slug, rest = parts[i], parts[i + 1]
		head, sep, body = rest.partition("\n---\n")
		if not sep:
			raise SourceError(f"lesson {slug}: header must end with a '---' line")
		meta = {}
		for line in head.strip().splitlines():
			key, _, value = line.partition(":")
			meta[key.strip()] = value.strip()
		if not meta.get("title"):
			raise SourceError(f"lesson {slug}: title is missing")
		lessons.append(
			{
				"slug": slug,
				"title": meta["title"],
				"summary": meta.get("summary", ""),
				"type": meta.get("type", "Lesson"),
				"body": body.strip("\n"),
			}
		)
	return lessons


def to_blocks(body: str, setups: dict | None = None) -> tuple[list, list]:
	"""Markdown-ish body -> (blocks, quiz questions). `setups`: named hidden code for ```try <lang> <setup>."""
	blocks, questions = [], []
	lines = body.splitlines()
	para: list[str] = []
	i = 0

	def flush():
		text = "\n".join(para).strip()
		para.clear()
		if not text:
			return
		is_md = any(re.match(r"\s*([-*]|\d+\.)\s|\s*\|", line) for line in text.splitlines())
		blocks.append({"type": "markdown" if is_md else "paragraph", "text": text})

	while i < len(lines):
		line = lines[i]
		fence = FENCE.match(line)
		callout = CALLOUT.match(line)
		heading = HEADING.match(line)
		if fence:
			flush()
			kind, arg, extra = fence.group(1), fence.group(2) or "", fence.group(3) or ""
			inner, i = _until(lines, i + 1, "```")
			blocks_or_q = _fenced(kind, arg, inner)
			if extra and kind == "try":
				if extra not in (setups or {}):
					raise SourceError(f"try block uses setup '{extra}', which course.json does not define")
				blocks_or_q["setup"] = setups[extra]
			if kind == "quiz":
				questions.extend(blocks_or_q)
			else:
				blocks.append(blocks_or_q)
			continue
		if callout:
			flush()
			inner, i = _until(lines, i + 1, ":::")
			block = {"type": "callout", "variant": callout.group(1), "text": "\n".join(inner).strip()}
			if callout.group(2):
				block["title"] = callout.group(2).strip()
			blocks.append(block)
			continue
		if heading:
			flush()
			blocks.append(
				{"type": "heading", "text": heading.group(2).strip(), "level": len(heading.group(1))}
			)
		elif not line.strip():
			flush()
		else:
			para.append(line)
		i += 1
	flush()
	return blocks, questions


def _until(lines, start, end):
	out = []
	i = start
	while i < len(lines):
		if lines[i].strip() == end:
			return out, i + 1
		out.append(lines[i])
		i += 1
	raise SourceError(f"block starting near line {start} is not closed with {end}")


def _fenced(kind: str, arg: str, inner: list[str]):
	code = "\n".join(inner)
	if kind == "try":
		return {"type": "playground", "language": arg, "code": code}
	if kind == "exercise":
		prompt = next((ln[1:].strip() for ln in inner if ln.startswith("? ")), "")
		answers = [ln[1:].strip() for ln in inner if ln.startswith("= ")]
		hint = next((ln[1:].strip() for ln in inner if ln.startswith("! ")), "")
		body = "\n".join(ln for ln in inner if not ln.startswith(("? ", "= ", "! ")))
		if not prompt or not answers:
			raise SourceError("exercise needs a '? prompt' line and '= answer' lines")
		block = {"type": "exercise", "prompt": prompt, "code": body.strip("\n"), "answers": answers}
		if arg:
			block["language"] = arg
		if hint:
			block["hint"] = hint
		return block
	if kind == "reference":
		block = {"type": "reference", "entries": [ln for ln in inner if ln.strip()]}
		if arg:
			block["language"] = arg
		return block
	if kind == "quiz":
		return parse_quiz(inner)
	block = {"type": "code", "code": code}
	if kind:
		block["language"] = kind
	return block


def parse_quiz(lines: list[str]) -> list[dict]:
	"""Questions separated by blank lines:

	    ? Question text
	    - wrong option
	    * right option                  (one * = single choice, several = multiple choice)
	    = true                          (true / false question: "= true" or "= false")
	    > explanation shown after submitting

	Quiz questions are choice questions (TCD Quiz Question); blanks belong in ```exercise blocks.
	"""
	questions, cur = [], None

	def close():
		if not cur:
			return
		q, options, right, equals = cur["q"], cur["options"], cur["right"], cur["equals"]
		row = {"question": q, "points": 1}
		if options:
			if not right:
				raise SourceError(f"question '{q}': mark the right option with *")
			row.update(
				question_type="Single Choice" if len(right) == 1 else "Multiple Choice",
				options="\n".join(options),
				correct_answers=",".join(str(n) for n in right),
			)
		elif equals and equals[0].lower() in ("true", "false", "صح", "خطأ"):
			row.update(
				question_type="True False",
				correct_answers="1" if equals[0].lower() in ("true", "صح") else "2",
			)
		else:
			raise SourceError(f"question '{q}': add options (- / *) or '= true' / '= false'")
		if cur["why"]:
			row["explanation"] = " ".join(cur["why"])
		questions.append(row)

	for raw in [*lines, ""]:
		line = raw.strip()
		if line.startswith("? "):
			close()
			cur = {"q": line[2:].strip(), "options": [], "right": [], "equals": [], "why": []}
		elif not cur:
			continue
		elif line.startswith(("- ", "* ")):
			cur["options"].append(line[2:].strip())
			if line.startswith("* "):
				cur["right"].append(len(cur["options"]))
		elif line.startswith("= "):
			cur["equals"].extend(a.strip() for a in line[2:].split("|") if a.strip())
		elif line.startswith("> "):
			cur["why"].append(line[2:].strip())
		elif not line:
			close()
			cur = None
	return questions
