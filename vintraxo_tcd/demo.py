"""Demo content for trying the learner portal.

bench --site <site> execute vintraxo_tcd.demo.create_demo

Idempotent: re-running updates nothing that already exists.
"""

import json

import frappe

SPACE = "demo-python"


def _content(title, content_type, blocks, **kw):
	name = frappe.db.get_value("TCD Content", {"space": SPACE, "title": title})
	if name:
		return frappe.get_doc("TCD Content", name)
	doc = frappe.get_doc(
		{
			"doctype": "TCD Content",
			"space": SPACE,
			"title": title,
			"content_type": content_type,
			"language": "ar",
			"visibility": "Public",
			"blocks": json.dumps(blocks, ensure_ascii=False),
			**kw,
		}
	).insert(ignore_permissions=True)
	for status in ("In Review", "Approved", "Published"):
		doc.status = status
		doc.save(ignore_permissions=True)
	return doc


def create_demo():
	if frappe.session.user == "Guest":
		frappe.set_user("Administrator")
	if not frappe.db.exists("TCD Space", SPACE):
		frappe.get_doc(
			{
				"doctype": "TCD Space",
				"space_name": SPACE,
				"title": "بايثون للمبتدئين",
				"visibility": "Public",
				"description": "مساحة تجريبية: دروس قصيرة مع محرر أكواد واختبار.",
			}
		).insert(ignore_permissions=True)

	l1 = _content(
		"مقدمة في بايثون",
		"Lesson",
		[
			{"type": "heading", "text": "أول برنامج", "level": 1},
			{
				"type": "paragraph",
				"text": "الدالة print تطبع النص على الشاشة.\nجرّب تشغيل الكود وغيّر الرسالة.",
			},
			{
				"type": "playground",
				"language": "python",
				"code": 'print("مرحبا يا عالم")',
				"expected_output": "مرحبا يا عالم",
			},
			{"type": "callout", "variant": "tip", "title": "معلومة", "text": "الكود يعمل داخل متصفحك فقط."},
		],
		summary="اكتب أول سطر كود بلغة بايثون.",
	)
	l2 = _content(
		"المتغيرات",
		"Lesson",
		[
			{"type": "paragraph", "text": "المتغير اسم يشير إلى قيمة."},
			{"type": "code", "language": "python", "code": "x = 5\ny = x * 2\nprint(y)"},
			{
				"type": "playground",
				"language": "python",
				"code": "x = 5\nprint(x * 2)",
				"expected_output": "10",
			},
			{"type": "list", "items": ["الاسم يبدأ بحرف", "لا مسافات في الاسم"]},
		],
	)
	l3 = _content(
		"استعلامات SQL",
		"Lesson",
		[
			{"type": "paragraph", "text": "قاعدة بيانات SQLite جديدة تُنشأ مع كل تشغيل."},
			{
				"type": "playground",
				"language": "sql",
				"code": "create table students(name text, grade int);\n"
				"insert into students values ('سارة', 90), ('عمر', 75);\n"
				"select * from students where grade > 80;",
			},
		],
	)
	_content(
		"مسار بايثون الأول",
		"Tutorial",
		[{"type": "paragraph", "text": "ثلاثة دروس قصيرة. أكمل الدروس الإلزامية لإنهاء المسار."}],
		lessons=[{"lesson": l1.name}, {"lesson": l2.name}, {"lesson": l3.name, "is_optional": 1}],
	)
	if not frappe.db.exists("TCD Quiz", {"content": l2.name}):
		frappe.get_doc(
			{
				"doctype": "TCD Quiz",
				"title": "اختبار المتغيرات",
				"content": l2.name,
				"pass_percentage": 50,
				"max_attempts": 0,
				"questions": [
					{
						"question": "ما ناتج print(3 * 2)؟",
						"question_type": "Single Choice",
						"options": "5\n6\n32",
						"correct_answers": "2",
						"explanation": "ناتج 3 * 2 هو 6",
					},
					{
						"question": "اسم المتغير يمكن أن يحتوي مسافة.",
						"question_type": "True False",
						"correct_answers": "2",
					},
				],
			}
		).insert(ignore_permissions=True)
	_demo_course(l1, l2, l3)
	_demo_lms(l3)
	_demo_relations(l1, l2, l3)
	frappe.db.commit()
	return f"/learn/{SPACE}"


