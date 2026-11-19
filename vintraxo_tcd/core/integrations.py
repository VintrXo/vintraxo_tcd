"""Integration layer (PLAN Phase 8, ADR-0017): connector registry, event mapping, outbox log,
signed delivery with retry/backoff and per-connector rate limits.

Events are written to an outbox (TCD Integration Event) inside the business transaction and sent
after commit by a background job; a scheduler job retries what is due. Nothing here runs user code."""

import hashlib
import hmac
import ipaddress
import json
import socket
import time
from urllib.parse import urlparse

import frappe
import requests
from frappe import _
from frappe.utils import add_to_date, get_url, now_datetime

EVENTS = {
	"Enrollment Created": "enrollment.created",
	"Enrollment Completed": "enrollment.completed",
	"Certificate Issued": "certificate.issued",
	"Certificate Revoked": "certificate.revoked",
	"Policy Activated": "policy.activated",
	"Policy Acknowledged": "policy.acknowledged",
}
BACKOFF_MINUTES = (1, 5, 15, 60, 240, 720)
KEEP_SENT_DAYS = 30


# ---------------------------------------------------------------- connector validation


def check_url(url: str, allow_private: bool = False, resolve: bool = True):
	"""Only http(s); HTTPS and public addresses unless the admin allows a private network (SSRF guard)."""
	parsed = urlparse((url or "").strip())
	if parsed.scheme not in ("http", "https") or not parsed.hostname:
		frappe.throw(_("The endpoint must be an http(s) URL."))
	if allow_private:
		return
	if parsed.scheme != "https":
		frappe.throw(_("Use HTTPS, or allow the private network for an internal service."))
	try:
		addresses = [ipaddress.ip_address(parsed.hostname)]
	except ValueError:
		if not resolve:
			addresses = []
		else:
			try:
				infos = socket.getaddrinfo(parsed.hostname, parsed.port or 443, proto=socket.IPPROTO_TCP)
			except socket.gaierror:
				frappe.throw(_("Cannot resolve the endpoint host {0}.").format(parsed.hostname))
			addresses = [ipaddress.ip_address(info[4][0]) for info in infos]
	for ip in addresses:
		if not ip.is_global:
			frappe.throw(
				_("The endpoint resolves to a private or local address. Allow the private network to use it.")
			)


def validate_connector(doc):
	doc.endpoint_url = (doc.endpoint_url or "").strip()
	# resolve on send; on save only literal addresses are checked (DNS may be unavailable here)
	check_url(doc.endpoint_url, doc.allow_private_network, resolve=False)
	seen = set()
	for row in doc.events:
		if row.event in seen:
			frappe.throw(_("Event {0} is listed twice.").format(_(row.event)))
		seen.add(row.event)
	doc.max_attempts = min(max(int(doc.max_attempts or 5), 1), len(BACKOFF_MINUTES) + 1)
	doc.timeout_seconds = min(max(int(doc.timeout_seconds or 10), 1), 30)


# ---------------------------------------------------------------- emit


def connectors_for(event: str) -> list[str]:
	enabled = frappe.get_all("TCD Connector", filters={"enabled": 1}, pluck="name")
	if not enabled:
		return []
	return frappe.get_all(
		"TCD Connector Event",
		filters={"parenttype": "TCD Connector", "parent": ("in", enabled), "event": event},
		pluck="parent",
		distinct=True,
	)


def emit(event: str, doc):
	"""Queue an event for every enabled connector that subscribes to it."""
	if event not in EVENTS or frappe.flags.in_install or frappe.flags.in_import:
		return []
	connectors = connectors_for(event)
	if not connectors:
		return []
	payload = json.dumps(serialize(event, doc), default=str, ensure_ascii=False)
	names = []
	for connector in connectors:
		row = frappe.get_doc(
			{
				"doctype": "TCD Integration Event",
				"connector": connector,
				"event": event,
				"status": "Queued",
				"attempts": 0,
				"next_attempt_on": now_datetime(),
				"reference_doctype": doc.doctype,
				"reference_name": doc.name,
				"payload": payload,
			}
		).insert(ignore_permissions=True)
		names.append(row.name)
		frappe.enqueue(
			"vintraxo_tcd.core.integrations.deliver",
			queue="short",
			event_name=row.name,
			enqueue_after_commit=True,
		)
	return names


