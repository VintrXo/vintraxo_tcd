"""Paid courses and paths, coupons and checkout (Phase 16, ADR-0024).

Checkout goes through the Frappe Payments app (when installed): a TCD Payment is the reference document
and the gateway calls its `on_payment_authorized` after a successful payment, which enrolls the learner.
Admin enrollment (batches, training rules) never asks for payment."""

import frappe
from frappe import _
from frappe.utils import flt, getdate, now_datetime, nowdate

from vintraxo_tcd.core import courses

OFFERING = {"Course": ("TCD Course", "course"), "Learning Path": ("TCD Learning Path", "learning_path")}


def payments_available() -> bool:
	return bool(frappe.db.exists("DocType", "Payment Gateway"))


def is_paid(enrollment_for: str, name: str) -> bool:
	doctype = OFFERING[enrollment_for][0]
	return bool(frappe.db.get_value(doctype, name, "paid"))


# ---------------------------------------------------------------- coupons


def validate_coupon_doc(doc):
	doc.code = (doc.code or "").strip().upper()
	if doc.discount_type == "Percentage" and not 0 < flt(doc.discount_value) <= 100:
		frappe.throw(_("A percentage discount must be between 1 and 100."))
	if doc.discount_type == "Amount" and flt(doc.discount_value) <= 0:
		frappe.throw(_("The discount must be more than zero."))
	if doc.valid_from and doc.valid_until and getdate(doc.valid_until) < getdate(doc.valid_from):
		frappe.throw(_("Valid Until must be after Valid From."))


def coupon_discount(
	code: str | None, enrollment_for: str, name: str, price: float
) -> tuple[str | None, float]:
	if not code:
		return None, 0.0
	code = code.strip().upper()
	c = frappe.db.get_value(
		"TCD Coupon",
		code,
		[
			"name",
			"enabled",
			"discount_type",
			"discount_value",
			"valid_from",
			"valid_until",
			"max_uses",
			"used",
		],
		as_dict=True,
	)
	today = getdate(nowdate())
	if (
		not c
		or not c.enabled
		or (c.valid_from and getdate(c.valid_from) > today)
		or (c.valid_until and getdate(c.valid_until) < today)
		or (c.max_uses and int(c.used or 0) >= int(c.max_uses))
	):
		frappe.throw(_("This coupon is not valid."))
	field = OFFERING[enrollment_for][1]
	items = frappe.get_all("TCD Coupon Item", filters={"parent": c.name}, fields=["course", "learning_path"])
	if items and not any(i.get(field) == name for i in items):
		frappe.throw(_("This coupon does not apply here."))
	off = price * flt(c.discount_value) / 100 if c.discount_type == "Percentage" else flt(c.discount_value)
	return c.name, round(min(off, price), 2)


def learner_country(user: str | None) -> str | None:
	if not user or user == "Guest":
		return None
	return frappe.db.get_value("TCD Learner Profile", user, "country")


def price_for(doctype: str, name: str, user: str | None = None) -> dict:
	"""The price a learner pays: the row for the country in their profile, else the default price."""
	o = frappe.db.get_value(doctype, name, ["paid", "price", "currency"], as_dict=True)
	out = {"price": flt(o.price) if o.paid else 0.0, "currency": o.currency, "country": None}
	country = learner_country(user)
	if o.paid and country:
		row = frappe.db.get_value(
			"TCD Country Price",
			{"parent": name, "parenttype": doctype, "country": country},
			["price", "currency"],
			as_dict=True,
		)
		if row:
			out = {"price": flt(row.price), "currency": row.currency, "country": country}
	return out


def quote(enrollment_for: str, name: str, coupon: str | None = None, user: str | None = None) -> dict:
	doctype = OFFERING[enrollment_for][0]
	o = frappe.db.get_value(doctype, name, ["title", "paid"], as_dict=True)
	p = price_for(doctype, name, user or frappe.session.user)
	price = p["price"] if o.paid else 0.0
	coupon_name, discount = coupon_discount(coupon, enrollment_for, name, price) if price else (None, 0.0)
	return {
		"title": o.title,
		"currency": p["currency"],
		"country": p["country"],
		"price": price,
		"discount": discount,
		"total": round(price - discount, 2),
		"coupon": coupon_name,
	}