def _demo_course(l1, l2, l3):
	"""Phase 1 demo: a sequenced course and a learning path."""
	course = frappe.db.get_value("TCD Course", {"space": SPACE, "title": "أساسيات بايثون"})
	if not course:
		doc = frappe.get_doc(
			{
				"doctype": "TCD Course",
				"title": "أساسيات بايثون",
				"space": SPACE,
				"visibility": "Public",
				"language": "ar",
				"completion_rule": "Required Sequence",
				"summary": "دورة قصيرة بترتيب إلزامي: كل درس يفتح بعد اللي قبله.",
			}
		).insert(ignore_permissions=True)
		frappe.get_doc(
			{
				"doctype": "TCD Chapter",
				"course": doc.name,
				"title": "البداية",
				"sort_order": 1,
				"items": [{"content": l1.name}, {"content": l2.name}],
			}
		).insert(ignore_permissions=True)
		frappe.get_doc(
			{
				"doctype": "TCD Chapter",
				"course": doc.name,
				"title": "قواعد البيانات",
				"sort_order": 2,
				"items": [{"content": l3.name, "is_optional": 1}],
			}
		).insert(ignore_permissions=True)
		doc.reload()
		doc.status = "Published"
		doc.save(ignore_permissions=True)
		course = doc.name
	if not frappe.db.exists("TCD Learning Path", {"space": SPACE, "title": "مسار مطوّر بايثون"}):
		path = frappe.get_doc(
			{
				"doctype": "TCD Learning Path",
				"title": "مسار مطوّر بايثون",
				"space": SPACE,
				"visibility": "Public",
				"language": "ar",
				"summary": "ابدأ بأساسيات بايثون.",
				"items": [{"course": course}],
			}
		).insert(ignore_permissions=True)
		path.status = "Published"
		path.save(ignore_permissions=True)


def _demo_lms(sql_lesson):
	"""Phase 1 demo: instructor, a video lesson and an assignment."""
	course = frappe.get_doc("TCD Course", {"space": SPACE, "title": "أساسيات بايثون"})
	if not any(r.user == "Administrator" for r in course.instructors):
		course.append("instructors", {"user": "Administrator"})
		course.save(ignore_permissions=True)
	_content(
		"شرح بالفيديو",
		"Lesson",
		[
			{"type": "paragraph", "text": "شاهد الفيديو ثم جرّب بنفسك."},
			{
				"type": "video",
				"url": "https://www.youtube.com/watch?v=kqtD5dpn9C8",
				"title": "Python for Beginners",
			},
			{"type": "link", "url": "https://docs.python.org/3/tutorial/", "title": "دليل بايثون الرسمي"},
		],
		lesson_type="Video",
	)
	if not frappe.db.exists("TCD Assignment", {"content": sql_lesson.name}):
		frappe.get_doc(
			{
				"doctype": "TCD Assignment",
				"title": "تكليف: استعلام بنفسك",
				"content": sql_lesson.name,
				"course": course.name,
				"submission_type": "Text",
				"max_score": 10,
				"pass_score": 6,
				"required_to_complete": 0,
				"instructions": "اكتب استعلام SQL يعرض الطلاب الحاصلين على أكثر من 70 مرتّبين تنازليًا.",
			}
		).insert(ignore_permissions=True)


def _demo_relations(l1, l2, l3):
	"""Phase 2 demo: prerequisites, next and related links across pillars."""
	course = frappe.db.get_value("TCD Course", {"space": SPACE, "title": "أساسيات بايثون"})
	video = frappe.db.get_value("TCD Content", {"space": SPACE, "title": "شرح بالفيديو"})
	links = [
		(l2.name, "Prerequisite", "Content", l1.name),
		(video, "Next", "Content", l1.name),
		(l3.name, "Related", "Course", course),
	]
	field = {"Content": "to_content", "Course": "to_course"}
	for source, kind, target_type, target in links:
		if not (source and target):
			continue
		filters = {
			"from_content": source,
			"relation_type": kind,
			"target_type": target_type,
			field[target_type]: target,
		}
		if not frappe.db.exists("TCD Content Relation", filters):
			frappe.get_doc({"doctype": "TCD Content Relation", **filters}).insert(ignore_permissions=True)
