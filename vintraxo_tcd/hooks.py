app_name = "vintraxo_tcd"
app_title = "VintraXo TCD"
app_publisher = "vintraxo"
app_description = "Training, Content & Documentation"
app_email = "boda10043@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "vintraxo_tcd",
# 		"logo": "/assets/vintraxo_tcd/logo.png",
# 		"title": "VintraXo TCD",
# 		"route": "/vintraxo_tcd",
# 		"has_permission": "vintraxo_tcd.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vintraxo_tcd/css/vintraxo_tcd.css"
# app_include_js = "/assets/vintraxo_tcd/js/vintraxo_tcd.js"

# include js, css files in header of web template
# web_include_css = "/assets/vintraxo_tcd/css/vintraxo_tcd.css"
# web_include_js = "/assets/vintraxo_tcd/js/vintraxo_tcd.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "vintraxo_tcd/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "vintraxo_tcd/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "vintraxo_tcd.utils.jinja_methods",
# 	"filters": "vintraxo_tcd.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "vintraxo_tcd.install.before_install"
# after_install = "vintraxo_tcd.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "vintraxo_tcd.uninstall.before_uninstall"
# after_uninstall = "vintraxo_tcd.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "vintraxo_tcd.utils.before_app_install"
# after_app_install = "vintraxo_tcd.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "vintraxo_tcd.utils.before_app_uninstall"
# after_app_uninstall = "vintraxo_tcd.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "vintraxo_tcd.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vintraxo_tcd.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["vintraxo_tcd.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"vintraxo_tcd.tasks.all"
# 	],
# 	"daily": [
# 		"vintraxo_tcd.tasks.daily"
# 	],
# 	"hourly": [
# 		"vintraxo_tcd.tasks.hourly"
# 	],
# 	"weekly": [
# 		"vintraxo_tcd.tasks.weekly"
# 	],
# 	"monthly": [
# 		"vintraxo_tcd.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "vintraxo_tcd.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "vintraxo_tcd.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "vintraxo_tcd.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "vintraxo_tcd.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["vintraxo_tcd.utils.before_request"]
# after_request = ["vintraxo_tcd.utils.after_request"]

# Job Events
# ----------
# before_job = ["vintraxo_tcd.utils.before_job"]
# after_job = ["vintraxo_tcd.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"vintraxo_tcd.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

after_install = "vintraxo_tcd.install.after_install"

permission_query_conditions = {
	"TCD Space": "vintraxo_tcd.core.permissions.space_query",
	"TCD Category": "vintraxo_tcd.core.permissions.category_query",
	"TCD Content": "vintraxo_tcd.core.permissions.content_query",
	"TCD Content Relation": "vintraxo_tcd.core.permissions.relation_query",
	"TCD Content Version": "vintraxo_tcd.core.permissions.version_query",
	"TCD Quiz": "vintraxo_tcd.core.permissions.quiz_query",
	"TCD Progress": "vintraxo_tcd.core.permissions.progress_query",
	"TCD Quiz Submission": "vintraxo_tcd.core.permissions.submission_query",
	"TCD Course": "vintraxo_tcd.core.permissions.course_query",
	"TCD Learning Path": "vintraxo_tcd.core.permissions.path_query",
	"TCD Chapter": "vintraxo_tcd.core.permissions.chapter_query",
	"TCD Enrollment": "vintraxo_tcd.core.permissions.enrollment_query",
	"TCD Assignment": "vintraxo_tcd.core.permissions.assignment_query",
	"TCD Assignment Submission": "vintraxo_tcd.core.permissions.submission_scope_query",
	"TCD Course Feedback": "vintraxo_tcd.core.permissions.feedback_query",
	"TCD Content Feedback": "vintraxo_tcd.core.permissions.content_feedback_query",
	"TCD User Skill": "vintraxo_tcd.core.permissions.user_skill_query",
	"TCD Certificate": "vintraxo_tcd.core.permissions.certificate_query",
	"TCD Acknowledgment": "vintraxo_tcd.core.permissions.acknowledgment_query",
}