def _employee(user: str) -> str | None:
	from vintraxo_tcd.core.training import employee_profile

	profile = employee_profile(user)
	return profile.name if profile else None


def serialize(event: str, doc) -> dict:
	get = doc.get
	if doc.doctype == "TCD Enrollment":
		return {
			"enrollment": doc.name,
			"user": get("user"),
			"employee": _employee(get("user")),
			"enrollment_for": get("enrollment_for"),
			"course": get("course"),
			"learning_path": get("learning_path"),
			"status": get("status"),
			"percent": get("percent"),
			"mandatory": get("mandatory"),
			"training_rule": get("training_rule"),
			"due_date": get("due_date"),
			"enrolled_on": get("enrolled_on"),
			"completed_on": get("completed_on"),
		}
	if doc.doctype == "TCD Certificate":
		return {
			"certificate": doc.name,
			"user": get("user"),
			"employee": _employee(get("user")),
			"title": get("title"),
			"certificate_for": get("certificate_for"),
			"course": get("course"),
			"learning_path": get("learning_path"),
			"status": get("status"),
			"issued_on": get("issued_on"),
			"expires_on": get("expires_on"),
			"revoked_reason": get("revoked_reason"),
			"verify_url": get_url(f"/verify/{get('verification_code')}"),
		}
	if doc.doctype == "TCD Governance Document":
		return {
			"document": doc.name,
			"title": get("title"),
			"doc_kind": get("doc_kind"),
			"version": get("version"),
			"effective_date": get("effective_date"),
			"url": get_url(f"/learn/policies/{doc.name}"),
		}
	if doc.doctype == "TCD Acknowledgment":
		return {
			"document": get("governance_document"),
			"version": get("version"),
			"user": get("user"),
			"employee": _employee(get("user")),
			"acknowledged_on": get("acknowledged_on"),
		}
	return {"name": doc.name}


# ---------------------------------------------------------------- deliver


def _summary(event: str, data: dict) -> str:
	subject = data.get("title") or data.get("course") or data.get("learning_path") or data.get("document")
	who = data.get("user")
	return " · ".join(str(x) for x in (_(event), subject, who) if x)


def build_request(connector, event_id: str, event: str, data: dict, created=None) -> tuple[bytes, dict]:
	code = EVENTS.get(event, event)
	if connector.payload_format == "Slack":
		envelope = {"text": _summary(event, data)}
	else:
		envelope = {
			"id": event_id,
			"event": code,
			"occurred_on": str(created or now_datetime()),
			"site": get_url(),
			"data": data,
		}
	body = json.dumps(envelope, default=str, ensure_ascii=False, separators=(",", ":")).encode()
	timestamp = str(int(time.time()))
	headers = {
		"Content-Type": "application/json",
		"User-Agent": "VintraXo-TCD",
		"X-TCD-Event": code,
		"X-TCD-Delivery": event_id,
		"X-TCD-Timestamp": timestamp,
	}
	secret = connector.get_password("secret", raise_exception=False)
	if secret:
		headers["X-TCD-Signature"] = "sha256=" + sign(secret, timestamp, body)
	return body, headers


