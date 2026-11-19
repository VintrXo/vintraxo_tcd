import re

import frappe
from frappe import _
from frappe.model.document import Document

RUNTIME_URL_FIELDS = ("pyodide_index_url", "sqljs_base_url")


class TCDSettings(Document):
	def validate(self):
		from vintraxo_tcd.core import runner

		runner.validate_settings(self)
		timeout = self.playground_timeout_seconds or 0
		if timeout < 1 or timeout > 60:
			frappe.throw(_("Playground timeout must be between 1 and 60 seconds."))
		for field in RUNTIME_URL_FIELDS:
			url = (self.get(field) or "").strip()
			if not url:
				continue
			if not re.match(r"^(https://|/)", url):
				frappe.throw(_("{0} must start with https:// or /.").format(_(self.meta.get_label(field))))
			self.set(field, url if url.endswith("/") else url + "/")
