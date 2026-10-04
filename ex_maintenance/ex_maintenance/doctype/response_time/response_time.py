# Copyright (c) 2024, Nortex and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ResponseTime(Document):
	pass


def get_average_response_seconds():
	"""Average seconds between a request being raised and its Work Order being completed."""
	result = frappe.db.sql(
		"""
		select avg(timestampdiff(second,
			timestamp(request_date, request_time),
			timestamp(completed_date, completed_time)))
		from `tabResponse Time`
		where request_date is not null and request_time is not null
			and completed_date is not null and completed_time is not null
		"""
	)
	return float(result[0][0] or 0)


def format_duration(seconds):
	if seconds < 60:
		return f"{seconds:.2f} seconds"
	if seconds < 3600:
		return f"{seconds / 60:.2f} minutes"
	return f"{seconds / 3600:.2f} hours"


# ! Used by the "Average Response Time" number card (called with `filters`) and the API
@frappe.whitelist()
def calculate_average_response_time(filters=None):
	frappe.has_permission("Response Time", "read", throw=True)
	return format_duration(get_average_response_seconds())
