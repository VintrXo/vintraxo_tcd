"""Online meetings for sessions (Phase 16, ADR-0024): Zoom (Server-to-Server OAuth) or Google Meet
(through Frappe's Google Calendar integration). A failure never blocks saving the session: the
instructor can still paste a link."""

import frappe
import requests
from frappe import _
from frappe.utils import get_datetime

ZOOM_TOKEN_URL = "https://zoom.us/oauth/token"
ZOOM_API = "https://api.zoom.us/v2"


def settings():
	return frappe.get_cached_doc("TCD Settings")


# ---------------------------------------------------------------- Zoom


def _zoom_token(s) -> str:
	secret = (
		s.get_password("zoom_client_secret", raise_exception=False) if s.get("zoom_client_secret") else None
	)
	if not (s.get("zoom_account_id") and s.get("zoom_client_id") and secret):
		frappe.throw(_("Zoom is not configured in Learning Settings."))
	r = requests.post(
		ZOOM_TOKEN_URL,
		params={"grant_type": "account_credentials", "account_id": s.zoom_account_id},
		auth=(s.zoom_client_id, secret),
		timeout=15,
	)
	r.raise_for_status()
	return r.json()["access_token"]


def _zoom_body(doc) -> dict:
	start, end = get_datetime(doc.starts_on), get_datetime(doc.ends_on)
	return {
		"topic": doc.title[:200],
		"type": 2,  # scheduled meeting
		"start_time": start.strftime("%Y-%m-%dT%H:%M:%S"),
		"timezone": frappe.utils.get_system_timezone(),
		"duration": max(int((end - start).total_seconds() // 60), 1),
		"agenda": (doc.description or "")[:2000],
		"settings": {"join_before_host": False, "waiting_room": True},
	}


def zoom_create(doc):
	s = settings()
	headers = {"Authorization": f"Bearer {_zoom_token(s)}"}
	r = requests.post(f"{ZOOM_API}/users/me/meetings", json=_zoom_body(doc), headers=headers, timeout=15)
	r.raise_for_status()
	data = r.json()
	return {"meeting_id": str(data["id"]), "meeting_url": data["join_url"], "host_url": data.get("start_url")}


def zoom_update(doc):
	s = settings()
	headers = {"Authorization": f"Bearer {_zoom_token(s)}"}
	requests.patch(
		f"{ZOOM_API}/meetings/{doc.meeting_id}", json=_zoom_body(doc), headers=headers, timeout=15
	).raise_for_status()


def zoom_delete(doc):
	s = settings()
	headers = {"Authorization": f"Bearer {_zoom_token(s)}"}
	requests.delete(f"{ZOOM_API}/meetings/{doc.meeting_id}", headers=headers, timeout=15)


# ---------------------------------------------------------------- Google Meet


def meet_create(doc):
	s = settings()
	if not s.get("google_calendar"):
		frappe.throw(_("Choose the Google Calendar in Learning Settings."))
	return {
		"calendar_event": _new_event(
			{
				"doctype": "Event",
				"subject": doc.title,
				"event_type": "Private",
				"starts_on": doc.starts_on,
				"ends_on": doc.ends_on,
				"description": doc.description,
				"sync_with_google_calendar": 1,
				"google_calendar": s.google_calendar,
				"add_video_conferencing": 1,
				"reference_doctype": "TCD Session",
				"reference_docname": doc.name,
			}
		)
	}


def _new_event(values: dict) -> str:
	return frappe.get_doc(values).insert(ignore_permissions=True).name


def meet_link(doc) -> str | None:
	"""The Meet link appears on the Event after Google syncs it."""
	if doc.get("meeting_url") or not doc.get("calendar_event"):
		return doc.get("meeting_url")
	return frappe.db.get_value("Event", doc.calendar_event, "google_meet_link")


# ---------------------------------------------------------------- session hooks


def sync(doc):
	"""Called from TCD Session.on_update: create / move / cancel the meeting."""
	if doc.session_type != "Online" or not doc.get("conferencing"):
		return
	before = doc.get_doc_before_save()
	try:
		if doc.status == "Cancelled":
			if before and before.status != "Cancelled":
				if doc.conferencing == "Zoom" and doc.meeting_id:
					zoom_delete(doc)
				elif doc.conferencing == "Google Meet" and doc.calendar_event:
					frappe.db.set_value("Event", doc.calendar_event, "status", "Cancelled")
			return
		if not (doc.meeting_id or doc.calendar_event):
			values = zoom_create(doc) if doc.conferencing == "Zoom" else meet_create(doc)
			doc.db_set(values, update_modified=False)
			return
		moved = before and (
			get_datetime(before.starts_on) != get_datetime(doc.starts_on)
			or get_datetime(before.ends_on) != get_datetime(doc.ends_on)
		)
		if moved and doc.conferencing == "Zoom":
			zoom_update(doc)
		elif moved and doc.calendar_event:
			frappe.db.set_value(
				"Event", doc.calendar_event, {"starts_on": doc.starts_on, "ends_on": doc.ends_on}
			)
	except Exception:
		frappe.log_error(title=f"TCD: meeting for session {doc.name}")
		frappe.msgprint(
			_("The meeting could not be created or updated. You can paste a meeting link instead."),
			indicator="orange",
			alert=True,
		)


def fill_meet_links():
	"""Hourly: copy Meet links that Google added to the calendar events."""
	for row in frappe.get_all(
		"TCD Session",
		filters={
			"conferencing": "Google Meet",
			"meeting_url": ("is", "not set"),
			"calendar_event": ("is", "set"),
		},
		fields=["name", "calendar_event"],
	):
		link = frappe.db.get_value("Event", row.calendar_event, "google_meet_link")
		if link:
			frappe.db.set_value("TCD Session", row.name, "meeting_url", link, update_modified=False)