def sign(secret: str, timestamp: str, body: bytes) -> str:
	"""HMAC-SHA256 over "<timestamp>.<body>" so receivers can reject replays."""
	return hmac.new(secret.encode(), timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()


def over_rate_limit(connector) -> bool:
	limit = int(connector.rate_limit_per_minute or 0)
	if not limit:
		return False
	sent = frappe.db.count(
		"TCD Integration Event",
		{
			"connector": connector.name,
			"status": "Sent",
			"sent_on": (">=", add_to_date(now_datetime(), seconds=-60)),
		},
	)
	return sent >= limit


def send(connector, body: bytes, headers: dict) -> requests.Response:
	check_url(connector.endpoint_url, connector.allow_private_network)
	return requests.post(
		connector.endpoint_url,
		data=body,
		headers=headers,
		timeout=int(connector.timeout_seconds or 10),
		allow_redirects=False,
	)


def deliver(event_name: str) -> str | None:
	"""Send one queued event. Returns Sent, Failed, Queued (retry later) or None."""
	status = frappe.db.get_value("TCD Integration Event", event_name, "status", for_update=True)
	if status != "Queued":
		return status
	ev = frappe.get_doc("TCD Integration Event", event_name)
	connector = frappe.get_doc("TCD Connector", ev.connector)
	if not connector.enabled or over_rate_limit(connector):
		ev.db_set("next_attempt_on", add_to_date(now_datetime(), minutes=1))
		return "Queued"

	code, error = None, None
	try:
		body, headers = build_request(
			connector, ev.name, ev.event, json.loads(ev.payload or "{}"), ev.creation
		)
		response = send(connector, body, headers)
		code = response.status_code
		if 200 <= code < 300:
			ev.db_set(
				{
					"status": "Sent",
					"sent_on": now_datetime(),
					"attempts": ev.attempts + 1,
					"response_code": code,
					"last_error": None,
				}
			)
			return "Sent"
		error = f"HTTP {code}: {response.text[:500]}"
	except frappe.ValidationError as e:  # blocked URL: retrying will not help
		ev.db_set({"status": "Failed", "attempts": ev.attempts + 1, "last_error": str(e)[:1000]})
		return "Failed"
	except Exception as e:
		error = f"{type(e).__name__}: {str(e)[:900]}"

	attempts = ev.attempts + 1
	values = {"attempts": attempts, "response_code": code or 0, "last_error": error}
	if attempts >= int(connector.max_attempts or 5):
		values["status"] = "Failed"
	else:
		minutes = BACKOFF_MINUTES[min(attempts - 1, len(BACKOFF_MINUTES) - 1)]
		values["next_attempt_on"] = add_to_date(now_datetime(), minutes=minutes)
	ev.db_set(values)
	return values.get("status", "Queued")


def retry(event_name: str):
	ev = frappe.get_doc("TCD Integration Event", event_name)
	if ev.status == "Sent":
		frappe.throw(_("This event was already sent."))
	ev.db_set({"status": "Queued", "attempts": 0, "next_attempt_on": now_datetime(), "last_error": None})
	frappe.enqueue(
		"vintraxo_tcd.core.integrations.deliver",
		queue="short",
		event_name=ev.name,
		enqueue_after_commit=True,
	)


def test_connector(name: str) -> dict:
	"""Send a signed ping now (nothing is logged in the outbox)."""
	connector = frappe.get_doc("TCD Connector", name)
	body, headers = build_request(
		connector, frappe.generate_hash(length=16), "tcd.ping", {"message": "VintraXo TCD test"}
	)
	headers["X-TCD-Event"] = "tcd.ping"
	try:
		response = send(connector, body, headers)
	except frappe.ValidationError:
		raise
	except Exception as e:
		return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}
	return {"ok": 200 <= response.status_code < 300, "status_code": response.status_code}


# ---------------------------------------------------------------- scheduler


def process_queue(limit: int = 200):
	"""Send what is due (retries, and events whose after-commit job never ran)."""
	for name in frappe.get_all(
		"TCD Integration Event",
		filters={"status": "Queued", "next_attempt_on": ("<=", now_datetime())},
		order_by="creation asc",
		pluck="name",
		limit=limit,
	):
		deliver(name)
		frappe.db.commit()  # one delivery per transaction: a crash never resends earlier ones


def purge_sent():
	frappe.db.delete(
		"TCD Integration Event",
		{"status": "Sent", "creation": ("<", add_to_date(now_datetime(), days=-KEEP_SENT_DAYS))},
	)
