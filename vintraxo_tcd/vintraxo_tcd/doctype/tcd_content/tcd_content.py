import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime

from vintraxo_tcd.core import content as svc


class TCDContent(Document):
	def validate(self):
		self.set_defaults()
		self.validate_category()
		svc.validate_lessons(self)

		blocks = svc.validate_blocks(svc.parse_blocks(self.blocks))
		self.blocks = svc.dump_blocks(blocks)
		self.search_text = svc.build_search_text(self.title, self.summary, blocks)
		svc.ensure_unique_slug(self)

		before = self.get_doc_before_save()
		if before:
			svc.validate_locked_fields(self, before)
			if before.status != self.status:
				svc.validate_transition(self, before.status, self.status)
		else:
			svc.validate_transition(self, None, self.status)

		if self.status == "Published" and not self.published_on:
			self.published_on = now_datetime()
		if self.status == "Draft":
			self.published_on = None

	def set_defaults(self):
		if not self.language or not self.visibility:
			settings = frappe.get_cached_doc("TCD Settings")
			self.language = self.language or settings.default_language or "ar"
			self.visibility = self.visibility or settings.default_visibility or "Internal"

	def validate_category(self):
		if self.category and frappe.db.get_value("TCD Category", self.category, "space") != self.space:
			frappe.throw(_("Category must belong to the same space."))

	def on_update(self):
		if self.flags.snapshot:
			self.flags.snapshot = False
			version = svc.create_snapshot(self)
			self.db_set(
				{
					"current_version": version,
					"approved_by": frappe.session.user,
					"approved_on": now_datetime(),
				}
			)

	def on_trash(self):
		frappe.db.delete("TCD Content Relation", {"from_content": self.name})
		frappe.db.delete("TCD Content Relation", {"to_content": self.name})
		frappe.db.delete("TCD Progress", {"content": self.name})
		frappe.db.set_value("TCD Content", self.name, "current_version", None)
		frappe.db.delete("TCD Content Version", {"content": self.name})
