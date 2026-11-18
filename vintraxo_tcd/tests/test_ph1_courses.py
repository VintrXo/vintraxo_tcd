import frappe
from frappe.tests import IntegrationTestCase

from vintraxo_tcd import api
from vintraxo_tcd.core import courses
from vintraxo_tcd.tests.test_p1 import USERS, make_content, make_space, make_user, publish
from vintraxo_tcd.tests.test_p2 import make_quiz
from vintraxo_tcd.tests.test_p3 import render

CLEAN = (
	"TCD Enrollment",
	"TCD Student Group",
	"TCD Chapter",
	"TCD Learning Path",
	"TCD Course",
	"TCD Quiz Submission",
	"TCD Quiz",
	"TCD Progress",
	"TCD Tutorial Lesson",
	"TCD Content Version",
	"TCD Content",
)


def lesson(space, title, **kw):
	return publish(make_content(space, title, content_type="Lesson", visibility="Public", **kw))


def make_course(space, title, chapters, rule="All Items", publish_it=True, **kw):
	"""chapters = [[content_doc | (content_doc, optional)], ...]"""
	frappe.set_user("Administrator")
	course = frappe.get_doc(
		{
			"doctype": "TCD Course",
			"title": title,
			"space": space,
			"visibility": "Public",
			"completion_rule": rule,
			**kw,
		}
	).insert()
	for i, items in enumerate(chapters):
		rows = []
		for it in items:
			doc, optional = it if isinstance(it, tuple) else (it, 0)
			rows.append({"content": doc.name, "is_optional": optional})
		frappe.get_doc(
			{
				"doctype": "TCD Chapter",
				"course": course.name,
				"title": f"Ch {i + 1}",
				"sort_order": i,
				"items": rows,
			}
		).insert()
	if publish_it:
		course.reload()
		course.status = "Published"
		course.save()
	return course


def enrollment(user, course=None, path=None):
	filters = {"user": user, "course": course} if course else {"user": user, "learning_path": path}
	name = frappe.db.get_value("TCD Enrollment", filters)
	return frappe.get_doc("TCD Enrollment", name) if name else None


