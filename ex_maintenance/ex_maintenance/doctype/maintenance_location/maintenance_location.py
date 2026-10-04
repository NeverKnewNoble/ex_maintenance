# Copyright (c) 2026, Nortex and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class MaintenanceLocation(Document):
	def validate(self):
		self.remove_duplicate_issues()

	def remove_duplicate_issues(self):
		seen = set()
		for row in list(self.issues):
			if row.issue in seen:
				self.remove(row)
			seen.add(row.issue)
