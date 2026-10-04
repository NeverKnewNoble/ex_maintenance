# Copyright (c) 2024, Nortex and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, nowtime


class ExRequests(Document):
	def validate(self):
		self.validate_location()

	def validate_location(self):
		if not self.location:
			return

		location = frappe.get_cached_value(
			"Maintenance Location", self.location, ["disabled", "requires_room_number"], as_dict=True
		)
		if location.disabled:
			frappe.throw(_("Location {0} is disabled.").format(frappe.bold(self.location)))
		if location.requires_room_number and not self.room_number:
			frappe.throw(_("Please enter the room number for {0}.").format(frappe.bold(self.location)))

	def before_insert(self):
		# ? Stamp the request time on the server so web form submissions are covered too
		if not self.request_date:
			self.request_date = nowdate()
		if not self.request_time:
			self.request_time = nowtime()

	def after_insert(self):
		create_work_order(self)


# ! Create the manager's Work Order for a new request
def create_work_order(ex_request):
	work_order = frappe.get_doc(
		{
			"doctype": "Ex Work Order",
			"location": ex_request.location,
			"room_number": ex_request.room_number,
			"other": ex_request.other,
			"request_code": ex_request.name,
			"date": ex_request.date,
			"time": ex_request.time,
			"further_information": ex_request.further_description,
			"issue": [
				{"issue_type": item.issue_type, "description": item.description}
				for item in ex_request.table_umyd
			],
		}
	)

	# Requests from the public web form are inserted as Guest
	work_order.insert(ignore_permissions=True)
	return work_order.name
