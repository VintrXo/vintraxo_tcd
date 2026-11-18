import frappe

TCD_ROLES = [
	"TCD Administrator",
	"TCD Content Author",
	"TCD Content Reviewer",
	"TCD Instructor",
	"TCD Learner",
]


def after_install():
	create_roles()
	add_navbar_link()
	frappe.db.commit()


def create_roles():
	for role in TCD_ROLES:
		if frappe.db.exists("Role", role):
			continue
		doc = frappe.get_doc(
			{
				"doctype": "Role",
				"role_name": role,
				"desk_access": 0 if role == "TCD Learner" else 1,
			}
		)
		doc.insert(ignore_permissions=True)


LEARN_URL = "/learn"


def add_navbar_link():
	"""Add a "Learning" item to the website navbar (once; admins can rename or remove it)."""
	settings = frappe.get_single("Website Settings")
	if any(item.url == LEARN_URL for item in settings.top_bar_items):
		return
	settings.append("top_bar_items", {"label": "Learning", "url": LEARN_URL})
	settings.save(ignore_permissions=True)
