"""Phase 31: link the Arabic and English Odoo docs as translations of each other (same slugs in both spaces).
Spaces → key "odoo"; pages → "odoo:<slug>"; courses → "odoo-course:<slug of their first page>".

    echo "exec(open('<app>/deploy/odoo_docs/link_languages.py').read(), {'__name__': '__main__'})" | bench --site <site> console
"""

import frappe

SPACES = {"odoo-ar": "ar", "odoo-en": "en"}


def main():
	pages = courses = 0
	for space, lang in SPACES.items():
		if not frappe.db.exists("TCD Space", space):
			continue
		frappe.db.set_value("TCD Space", space, {"language": lang, "translation_key": "odoo"}, update_modified=False)
		for name, slug in frappe.get_all("TCD Content", filters={"space": space}, fields=["name", "slug"], as_list=True):
			frappe.db.set_value("TCD Content", name, "translation_key", f"odoo:{slug}", update_modified=False)
			pages += 1
		for course in frappe.get_all("TCD Course", filters={"space": space}, pluck="name"):
			chapter = frappe.get_all("TCD Chapter", filters={"course": course}, order_by="sort_order asc", pluck="name", limit=1)
			first = frappe.get_all("TCD Learning Item", filters={"parent": chapter[0] if chapter else ""}, order_by="idx asc", pluck="content", limit=1)
			if first:
				slug = frappe.db.get_value("TCD Content", first[0], "slug")
				frappe.db.set_value("TCD Course", course, "translation_key", f"odoo-course:{slug}", update_modified=False)
				courses += 1
	frappe.db.commit()
	print(f"LINKED pages={pages} courses={courses}")


main()