# ---------------------------------------------------------------- checkout


def _controller(gateway: str):
	from payments.utils import get_payment_gateway_controller

	return get_payment_gateway_controller(gateway)


def checkout(
	enrollment_for: str, name: str, user: str, coupon: str | None = None, redirect_to: str = "/learn/my"
) -> dict:
	if user == "Guest":
		raise frappe.PermissionError
	if enrollment_for not in OFFERING:
		frappe.throw(_("Invalid enrollment type."))
	doctype, field = OFFERING[enrollment_for]
	doc = frappe.get_doc(doctype, name)
	doc.check_permission("read")
	if doc.status != "Published":
		frappe.throw(_("You can only buy published courses and learning paths."))
	if not doc.get("paid"):
		frappe.throw(_("This is free. Enroll directly."))
	if frappe.db.exists("TCD Enrollment", {"user": user, field: name, "status": ("!=", "Withdrawn")}):
		return {"enrolled": True, "url": redirect_to}
	if doctype == "TCD Course":
		from vintraxo_tcd.core import connect

		unmet = connect.unmet_course_prerequisites(user, name)
		if unmet:
			frappe.throw(_("Complete these courses first: {0}").format(", ".join(unmet)))
	q = quote(enrollment_for, name, coupon, user)
	gateway = frappe.db.get_single_value("TCD Settings", "payment_gateway")
	if q["total"] > 0 and not (payments_available() and gateway):
		frappe.throw(_("Online payment is not set up yet. Ask your administrator."))
	controller = _controller(gateway) if q["total"] > 0 else None  # fail before writing anything
	payment = frappe.get_doc(
		{
			"doctype": "TCD Payment",
			"user": user,
			"enrollment_for": enrollment_for,
			field: name,
			"status": "Pending",
			"currency": q["currency"],
			"original_amount": q["price"],
			"discount_amount": q["discount"],
			"amount": q["total"],
			"coupon": q["coupon"],
			"payment_gateway": gateway if q["total"] > 0 else None,
		}
	)
	payment.flags.from_service = True
	payment.insert(ignore_permissions=True)
	if q["total"] <= 0:
		complete(payment.name, "Free")
		return {"enrolled": True, "url": redirect_to}
	url = controller.get_payment_url(
		amount=q["total"],
		title=q["title"],
		description=_("Payment for {0}").format(q["title"]),
		reference_doctype="TCD Payment",
		reference_docname=payment.name,
		payer_email=user,
		payer_name=frappe.db.get_value("User", user, "full_name") or user,
		currency=q["currency"],
		payment_gateway=gateway,
		redirect_to=redirect_to,
	)
	return {"enrolled": False, "url": url, "payment": payment.name}


def complete(payment_name: str, status: str = "Paid") -> str | None:
	"""Mark a payment done and enroll the learner (once)."""
	p = frappe.get_doc("TCD Payment", payment_name)
	if p.status in ("Paid", "Free"):
		return None
	p.db_set({"status": status, "paid_on": now_datetime()})
	if p.coupon:
		frappe.db.set_value(
			"TCD Coupon", p.coupon, "used", int(frappe.db.get_value("TCD Coupon", p.coupon, "used") or 0) + 1
		)
	target = p.course or p.learning_path
	courses.enroll(p.user, p.enrollment_for, target)
	from vintraxo_tcd.core import notify

	title = frappe.db.get_value(OFFERING[p.enrollment_for][0], target, "title")
	notify._send(
		[p.user], _("Payment received: you are enrolled in {0}").format(title), "TCD Payment", p.name
	)
	return p.name


def on_payment_authorized(doc, status: str):
	"""Called by the Payments app gateway controller on the reference document."""
	if status in ("Completed", "Authorized"):
		complete(doc.name, "Paid")
	elif status in ("Failed", "Cancelled"):
		if doc.status == "Pending":
			doc.db_set("status", "Failed")


def validate_country_prices(doc):
	seen = set()
	for row in doc.get("country_prices") or []:
		if row.country in seen:
			frappe.throw(_("Row {0}: {1} is listed twice.").format(row.idx, frappe.bold(row.country)))
		seen.add(row.country)
		if flt(row.price) < 0:
			frappe.throw(_("Row {0}: the price cannot be negative.").format(row.idx))
