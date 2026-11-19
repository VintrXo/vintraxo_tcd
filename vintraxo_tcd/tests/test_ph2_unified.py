import frappe

from vintraxo_tcd import api
from vintraxo_tcd.core import connect
from vintraxo_tcd.tests.base import TCDTestCase
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user, publish
from vintraxo_tcd.tests.test_p3 import render
from vintraxo_tcd.tests.test_ph1_courses import CLEAN, enrollment, lesson, make_course


def relate(source, relation_type, target, target_type="Content"):
	field = connect.TARGET_FIELD[target_type]
	return frappe.get_doc(
		{
			"doctype": "TCD Content Relation",
			"from_content": source,
			"relation_type": relation_type,
			"target_type": target_type,
			field: target,
		}
	).insert()


class TestPhase2Unified(TCDTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		frappe.set_user("Administrator")
		for key, (email, roles) in USERS.items():
			setattr(cls, key, make_user(email, roles))
		settings = frappe.get_single("TCD Settings")
		settings.update({"require_approval_before_publish": 1, "enable_portal": 1})
		settings.save()

	def setUp(self):
		frappe.set_user("Administrator")
		for dt in ("TCD Course Feedback", "TCD Assignment Submission", "TCD Assignment", *CLEAN):
			frappe.db.delete(dt)
		for child in ("TCD Learning Item", "TCD Course Instructor", "TCD Course Prerequisite"):
			frappe.db.delete(child)
		self.space = make_space("ph2-public").name
		self.a = lesson(self.space, "أساسيات المتغيرات")
		self.b = lesson(self.space, "الدوال المتقدمة")
		self.c = lesson(self.space, "Lesson C")

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ relations

	def test_relation_validation(self):
		course = make_course(self.space, "Target course", [[self.c]])
		rel = relate(self.b.name, "Related", course.name, "Course")
		self.assertIsNone(rel.to_content)
		for bad in (
			lambda: relate(self.a.name, "Related", self.a.name),  # self
			lambda: relate(self.b.name, "Related", course.name, "Course"),  # duplicate
			lambda: frappe.get_doc(
				{
					"doctype": "TCD Content Relation",
					"from_content": self.a.name,
					"relation_type": "Related",
					"target_type": "Course",
				}
			).insert(),  # no target
		):
			with self.assertRaises(frappe.ValidationError):
				bad()
		relate(self.b.name, "Prerequisite", self.a.name)
		with self.assertRaises(frappe.ValidationError):
			relate(self.a.name, "Prerequisite", self.b.name)  # reverse pair

	def test_relation_permissions(self):
		draft_course = make_course(self.space, "Draft target", [[self.c]], publish_it=False)
		live_course = make_course(self.space, "Live target", [[self.c]])
		hidden = relate(self.a.name, "Related", draft_course.name, "Course")
		shown = relate(self.a.name, "Related", live_course.name, "Course")
		frappe.set_user(self.learner)
		names = set(frappe.get_list("TCD Content Relation", pluck="name"))
		self.assertIn(shown.name, names)
		self.assertNotIn(hidden.name, names)
		self.assertFalse(frappe.has_permission("TCD Content Relation", "read", hidden.name))
		related = connect.related_for_content(self.learner, self.a.name)
		self.assertEqual([r["name"] for r in related["related"]], [live_course.name])

	# ------------------------------------------------------------ prerequisites

	def test_content_prerequisites(self):
		relate(self.b.name, "Prerequisite", self.a.name)
		course = make_course(self.space, "Needed course", [[self.c]])
		relate(self.b.name, "Prerequisite", course.name, "Course")
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.ValidationError):
			api.complete_lesson(self.b.name)
		api.complete_lesson(self.a.name)
		self.assertEqual(connect.unmet_prerequisites(self.learner, self.b.name), ["Needed course"])
		api.enroll("Course", course.name)
		api.complete_lesson(self.c.name)  # completes the course
		self.assertEqual(enrollment(self.learner, course.name).status, "Completed")
		api.complete_lesson(self.b.name)
		prereqs = connect.prerequisites(self.learner, self.b.name)
		self.assertTrue(all(p["satisfied"] for p in prereqs))

		frappe.set_user(self.reviewer)  # staff are never blocked
		self.assertEqual(connect.unmet_prerequisites(self.reviewer, self.b.name), [])

	def test_course_prerequisites(self):
		first = make_course(self.space, "First", [[self.a]], instructors=[self.vip])
		second = make_course(
			self.space, "Second", [[self.b]], instructors=[self.vip], prerequisites=[{"course": first.name}]
		)
		with self.assertRaises(frappe.ValidationError):
			make_course(
				self.space, "Self", [[self.c]], prerequisites=[{"course": first.name}, {"course": first.name}]
			)

		frappe.set_user(self.learner)
		with self.assertRaises(frappe.ValidationError):
			api.enroll("Course", second.name)
		api.enroll("Course", first.name)
		api.complete_lesson(self.a.name)
		api.enroll("Course", second.name)  # now allowed

		frappe.set_user("Administrator")
		batch = frappe.get_doc(
			{"doctype": "TCD Batch", "group_name": "ph2-batch", "members": [{"user": self.vip}]}
		).insert()
		frappe.set_user(self.vip)
		res = api.enroll_batch(batch.name, "Course", second.name)
		self.assertEqual(res["enrolled"], [self.vip])
		self.assertEqual(res["warnings"], [{"user": self.vip, "missing": ["First"]}])

	# ------------------------------------------------------------ used in, navigation

	def test_used_in_and_navigation(self):
		tutorial = publish(
			make_content(
				self.space,
				"Tutorial",
				content_type="Tutorial",
				visibility="Public",
				lessons=[{"lesson": self.a.name}, {"lesson": self.b.name}],
			)
		)
		course = make_course(self.space, "Nav course", [[self.a, self.b], [self.c]])
		path = frappe.get_doc(
			{
				"doctype": "TCD Learning Path",
				"title": "Nav path",
				"space": self.space,
				"visibility": "Public",
				"items": [{"course": course.name}],
			}
		).insert()
		hidden_course = make_course(self.space, "Hidden draft", [[self.a]], publish_it=False)
		relate(self.a.name, "Next", self.b.name)
		relate(self.c.name, "See Also", self.a.name)

		frappe.set_user(self.learner)
		rel = connect.related_for_content(self.learner, self.a.name)
		used = {r["name"] for r in rel["used_in"]}
		self.assertTrue({tutorial.name, course.name} <= used)
		self.assertNotIn(hidden_course.name, used)
		self.assertNotIn(path.name, used)  # path is Draft
		self.assertEqual([r["name"] for r in rel["next"]], [self.b.name])
		self.assertEqual([r["name"] for r in rel["referenced_by"]], [self.c.name])

		nav = connect.course_navigation(self.learner, course.name, self.b.name)
		self.assertEqual((nav["prev"]["name"], nav["next"]["name"]), (self.a.name, self.c.name))

	# ------------------------------------------------------------ unified search

	def test_unified_search(self):
		other_space = make_space("ph2-other").name
		course = make_course(self.space, "دورة شاملة", [[self.a]])  # its chapter is titled "Ch 1"
		draft = make_course(self.space, "دورة مسودة شاملة", [[self.b]], publish_it=False)
		path = frappe.get_doc(
			{
				"doctype": "TCD Learning Path",
				"title": "مسار شامل",
				"space": self.space,
				"visibility": "Public",
				"items": [{"course": course.name}],
			}
		).insert()
		path.status = "Published"
		path.save()
		lesson(other_space, "درس شامل")

		frappe.set_user(self.learner)
		kinds = {r.kind for r in api.search_all("شامل")}
		self.assertEqual(kinds, {"Course", "Learning Path", "Lesson"})
		names = {r.name for r in api.search_all("شامل")}
		self.assertNotIn(draft.name, names)
		self.assertEqual({r.kind for r in api.search_all("شامل", types="Course")}, {"Course"})
		self.assertEqual({r.space for r in api.search_all("شامل", space=self.space)}, {self.space})
		# chapter titles feed the course search text; diacritics are ignored
		self.assertEqual({r.name for r in api.search_all("ch 1", types="Course")}, {course.name})
		self.assertIn(course.name, {r.name for r in api.search_all("دَوْرَة", types="Course")})

	# ------------------------------------------------------------ recommendations

	def test_recommendations(self):
		course = make_course(self.space, "Rec course", [[self.a, self.b]], rule="Required Sequence")
		popular = make_course(self.space, "Popular course", [[self.c]])
		closed = make_course(self.space, "Closed course", [[self.c]], self_enrollment=0)
		relate(self.a.name, "Related", self.c.name)
		frappe.set_user(self.vip)
		api.enroll("Course", popular.name)

		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.a.name)
		recs = {r["name"]: r["reason"] for r in connect.recommendations(self.learner)}
		self.assertEqual(recs.get(self.b.name), "continue")
		self.assertEqual(recs.get(self.c.name), "follow_up")
		self.assertEqual(recs.get(popular.name), "popular")
		self.assertNotIn(closed.name, recs)
		self.assertNotIn(course.name, recs)  # already enrolled

	# ------------------------------------------------------------ portal

	def test_portal(self):
		relate(self.b.name, "Prerequisite", self.a.name)
		relate(self.b.name, "Related", self.c.name)
		first = make_course(self.space, "Portal first", [[self.c]])
		second = make_course(self.space, "Portal second", [[self.a]], prerequisites=[{"course": first.name}])

		status, html, _ = render(f"/learn/{self.space}/{self.b.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-related", html)
		self.assertIn("أساسيات المتغيرات", html)  # prerequisite listed
		self.assertIn("tcd-callout-warning", html)

		status, html, _ = render(f"/learn/{self.space}/course/{second.slug}", self.learner)
		self.assertNotIn("tcd-enroll", html)  # prerequisites unmet
		self.assertIn("Portal first", html)

		status, html, _ = render(f"/learn/{self.space}/{self.a.slug}?course={second.name}", self.learner)
		self.assertIn("Portal second", html)

		status, html, _ = render("/learn?q=Portal&t=Course", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("Portal first", html)
		self.assertNotIn("Lesson C", html)

		frappe.set_user(self.learner)
		api.complete_lesson(self.a.name)
		status, html, _ = render("/learn/my", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("أساسيات المتغيرات", html)  # recently completed
