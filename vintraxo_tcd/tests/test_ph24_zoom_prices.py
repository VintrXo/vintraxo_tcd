import json
from unittest.mock import MagicMock, patch

import frappe
from frappe.utils import add_to_date, now_datetime

from vintraxo_tcd import api
from vintraxo_tcd.core import meetings, payments
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course

REQ = "vintraxo_tcd.core.meetings.requests"


def ok(data=None):
	r = MagicMock()
	r.json.return_value = data or {}
	r.raise_for_status.return_value = None
	return r


class TestPhase24ZoomAndPrices(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		cls.other = make_user("tcd-other@test.local", ["TCD Learner"])

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in (
			"TCD Session",
			"TCD Session Attendance",
			"TCD Learner Profile",
			"TCD Country Price",
			*CLEAN,
		):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		frappe.db.delete("TCD Course Instructor")
		frappe.get_single("TCD Settings").update(
			{
				"enable_portal": 1,
				"meeting_provider": "Zoom",
				"zoom_account_id": "acc",
				"zoom_client_id": "cid",
				"zoom_client_secret": "sec",
				"zoom_attendance_percent": 50,
			}
		).save()
		frappe.clear_document_cache("TCD Settings", "TCD Settings")
		self.space = make_space("ph24-space").name

	def tearDown(self):
		frappe.set_user("Administrator")
		frappe.get_single("TCD Settings").update({"meeting_provider": None}).save()

	# ------------------------------------------------------------ Zoom attendance

	def ended_session(self):
		course = make_course(
			self.space, "Live course", [[lesson(self.space, "Live lesson")]], instructors=[self.vip]
		)
		for user in (self.learner, self.other, self.vip):
			frappe.set_user(user)
			api.enroll("Course", course.name)
		frappe.set_user("Administrator")
		start = add_to_date(now_datetime(), hours=-3)
		return frappe.get_doc(
			{
				"doctype": "TCD Session",
				"title": "Live",
				"course": course.name,
				"session_type": "Online",
				"conferencing": "Zoom",
				"meeting_id": "123",  # already created: no Zoom call on insert
				"starts_on": start,
				"ends_on": add_to_date(start, hours=1),
				"attendance": [{"user": self.vip, "status": "Excused"}],  # marked by hand: kept
			}
		).insert()

	def test_attendance_read_from_zoom(self):
		s = self.ended_session()
		participants = {
			"participants": [
				{"user_email": self.learner.upper(), "duration": 1200},
				{"user_email": self.learner, "duration": 900},  # rejoined: 35 min in total
				{"user_email": self.other, "duration": 300},
				{"user_email": "", "name": "Phone user", "duration": 3600},
			]
		}
		with patch(REQ) as req:
			req.post.return_value = ok({"access_token": "T"})
			req.get.return_value = ok(participants)
			self.assertEqual(meetings.take_zoom_attendance(s.name), {"present": 1, "absent": 1, "kept": 1})
			url = req.get.call_args.args[0]
			self.assertTrue(url.endswith("/past_meetings/123/participants"))
		s.reload()
		rows = {r.user: (r.status, r.note) for r in s.attendance}
		self.assertEqual(rows[self.learner][0], "Present")
		self.assertEqual(rows[self.other], ("Absent", "Zoom: 5 min"))
		self.assertEqual(rows[self.vip][0], "Excused")
		self.assertEqual((s.attendance_synced, s.status), (1, "Completed"))

		with patch(REQ) as req:  # the hourly job skips sessions already read
			meetings.sync_zoom_attendance()
			req.get.assert_not_called()

	def test_hourly_job_and_permissions(self):
		s = self.ended_session()
		with patch(REQ) as req:
			req.post.return_value = ok({"access_token": "T"})
			req.get.return_value = ok({"participants": []})
			meetings.sync_zoom_attendance()
		self.assertEqual(frappe.db.get_value("TCD Session", s.name, "attendance_synced"), 1)
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.zoom_attendance(s.name)

	# ------------------------------------------------------------ country prices

	def test_country_price(self):
		frappe.get_single("TCD Settings").update({"payment_gateway": None}).save()
		course = make_course(
			self.space,
			"Paid course",
			[[lesson(self.space, "Paid lesson")]],
			paid=1,
			price=100,
			currency="USD",
			country_prices=[{"country": "Egypt", "price": 1500, "currency": "EGP"}],
		)
		self.assertEqual(payments.price_for("TCD Course", course.name, self.learner)["price"], 100)
		frappe.set_user(self.learner)
		api.save_profile(json.dumps({"headline": "x", "country": "Egypt"}))
		q = api.price_quote("Course", course.name)
		self.assertEqual((q["price"], q["currency"], q["country"]), (1500, "EGP", "Egypt"))
		status, html, _ = render(f"/learn/{self.space}/course/{course.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("Egypt", html)
		with self.assertRaises(frappe.ValidationError):
			api.save_profile(json.dumps({"country": "Atlantis"}))

		frappe.set_user("Administrator")
		course.reload()
		course.status = "Draft"
		course.save()
		course.append("country_prices", {"country": "Egypt", "price": 1, "currency": "EGP"})
		with self.assertRaises(frappe.ValidationError):  # listed twice
			course.save()