has_permission = {
	"TCD Space": "vintraxo_tcd.core.permissions.space_has_permission",
	"TCD Category": "vintraxo_tcd.core.permissions.category_has_permission",
	"TCD Content": "vintraxo_tcd.core.permissions.content_has_permission",
	"TCD Content Relation": "vintraxo_tcd.core.permissions.relation_has_permission",
	"TCD Content Version": "vintraxo_tcd.core.permissions.version_has_permission",
	"TCD Quiz": "vintraxo_tcd.core.permissions.quiz_has_permission",
	"TCD Progress": "vintraxo_tcd.core.permissions.own_or_staff_has_permission",
	"TCD Quiz Submission": "vintraxo_tcd.core.permissions.own_or_staff_has_permission",
	"TCD Course": "vintraxo_tcd.core.permissions.offering_has_permission",
	"TCD Learning Path": "vintraxo_tcd.core.permissions.offering_has_permission",
	"TCD Chapter": "vintraxo_tcd.core.permissions.chapter_has_permission",
	"TCD Enrollment": "vintraxo_tcd.core.permissions.enrollment_has_permission",
	"TCD Assignment": "vintraxo_tcd.core.permissions.assignment_has_permission",
	"TCD Assignment Submission": "vintraxo_tcd.core.permissions.own_or_course_instructor_has_permission",
	"TCD Course Feedback": "vintraxo_tcd.core.permissions.own_or_course_instructor_has_permission",
	"TCD Content Feedback": "vintraxo_tcd.core.permissions.content_feedback_has_permission",
	"TCD User Skill": "vintraxo_tcd.core.permissions.user_skill_has_permission",
	"TCD Certificate": "vintraxo_tcd.core.permissions.certificate_has_permission",
	"TCD Acknowledgment": "vintraxo_tcd.core.permissions.acknowledgment_has_permission",
}

website_route_rules = [
	{"from_route": "/learn/my", "to_route": "learn/my"},
	{"from_route": "/learn/policies", "to_route": "learn/policies"},
	{"from_route": "/learn/policies/<code>", "to_route": "learn/policy"},
	{"from_route": "/verify/<code>", "to_route": "verify"},
	{"from_route": "/learn/instructor", "to_route": "learn/instructor"},
	{"from_route": "/learn/<space>", "to_route": "learn/space"},
	{"from_route": "/learn/<space>/course/<slug>", "to_route": "learn/course"},
	{"from_route": "/learn/<space>/path/<slug>", "to_route": "learn/path"},
	{"from_route": "/learn/<space>/<slug>", "to_route": "learn/content"},
]

portal_menu_items = [
	{"title": "Learning", "route": "/learn", "reference_doctype": "", "role": "TCD Learner"},
]

add_to_apps_screen = [
	{
		"name": "vintraxo_tcd",
		"logo": "/assets/vintraxo_tcd/images/vx-logo.png",
		"title": "VX",
		"route": "/app/vintraxo-tcd",
		"has_permission": "vintraxo_tcd.core.permissions.has_app_permission",
	}
]

app_include_js = ["/assets/vintraxo_tcd/js/tcd_desk.js"]

scheduler_events = {
	"cron": {
		"*/5 * * * *": ["vintraxo_tcd.core.integrations.process_queue"],
	},
	"daily": [
		"vintraxo_tcd.core.credentials.expire_certificates",
		"vintraxo_tcd.core.governance.daily",
		"vintraxo_tcd.core.training.daily",
		"vintraxo_tcd.core.integrations.purge_sent",
	],
}

# Employee exists only with ERPNext/HRMS; without it this event simply never fires.
doc_events = {
	"User": {"on_update": "vintraxo_tcd.core.training.on_user_update"},
	"Employee": {"on_update": "vintraxo_tcd.core.training.on_employee_update"},
}
