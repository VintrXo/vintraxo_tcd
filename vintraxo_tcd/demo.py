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
	frappe.db.commit()
	return f"/learn/{SPACE}"
