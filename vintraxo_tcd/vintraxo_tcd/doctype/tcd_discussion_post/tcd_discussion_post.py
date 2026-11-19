from frappe.model.document import Document

from vintraxo_tcd.core import discussions


class TCDDiscussionPost(Document):
	def validate(self):
		discussions.validate(self)
