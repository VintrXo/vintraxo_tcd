from unittest.mock import MagicMock, patch

import frappe
from frappe.utils import add_to_date, now_datetime

from vintraxo_tcd import api
from vintraxo_tcd.core import meetings, sessions
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_space, make_user
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, lesson, make_course

REQ = "vintraxo_tcd.core.meetings.requests"


def ok(data=None):
	r = MagicMock()
	r.json.return_value = data or {}
	r.raise_for_status.return_value = None
	return r


class TestPhase16Meetings(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Session", "TCD Session Attendance", *CLEAN):
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
			}
		).save()
		frappe.clear_document_cache("TCD Settings", "TCD Settings")
		self.space = make_space("ph16m-space").name
		self.course = make_course(
			self.space, "Live course", [[lesson(self.space, "Live lesson")]], instructors=[self.vip]
		)
		frappe.set_user(self.learner)
		api.enroll("Course", self.course.name)
		frappe.set_user("Administrator")

	def tearDown(self):
		frappe.set_user("Administrator")
		frappe.get_single("TCD Settings").update({"meeting_provider": None}).save()

	def session(self, **kw):
		start = add_to_date(now_datetime(), hours=24)
		return frappe.get_doc(
			{
				"doctype": "TCD Session",
				"title": "Live",
				"course": self.course.name,
				"session_type": "Online",
				"starts_on": start,
				"ends_on": add_to_date(start, hours=1),
				**kw,
			}
		).insert()

	def test_zoom_create_move_cancel(self):
		with patch(REQ) as req:
			req.post.side_effect = [
				ok({"access_token": "T"}),
				ok({"id": 123, "join_url": "https://zoom.us/j/123", "start_url": "https://zoom.us/s/123"}),
			]
			s = self.session()
		s.reload()
		self.assertEqual(
			(s.conferencing, s.meeting_id, s.meeting_url), ("Zoom", "123", "https://zoom.us/j/123")
		)
		token_call, create_call = req.post.call_args_list
		self.assertEqual(token_call.kwargs["auth"], ("cid", "sec"))
		self.assertEqual(token_call.kwargs["params"]["grant_type"], "account_credentials")
		self.assertEqual(create_call.kwargs["headers"]["Authorization"], "Bearer T")
		self.assertEqual(create_call.kwargs["json"]["duration"], 60)

		frappe.set_user(self.learner)
		row = sessions.for_course(self.course.name, self.learner)["upcoming"][0]
		self.assertEqual(row["meeting_url"], "https://zoom.us/j/123")
		self.assertNotIn("host_url", row)  # the host link is for the instructor only
		frappe.set_user("Administrator")

		with patch(REQ) as req:
			req.post.return_value = ok({"access_token": "T"})
			s.starts_on = add_to_date(s.starts_on, hours=1)
			s.ends_on = add_to_date(s.ends_on, hours=1)
			s.save()
			self.assertTrue(req.patch.called)
			s.status = "Cancelled"
			s.save()
			self.assertIn("/meetings/123", req.delete.call_args.args[0])

	def test_failure_does_not_block_and_manual_link(self):
		with patch(REQ) as req:
			req.post.side_effect = Exception("zoom down")
			s = self.session()
		s.reload()
		self.assertFalse(s.meeting_id)
		self.assertTrue(frappe.get_all("Error Log", filters={"method": ("like", "%meeting for session%")}))
		manual = self.session(conferencing="", meeting_url="https://meet.example.com/abc")
		self.assertEqual(manual.meeting_url, "https://meet.example.com/abc")

	def test_google_meet_through_calendar_event(self):
		frappe.get_single("TCD Settings").update({"meeting_provider": "Google Meet"}).save()
		frappe.clear_document_cache("TCD Settings", "TCD Settings")
		created = []
		with (
			patch.object(meetings, "settings", return_value=frappe._dict(google_calendar="Team Calendar")),
			patch.object(meetings, "_new_event", side_effect=lambda v: created.append(v) or "EV-1"),
		):
			s = self.session()
		s.reload()
		self.assertEqual((s.conferencing, s.calendar_event), ("Google Meet", "EV-1"))
		self.assertEqual(
			(created[0]["add_video_conferencing"], created[0]["google_calendar"]), (1, "Team Calendar")
		)
		self.assertEqual(created[0]["reference_docname"], s.name)

		event = frappe.get_doc(
			{
				"doctype": "Event",
				"subject": "Live",
				"event_type": "Private",
				"starts_on": s.starts_on,
				"google_meet_link": "https://meet.google.com/x",
			}
		).insert(ignore_permissions=True)
		frappe.db.set_value("TCD Session", s.name, "calendar_event", event.name)
		s.reload()
		self.assertEqual(meetings.meet_link(s), "https://meet.google.com/x")
		meetings.fill_meet_links()
		self.assertEqual(
			frappe.db.get_value("TCD Session", s.name, "meeting_url"), "https://meet.google.com/x"
		)