class TestPhase1Courses(IntegrationTestCase):
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
		for dt in CLEAN:
			frappe.db.delete(dt)
		frappe.db.delete("TCD Learning Item")
		frappe.db.delete("TCD Student Group Member")
		self.space = make_space("ph1-public").name
		self.l1 = lesson(self.space, "Lesson A")
		self.l2 = lesson(self.space, "Lesson B")
		self.l3 = lesson(self.space, "Lesson C")

	def tearDown(self):
		frappe.set_user("Administrator")

	# ------------------------------------------------------------ structure

	def test_chapter_item_rules(self):
		course = make_course(self.space, "Structure", [[self.l1]], publish_it=False)
		tutorial = make_content(self.space, "Tut", content_type="Tutorial")
		other = make_space("ph1-other").name
		foreign = make_content(other, "Foreign", content_type="Lesson")

		def chapter(items):
			return frappe.get_doc(
				{
					"doctype": "TCD Chapter",
					"course": course.name,
					"title": "X",
					"items": [{"content": c} for c in items],
				}
			).insert()

		for bad in ([tutorial.name], [foreign.name], [self.l1.name], [self.l2.name, self.l2.name]):
			with self.assertRaises(frappe.ValidationError, msg=bad):
				chapter(bad)
		ch = chapter([self.l2.name])
		self.assertEqual(ch.items[0].item_title, "Lesson B")

	def test_publish_rules(self):
		draft = make_content(self.space, "Draft lesson", content_type="Lesson", visibility="Public")
		course = make_course(self.space, "Pub", [[self.l1, draft]], publish_it=False)
		course.status = "Published"
		with self.assertRaises(frappe.ValidationError):
			course.save()  # required item not published

		empty = frappe.get_doc({"doctype": "TCD Course", "title": "Empty", "space": self.space}).insert()
		empty.status = "Published"
		with self.assertRaises(frappe.ValidationError):
			empty.save()

		ok = make_course(self.space, "Author cannot publish", [[self.l1]], publish_it=False)
		frappe.set_user(self.author)
		ok = frappe.get_doc("TCD Course", ok.name)
		ok.status = "Published"
		with self.assertRaises(frappe.PermissionError):
			ok.save()

	def test_published_course_structure_locked(self):
		course = make_course(self.space, "Locked", [[self.l1]])
		ch = frappe.get_doc("TCD Chapter", {"course": course.name})
		ch.append("items", {"content": self.l2.name})
		with self.assertRaises(frappe.ValidationError):
			ch.save()
		self.assertTrue(course.slug)

	# ------------------------------------------------------------ completion rules

	def test_all_items_rollup(self):
		course = make_course(self.space, "All", [[self.l1], [self.l2, (self.l3, 1)]])
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		e = enrollment(self.learner, course.name)
		self.assertEqual((e.status, e.percent), ("Active", 50))

		state = courses.course_status(self.learner, course.name)
		self.assertEqual([c["percent"] for c in state["chapters"]], [100, 0])

		api.complete_lesson(self.l2.name)  # optional l3 not needed
		e.reload()
		self.assertEqual((e.status, e.percent), ("Completed", 100))
		self.assertTrue(e.completed_on)

	def test_required_sequence(self):
		quiz_lesson = self.l2
		quiz = make_quiz(quiz_lesson.name)
		q = {row.question_type: row.name for row in quiz.questions}
		course = make_course(self.space, "Seq", [[self.l1, self.l2]], rule="Required Sequence")
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		self.assertTrue(courses.course_status(self.learner, course.name)["items"][1]["locked"])

		with self.assertRaises(frappe.ValidationError):
			api.complete_lesson(self.l2.name)
		# passing the quiz early keeps the result but does not complete the lesson
		res = api.submit_quiz(
			quiz.name, {q["Single Choice"]: [2], q["True False"]: [1], q["Multiple Choice"]: [2, 4]}
		)
		self.assertTrue(res["passed"])
		self.assertNotEqual(
			frappe.db.get_value("TCD Progress", {"user": self.learner, "content": self.l2.name}, "status"),
			"Completed",
		)

		api.complete_lesson(self.l1.name)
		api.complete_lesson(self.l2.name)  # quiz already passed
		self.assertEqual(enrollment(self.learner, course.name).status, "Completed")

	def test_sequence_only_applies_to_enrolled_learners(self):
		make_course(self.space, "Seq2", [[self.l1, self.l2]], rule="Required Sequence")
		frappe.set_user(self.learner)
		api.complete_lesson(self.l2.name)  # not enrolled: no gating

	def test_manual_approval(self):
		course = make_course(self.space, "Manual", [[self.l1]], rule="Manual Approval")
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.complete_lesson(self.l1.name)
		e = enrollment(self.learner, course.name)
		self.assertEqual(e.status, "Pending Approval")
		with self.assertRaises(frappe.PermissionError):
			api.approve_enrollment(e.name)

		frappe.set_user(self.vip)  # instructor
		api.approve_enrollment(e.name)
		e.reload()
		self.assertEqual((e.status, e.approved_by), ("Completed", self.vip))
		with self.assertRaises(frappe.ValidationError):
			api.approve_enrollment(e.name)

	def test_minimum_score(self):
		quiz = make_quiz(self.l1.name, required_to_complete=0)
		q = {row.question_type: row.name for row in quiz.questions}
		course = make_course(self.space, "Score", [[self.l1]], rule="Minimum Score", minimum_score=80)
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		api.submit_quiz(quiz.name, {q["Single Choice"]: [2], q["True False"]: [1]})  # 2/4 = 50%
		api.complete_lesson(self.l1.name)
		e = enrollment(self.learner, course.name)
		self.assertEqual((e.status, e.score), ("Active", 50))
		api.submit_quiz(
			quiz.name, {q["Single Choice"]: [2], q["True False"]: [1], q["Multiple Choice"]: [2, 4]}
		)
		e.reload()
		self.assertEqual((e.status, e.score), ("Completed", 100))

	def test_learning_path_rollup(self):
		c1 = make_course(self.space, "P1", [[self.l1]])
		c2 = make_course(self.space, "P2", [[self.l2]])
		path = frappe.get_doc(
			{
				"doctype": "TCD Learning Path",
				"title": "Path",
				"space": self.space,
				"visibility": "Public",
				"items": [{"course": c1.name}, {"course": c2.name}],
			}
		).insert()
		path.status = "Published"
		path.save()

		frappe.set_user(self.learner)
		api.enroll("Learning Path", path.name)
		self.assertTrue(enrollment(self.learner, c1.name) and enrollment(self.learner, c2.name))
		api.complete_lesson(self.l1.name)
		pe = enrollment(self.learner, path=path.name)
		self.assertEqual((pe.status, pe.percent), ("Active", 50))
		api.complete_lesson(self.l2.name)
		pe.reload()
		self.assertEqual(pe.status, "Completed")
		data = api.get_learning_path(path.name)
		self.assertTrue(all(c["completed"] for c in data["courses"]))

		frappe.set_user("Administrator")
		path.reload()
		path.items = path.items[:1]
		with self.assertRaises(frappe.ValidationError):
			path.save()  # published structure is locked

	# ------------------------------------------------------------ enrollment rules

	def test_enrollment_rules(self):
		closed = make_course(self.space, "Closed", [[self.l1]], self_enrollment=0)
		draft = make_course(self.space, "Draft course", [[self.l2]], publish_it=False)
		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.enroll("Course", closed.name)
		with self.assertRaises(frappe.PermissionError):
			api.enroll("Course", draft.name)  # not readable for learners
		with self.assertRaises(frappe.PermissionError):
			frappe.get_doc(
				{
					"doctype": "TCD Enrollment",
					"user": self.learner,
					"enrollment_for": "Course",
					"course": closed.name,
				}
			).insert()  # learners have no create DocPerm

		open_course = make_course(self.space, "Open", [[self.l3]])
		frappe.set_user(self.learner)
		first = api.enroll("Course", open_course.name)
		again = api.enroll("Course", open_course.name)
		self.assertEqual(first["name"], again["name"])

	def test_enroll_group(self):
		restricted_space = make_space("ph1-restricted", "Restricted", roles=["TCD Instructor"]).name
		course = make_course(self.space, "Group course", [[self.l1]], self_enrollment=0)
		hidden_lesson = lesson(restricted_space, "Hidden")
		hidden_course = make_course(restricted_space, "Hidden course", [[hidden_lesson]])
		group = frappe.get_doc(
			{
				"doctype": "TCD Student Group",
				"group_name": "ph1-cohort",
				"members": [{"user": self.learner}, {"user": self.vip}],
			}
		).insert()

		frappe.set_user(self.vip)
		res = api.enroll_group(group.name, "Course", course.name, due_date="2030-01-01")
		self.assertEqual(set(res["enrolled"]), {self.learner, self.vip})
		self.assertEqual(str(enrollment(self.learner, course.name).due_date), "2030-01-01")

		res = api.enroll_group(group.name, "Course", hidden_course.name)
		self.assertEqual(res["enrolled"], [self.vip])  # learner has no access to the restricted space
		self.assertEqual([s["user"] for s in res["skipped"]], [self.learner])

		frappe.set_user(self.learner)
		with self.assertRaises(frappe.PermissionError):
			api.enroll_group(group.name, "Course", course.name)

	# ------------------------------------------------------------ permissions

	def test_permissions(self):
		course = make_course(self.space, "Perm", [[self.l1]])
		draft = make_course(self.space, "Hidden draft", [[self.l2]], publish_it=False)
		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		frappe.set_user(self.vip)
		api.enroll("Course", course.name)

		frappe.set_user(self.learner)
		self.assertEqual(set(frappe.get_list("TCD Course", pluck="name")), {course.name})
		self.assertFalse(frappe.has_permission("TCD Course", "read", draft.name))
		self.assertEqual(
			set(frappe.get_list("TCD Chapter", pluck="course")), {course.name}
		)  # draft chapters hidden
		self.assertEqual(set(frappe.get_list("TCD Enrollment", pluck="user")), {self.learner})
		other = frappe.db.get_value("TCD Enrollment", {"user": self.vip})
		self.assertFalse(frappe.has_permission("TCD Enrollment", "read", other))
		self.assertFalse(frappe.has_permission("TCD Student Group", "read"))

		frappe.set_user(self.vip)
		self.assertEqual(set(frappe.get_list("TCD Enrollment", pluck="user")), {self.learner, self.vip})
		self.assertIn(draft.name, frappe.get_list("TCD Course", pluck="name"))  # staff see drafts

	# ------------------------------------------------------------ portal

	def test_portal_pages(self):
		course = make_course(self.space, "Portal course", [[self.l1, self.l2]], rule="Required Sequence")
		draft = make_course(self.space, "Portal draft", [[self.l3]], publish_it=False)
		status, html, _ = render(f"/learn/{self.space}/course/{course.slug}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-enroll", html)
		self.assertIn("Lesson A", html)

		frappe.set_user(self.learner)
		api.enroll("Course", course.name)
		status, html, _ = render(f"/learn/{self.space}/course/{course.slug}", self.learner)
		self.assertNotIn("tcd-enroll", html)
		self.assertIn("tcd-status-locked", html)

		status, html, _ = render(f"/learn/{self.space}/{self.l2.slug}?course={course.name}", self.learner)
		self.assertEqual(status, 200)
		self.assertIn("tcd-callout-warning", html)  # locked by sequence
		self.assertIn("Portal course", html)  # breadcrumb

		status, _, _ = render(f"/learn/{self.space}/course/{draft.slug}", self.learner)
		self.assertEqual(status, 404)
		status, html, _ = render(f"/learn/{self.space}", self.learner)
		self.assertIn("Portal course", html)
		self.assertNotIn("Portal draft", html)
		status, html, _ = render("/learn", self.learner)
		self.assertIn("tcd-cards", html)
		self.assertIn("Portal course", html)  # my courses
