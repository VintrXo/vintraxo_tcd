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
