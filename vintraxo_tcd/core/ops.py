"""Production readiness check (Phase 21, ADR-0029).

Read-only: lists what a site still needs before real users rely on it. Run from the Desk (Learning
Settings → Readiness check) or `bench --site <site> execute vintraxo_tcd.core.ops.print_readiness`."""

import glob
import os
import time

import frappe
from frappe import _

from vintraxo_tcd.core.permissions import is_admin

OK, WARN, FAIL = "ok", "warn", "fail"
TCD_ROLES = (
	"TCD Administrator",
	"TCD Content Author",
	"TCD Content Reviewer",
	"TCD Instructor",
	"TCD Learner",
)


def _item(area: str, status: str, message: str, fix: str = "") -> dict:
	return {"area": area, "status": status, "message": message, "fix": fix}


def _latest_backup_age_hours() -> float | None:
	files = glob.glob(frappe.get_site_path("private", "backups", "*-database.sql.gz"))
	if not files:
		return None
	return (time.time() - max(os.path.getmtime(f) for f in files)) / 3600


def readiness() -> list[dict]:
	out = []
	conf = frappe.local.conf
	settings = frappe.get_single("TCD Settings")

	# ------------------------------------------------------------ site
	from frappe.utils.scheduler import is_scheduler_inactive

	if is_scheduler_inactive(verbose=False):
		out.append(
			_item(
				_("Site"),
				FAIL,
				_(
					"The scheduler is off: reminders, meeting links, review dates and queued integrations will not run."
				),
				"bench --site <site> enable-scheduler",
			)
		)
	else:
		out.append(_item(_("Site"), OK, _("The scheduler is on.")))
	if conf.get("host_name"):
		out.append(_item(_("Site"), OK, _("Site address: {0}").format(conf.host_name)))
	else:
		out.append(
			_item(
				_("Site"),
				WARN,
				_("host_name is not set: links in e-mails and certificates may point to the wrong address."),
				"bench --site <site> set-config host_name https://your-domain",
			)
		)
	if not conf.get("encryption_key"):
		out.append(
			_item(
				_("Site"),
				FAIL,
				_("encryption_key is missing: saved passwords and tokens cannot be read."),
				"",
			)
		)
	if conf.get("developer_mode"):
		out.append(
			_item(
				_("Site"),
				WARN,
				_("developer_mode is on. Turn it off on the production server."),
				"bench --site <site> set-config developer_mode 0",
			)
		)

	age = _latest_backup_age_hours()
	if age is None:
		out.append(
			_item(
				_("Backups"),
				FAIL,
				_("No database backup found on this site."),
				"bench setup backups (production) or bench --site <site> backup --with-files",
			)
		)
	elif age > 26:
		out.append(
			_item(
				_("Backups"),
				WARN,
				_("The latest backup is {0} hours old.").format(int(age)),
				"bench setup backups",
			)
		)
	else:
		out.append(_item(_("Backups"), OK, _("The latest backup is {0} hours old.").format(int(age))))

	from frappe.email.doctype.email_account.email_account import EmailAccount

	try:
		account = EmailAccount.find_outgoing(_raise_error=False)
	except Exception:
		account = None
	if account and getattr(account, "name", None):
		out.append(_item(_("E-mail"), OK, _("Outgoing e-mail account: {0}").format(account.name)))
	else:
		out.append(
			_item(
				_("E-mail"),
				WARN,
				_("No outgoing e-mail account: learners get in-app notifications only."),
				_("Desk → Email Account"),
			)
		)

	# ------------------------------------------------------------ learning settings
	if not settings.enable_portal:
		out.append(
			_item(
				_("Learning"),
				FAIL,
				_("The learning portal (/learn) is turned off."),
				_("Learning Settings → Enable Portal"),
			)
		)
	else:
		out.append(_item(_("Learning"), OK, _("The learning portal is on.")))
	if settings.get("enable_guest_access"):
		out.append(
			_item(
				_("Learning"),
				WARN,
				_("Visitors without login can read public pages. Make sure this is intended."),
			)
		)
	if settings.get("allow_scorm"):
		out.append(
			_item(_("Learning"), WARN, _("SCORM packages are allowed: only upload packages you trust."))
		)

	for role in TCD_ROLES:
		if not frappe.db.exists("Role", role):
			out.append(_item(_("Roles"), FAIL, _("Role {0} is missing (run migrate).").format(role)))
	users = frappe.db.sql(
		"""select count(distinct parent) from `tabHas Role` where role in %(r)s and parenttype='User'""",
		{"r": TCD_ROLES},
	)[0][0]
	out.append(_item(_("Roles"), OK if users else WARN, _("{0} users have learning roles.").format(users)))

	# ------------------------------------------------------------ integrations
	ai = frappe.get_single("TCD AI Settings")
	if ai.enabled and not ai.get_password("api_key", raise_exception=False):
		out.append(_item(_("Integrations"), FAIL, _("The AI assistant is on but has no API key.")))
	elif ai.enabled:
		out.append(_item(_("Integrations"), OK, _("The AI assistant is on.")))
	else:
		out.append(_item(_("Integrations"), WARN, _("The AI assistant is off."), _("AI Settings")))
	if settings.get("runner_enabled") and not settings.get("runner_url"):
		out.append(_item(_("Integrations"), FAIL, _("The code runner is on but has no URL.")))
	elif not settings.get("runner_enabled"):
		out.append(
			_item(
				_("Integrations"),
				WARN,
				_(
					"The server code runner (Judge0) is off: only browser languages run (Python, SQL, JavaScript, HTML)."
				),
				"docs/PHASE10_ISOLATION_DESIGN.md",
			)
		)
	provider = settings.get("meeting_provider")
	if provider == "Zoom" and not settings.get("zoom_account_id"):
		out.append(_item(_("Integrations"), FAIL, _("Zoom is selected but its credentials are missing.")))
	paid = frappe.db.count("TCD Course", {"paid": 1, "status": "Published"})
	if paid and not settings.get("payment_gateway"):
		out.append(
			_item(
				_("Integrations"),
				FAIL,
				_("{0} paid courses are published but no payment gateway is set.").format(paid),
			)
		)

	# ------------------------------------------------------------ content
	for c in frappe.get_all(
		"TCD Course",
		filters={"status": "Published", "issue_certificate": 1, "requires_evaluation": 1},
		fields=["name", "title"],
	):
		from vintraxo_tcd.core import evaluations

		if not evaluations.evaluators_for(c.name):
			out.append(
				_item(
					_("Courses"),
					FAIL,
					_("{0} needs an evaluation but has no active evaluator.").format(c.title),
					_("Evaluators"),
				)
			)
	spaces = frappe.db.count("TCD Space", {"is_active": 1})
	pages = frappe.db.count("TCD Content", {"status": "Published"})
	out.append(
		_item(
			_("Content"),
			OK if pages else WARN,
			_("{0} active spaces, {1} published pages.").format(spaces, pages),
		)
	)
	overdue = len(
		frappe.get_all(
			"TCD Content",
			filters=[
				["status", "=", "Published"],
				["next_review_date", "is", "set"],
				["next_review_date", "<", frappe.utils.nowdate()],
			],
			pluck="name",
		)
	)
	if overdue:
		out.append(
			_item(_("Content"), WARN, _("{0} published pages are past their review date.").format(overdue))
		)
	return out


def summary(items: list[dict]) -> dict:
	return {s: sum(1 for i in items if i["status"] == s) for s in (OK, WARN, FAIL)}


@frappe.whitelist()
def readiness_report() -> dict:
	if not is_admin(frappe.session.user):
		raise frappe.PermissionError
	items = readiness()
	return {"items": items, "summary": summary(items)}


def print_readiness():
	"""bench --site <site> execute vintraxo_tcd.core.ops.print_readiness"""
	items = readiness()
	marks = {OK: "OK  ", WARN: "WARN", FAIL: "FAIL"}
	for i in items:
		line = f"[{marks[i['status']]}] {i['area']}: {i['message']}"
		if i["fix"] and i["status"] != OK:
			line += f"  ->  {i['fix']}"
		print(line)
	print(summary(items))
