"""Media blocks and upload validation (ADR-0009)."""

import os
import re
from urllib.parse import parse_qs, urlparse

import frappe
from frappe import _

DEFAULT_VIDEO_HOSTS = ("youtube.com", "youtu.be", "vimeo.com")
DEFAULT_EXTENSIONS = "pdf,docx,xlsx,pptx,zip,png,jpg,jpeg,txt,csv,mp4,webm"
YOUTUBE_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
VIDEO_FILE_EXT = (".mp4", ".webm")


def _settings():
	return frappe.get_cached_doc("TCD Settings")


def video_hosts() -> list[str]:
	raw = _settings().video_domains
	hosts = [h.strip().lower() for h in (raw or "").splitlines() if h.strip()]
	return hosts or list(DEFAULT_VIDEO_HOSTS)


def allowed_extensions() -> set[str]:
	raw = _settings().allowed_file_extensions or DEFAULT_EXTENSIONS
	return {e.strip().lower().lstrip(".") for e in raw.split(",") if e.strip()}


def max_upload_bytes() -> int:
	return int(_settings().max_upload_mb or 10) * 1024 * 1024


def _host_allowed(host: str) -> bool:
	host = host.lower()
	return any(host == h or host.endswith("." + h) for h in video_hosts())


def parse_video(url: str) -> tuple[str, str]:
	"""Return (provider, embed_url) for an allowed video URL, or throw."""
	url = (url or "").strip()
	if url.startswith("/files/"):
		if not url.lower().endswith(VIDEO_FILE_EXT):
			frappe.throw(_("Uploaded videos must be mp4 or webm."))
		validate_file_url(url, public_only=True)
		return "file", url
	parsed = urlparse(url)
	if parsed.scheme != "https" or not parsed.hostname:
		frappe.throw(_("Video URL must start with https:// or be an uploaded file."))
	host = parsed.hostname.lower()
	if not _host_allowed(host):
		frappe.throw(_("Video host {0} is not allowed. See TCD Settings.").format(frappe.bold(host)))

	video_id = None
	if host == "youtu.be":
		video_id = parsed.path.lstrip("/").split("/")[0]
	elif host.endswith("youtube.com") or host.endswith("youtube-nocookie.com"):
		if parsed.path == "/watch":
			video_id = (parse_qs(parsed.query).get("v") or [""])[0]
		else:
			parts = [p for p in parsed.path.split("/") if p]
			if len(parts) >= 2 and parts[0] in ("embed", "shorts", "live"):
				video_id = parts[1]
	if video_id is not None:
		if not YOUTUBE_ID.match(video_id):
			frappe.throw(_("Could not read the YouTube video id."))
		return "youtube", f"https://www.youtube-nocookie.com/embed/{video_id}"

	if host.endswith("vimeo.com"):
		digits = [p for p in parsed.path.split("/") if p.isdigit()]
		if not digits:
			frappe.throw(_("Could not read the Vimeo video id."))
		return "vimeo", f"https://player.vimeo.com/video/{digits[-1]}"

	frappe.throw(_("Only YouTube, Vimeo or uploaded videos are supported."))


def validate_link(url: str):
	parsed = urlparse((url or "").strip())
	if parsed.scheme != "https" or not parsed.hostname:
		frappe.throw(_("External links must start with https://"))


def validate_file_url(url: str, public_only: bool = False, owner: str | None = None) -> dict:
	"""The URL must belong to an existing File with an allowed extension and size."""
	url = (url or "").strip()
	if public_only and not url.startswith("/files/"):
		frappe.throw(_("Use a public uploaded file (/files/...)."))
	if not (url.startswith("/files/") or url.startswith("/private/files/")):
		frappe.throw(_("Files must be uploaded first."))
	file = frappe.db.get_value(
		"File", {"file_url": url}, ["name", "file_size", "owner", "is_private", "file_name"], as_dict=True
	)
	if not file:
		frappe.throw(_("Uploaded file not found: {0}").format(frappe.bold(url)))
	ext = os.path.splitext(file.file_name or url)[1].lower().lstrip(".")
	if ext not in allowed_extensions():
		frappe.throw(_("File type .{0} is not allowed.").format(ext))
	if (file.file_size or 0) > max_upload_bytes():
		frappe.throw(_("File is larger than {0} MB.").format(_settings().max_upload_mb or 10))
	if owner and file.owner != owner:
		frappe.throw(_("You can only submit files you uploaded."))
	return file
