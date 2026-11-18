import json

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, now_datetime

from vintraxo_tcd import api
from vintraxo_tcd.core import permissions
from vintraxo_tcd.core.dashboards import instructor_dashboard, my_learning
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user, publish
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, enrollment, lesson, make_course
from vintraxo_tcd.vintraxo_tcd.report.tcd_instructor_dashboard import tcd_instructor_dashboard as report


def blocks(*items):
	return json.dumps(list(items))


def make_file(name, content=b"data", private=1, user=None):
	if user:
		frappe.set_user(user)
	doc = frappe.get_doc(
		{"doctype": "File", "file_name": name, "content": content, "is_private": private}
	).insert(ignore_permissions=True)
	frappe.set_user("Administrator")
	return doc


class TestPhase1LMS(IntegrationTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		settings = frappe.get_single("TCD Settings")
		settings.update(
			{
				"require_approval_before_publish": 1,
				"enable_portal": 1,
				"video_domains": "youtube.com\nyoutu.be\nvimeo.com",
				"allowed_file_extensions": "pdf,txt,mp4",
				"max_upload_mb": 1,
			}
		)
		settings.save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Course Feedback", "TCD Assignment Submission", "TCD Assignment", *CLEAN):
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		frappe.db.delete("TCD Course Instructor")
		frappe.db.delete("TCD Batch Member")
		frappe.clear_document_cache("TCD Settings", "TCD Settings")
		self.space = make_space("ph1b-public").name
		self.l1 = lesson(self.space, "Lesson One")
		self.l2 = lesson(self.space, "Lesson Two")

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ batch rename

	def test_batch(self):
		self.assertTrue(frappe.db.exists("DocType", "TCD Batch"))
		self.assertFalse(frappe.db.exists("DocType", "TCD Student Group"))
		self.assertTrue(frappe.get_meta("TCD Enrollment").get_field("batch"))
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "TCD Batch",
					"group_name": "bad-dates",
					"start_date": "2030-02-01",
					"end_date": "2030-01-01",
				}
			).insert()
		for reserved in ("my", "instructor"):
			with self.assertRaises(frappe.ValidationError):
				make_space(reserved)

	# ------------------------------------------------------------ enrolled-only access

	def test_enrolled_only_course(self):
		shared = self.l2
		course = make_course(self.space, "Closed course", [[self.l1, shared]], access="Enrolled Only")
		make_course(self.space, "Open course", [[shared]])
		frappe.set_user(self.learner)
		self.assertFalse(frappe.has_permission("TCD Content", "read", self.l1.name))
		self.assertTrue(frappe.has_permission("TCD Content", "read", shared.name))  # also in an Open course
		self.assertNotIn(self.l1.name, frappe.get_list("TCD Content", pluck="name"))
		self.assertFalse(any(r.name == self.l1.name for r in api.search_content("Lesson One")))
		self.assertTrue(frappe.has_permission("TCD Course", "read", course.name))  # outline stays visible

		api.enroll("Course", course.name)
		self.assertTrue(frappe.has_permission("TCD Content", "read", self.l1.name))
		self.assertIn(self.l1.name, frappe.get_list("TCD Content", pluck="name"))

		frappe.set_user(self.reviewer)  # staff are not gated
		self.assertTrue(frappe.has_permission("TCD Content", "read", self.l1.name))

	# ------------------------------------------------------------ lesson types and media blocks

	def test_lesson_type_and_media_blocks(self):
		article = make_content(self.space, "Article", lesson_type="Video")
		self.assertIsNone(article.lesson_type)  # only lessons keep a lesson type

		doc = make_content(
			self.space,
			"Media",
			content_type="Lesson",
			lesson_type="Video",
			blocks=blocks(
				{"type": "video", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "title": "YT"},
				{"type": "video", "url": "https://youtu.be/dQw4w9WgXcQ"},
				{"type": "video", "url": "https://vimeo.com/76979871"},
				{"type": "link", "url": "https://example.com/docs", "title": "Docs"},
			),
		)
		b = json.loads(doc.blocks)
		self.assertEqual(b[0]["embed_url"], "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ")
		self.assertEqual(b[1]["provider"], "youtube")
		self.assertEqual(b[2]["embed_url"], "https://player.vimeo.com/video/76979871")
		self.assertEqual(doc.lesson_type, "Video")

		bad = [
			{"type": "video", "url": "https://evil.example/video"},
			{"type": "video", "url": "http://www.youtube.com/watch?v=dQw4w9WgXcQ"},
			{"type": "video", "url": "https://www.youtube.com/watch?v=<script>"},
			{"type": "video", "url": "/files/missing.mp4"},
			{"type": "link", "url": "javascript:alert(1)", "title": "x"},
			{"type": "link", "url": "http://plain.example", "title": "x"},
			{"type": "file", "url": "/files/missing.pdf", "title": "x"},
		]
		for block in bad:
			with self.assertRaises(frappe.ValidationError, msg=block):
				make_content(self.space, "Bad media", blocks=blocks(block))

		public_pdf = make_file("guide.txt", b"guide", private=0)
		private_pdf = make_file("secret.txt", b"secret", private=1)
		exe = make_file("tool.exe", b"MZ", private=0)
		make_content(
			self.space,
			"With file",
			blocks=blocks({"type": "file", "url": public_pdf.file_url, "title": "Guide"}),
		)
		for f in (private_pdf, exe):
			with self.assertRaises(frappe.ValidationError, msg=f.file_url):
				make_content(
					self.space, "Bad file", blocks=blocks({"type": "file", "url": f.file_url, "title": "x"})
				)

		settings = frappe.get_single("TCD Settings")
		settings.video_domains = "vimeo.com"
		settings.save()
		frappe.clear_document_cache("TCD Settings", "TCD Settings")
		try:
			with self.assertRaises(frappe.ValidationError):
				make_content(
					self.space,
					"No yt",
					blocks=blocks({"type": "video", "url": "https://youtu.be/dQw4w9WgXcQ"}),
				)
		finally:
			settings.video_domains = "youtube.com\nyoutu.be\nvimeo.com"
			settings.save()

	def test_media_rendering_is_safe(self):
		doc = publish(
			make_content(
				self.space,
				"Render media",
				content_type="Lesson",
				visibility="Public",
				blocks=blocks(
					{"type": "video", "url": "https://youtu.be/dQw4w9WgXcQ", "title": '"><script>x</script>'},
					{"type": "link", "url": "https://example.com/?a=<b>", "title": "<img src=x onerror=1>"},
				),
			)
		)
		status, html, _ = render(f"/learn/{self.space}/{doc.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn('src="https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ"', html)
		self.assertIn('sandbox="allow-scripts allow-same-origin allow-presentation allow-popups"', html)
		self.assertIn('rel="noopener noreferrer nofollow"', html)
		self.assertNotIn("<script>x</script>", html)
		self.assertNotIn("<img src=x onerror=1>", html)

	# ------------------------------------------------------------ assignments

	def _assignment(self, **kw):
		course = make_course(self.space, "Assign course", [[self.l1, self.l2]], instructors=[self.vip])
		a = frappe.get_doc(
			{
				"doctype": "TCD Assignment",
				"title": "Essay",
				"content": self.l1.name,
				"course": course.name,
				"submission_type": "Text",
				"max_score": 10,
				"pass_score": 6,
				**kw,
			}
		).insert()
		return course, a

	def test_assignment_validation(self):
		other = make_course(self.space, "Other", [[self.l2]])
		for bad in ({"pass_score": 20}, {"max_score": 0}, {"course": other.name}):
			with self.assertRaises(frappe.ValidationError, msg=bad):
				frappe.get_doc(
					{
						"doctype": "TCD Assignment",
						"title": "X",
						"content": self.l1.name,
						"max_score": 10,
						"pass_score": 5,
						**bad,
					}
				).insert()

	def test_assignment_flow(self):
		course, a = self._assignment()
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		with self.assertRaises(frappe.ValidationError):
			api.complete_lesson(self.l1.name)  # required assignment not passed
		with self.assertRaises(frappe.ValidationError):
			api.submit_assignment(a.name, answer_text="   ")
		sub = api.submit_assignment(a.name, answer_text="My essay")
		self.assertEqual(sub["status"], "Submitted")
		self.assertEqual(api.get_lesson(self.l1.name)["assignment"]["submission"]["status"], "Submitted")

		frappe.set_user(self.reviewer)  # not an instructor of the course
		with self.assertRaises(frappe.PermissionError):
			api.grade_submission(sub["name"], "Graded", 8)

		frappe.set_user(self.vip)
		with self.assertRaises(frappe.ValidationError):
			api.grade_submission(sub["name"], "Returned")  # feedback required
		with self.assertRaises(frappe.ValidationError):
			api.grade_submission(sub["name"], "Graded", 11)
		api.grade_submission(sub["name"], "Returned", feedback="Add an example")

		frappe.set_user(self.learner)
		api.submit_assignment(a.name, answer_text="My essay with an example")
		frappe.set_user(self.vip)
		res = api.grade_submission(sub["name"], "Graded", 8, "Good")
		self.assertTrue(res["passed"])
		self.assertEqual(
			frappe.db.get_value("TCD Progress", {"user": self.learner, "content": self.l1.name}, "status"),
			"Completed",
		)
		self.assertEqual(enrollment(self.learner, course.name).percent, 50)

		frappe.set_user(self.learner)
		with self.assertRaises(frappe.ValidationError):
			api.submit_assignment(a.name, answer_text="again")  # graded is final
		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc("TCD Assignment Submission", sub["name"]).save(ignore_permissions=True)

	def test_assignment_files_and_privacy(self):
		course, a = self._assignment(submission_type="File", due_date=add_days(now_datetime(), -1))
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		frappe.set_user(self.vip)
		api.enroll("Course", course.name)

		mine = make_file("answer.txt", b"answer", user=self.learner)
		theirs = make_file("other.txt", b"other", user=self.vip)
		bad_ext = make_file("answer.exe", b"MZ", user=self.learner)
		frappe.set_user(self.learner)
		for url in (theirs.file_url, bad_ext.file_url):
			with self.assertRaises(frappe.ValidationError, msg=url):
				api.submit_assignment(a.name, attachment=url)
		res = api.submit_assignment(a.name, attachment=mine.file_url)
		self.assertTrue(res["is_late"])
		self.assertEqual(
			frappe.db.get_value("File", mine.name, ["attached_to_doctype", "attached_to_name"]),
			("TCD Assignment Submission", res["name"]),
		)

		frappe.set_user(self.vip)
		vip_sub = api.submit_assignment(a.name, attachment=theirs.file_url)
		frappe.set_user(self.learner)
		self.assertEqual(set(frappe.get_list("TCD Assignment Submission", pluck="user")), {self.learner})
		self.assertFalse(frappe.has_permission("TCD Assignment Submission", "read", vip_sub["name"]))

		# an instructor of another course sees nothing
		frappe.set_user("Administrator")
		frappe.db.delete("TCD Course Instructor", {"parent": course.name})
		frappe.set_user(self.vip)
		self.assertEqual(set(frappe.get_list("TCD Assignment Submission", pluck="user")), {self.vip})

	# ------------------------------------------------------------ feedback

	def test_course_feedback(self):
		course = make_course(self.space, "Rated", [[self.l1]], instructors=[self.vip])
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.rate_course(course.name, 5)
		api.enroll("Course", course.name)
		with self.assertRaises(frappe.ValidationError):
			api.rate_course(course.name, 7)
		api.rate_course(course.name, 4, "Nice")
		res = api.rate_course(course.name, 5, "Great")
		self.assertEqual(res["rating"], {"average": 5.0, "count": 1})
		self.assertEqual(api.get_course(course.name)["my_feedback"].rating, 5)

		frappe.set_user(self.vip)
		self.assertEqual(len(frappe.get_list("TCD Course Feedback")), 1)
		frappe.set_user(self.author)
		self.assertFalse(frappe.has_permission("TCD Course Feedback", "read"))

	# ------------------------------------------------------------ dashboards

	def test_dashboards(self):
		course, a = self._assignment()
		mine2 = make_course(self.space, "Second", [[self.l2]], rule="Manual Approval", instructors=[self.vip])
		not_mine = make_course(self.space, "Not taught", [[self.l2]])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.enroll("Course", mine2.name)
		api.enroll("Course", not_mine.name)
		api.submit_assignment(a.name, answer_text="answer")
		api.complete_lesson(self.l2.name)
		frappe.db.set_value(
			"TCD Enrollment", enrollment(self.learner, course.name).name, "due_date", "2000-01-01"
		)

		data = my_learning(self.learner)
		self.assertEqual(data["summary"]["pending_approval"], 1)  # mine2 is manual approval
		self.assertEqual(data["summary"]["completed"], 1)  # not_mine
		self.assertGreaterEqual(data["summary"]["overdue"], 1)
		self.assertEqual([x.status for x in data["assignments"]], ["Submitted"])

		frappe.set_user(self.vip)
		dash = instructor_dashboard(self.vip)
		self.assertEqual({c["course"] for c in dash["courses"]}, {course.name, mine2.name})
		self.assertEqual(len(dash["pending_approvals"]), 1)
		self.assertEqual(len(dash["to_grade"]), 1)
		_cols, rows, _m, _chart, summary = report.execute({})
		self.assertEqual(len(rows), 2)
		self.assertEqual({s["label"]: s["value"] for s in summary}["Enrolled"], 2)

		status, html, _ = render("/learn/my", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("Essay", html)
		status, _, _ = render("/learn/instructor", self.learner)
		self.assertEqual(status, 404)
		status, html, _ = render("/learn/instructor", self.vip)
		self.assertEqual(status, 200)
		self.assertIn("tcd-approve", html)

	def test_permission_helpers(self):
		course = make_course(self.space, "Helper", [[self.l1]], instructors=[self.vip])
		self.assertTrue(permissions.is_instructor_of(self.vip, course.name))
		self.assertFalse(permissions.is_instructor_of(self.reviewer, course.name))
		self.assertTrue(permissions.is_instructor_of("Administrator", course.name))
