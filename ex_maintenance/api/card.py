import frappe

from ex_maintenance.ex_maintenance.doctype.response_time.response_time import (
	calculate_average_response_time,
)


#  ! API call to get cards count and data
@frappe.whitelist()
def get_work_order_count():
	frappe.has_permission("Ex Work Order", "read", throw=True)

	return {
		"open_count": frappe.db.count("Ex Work Order", filters={"status": "Open"}),
		"completed_count": frappe.db.count("Ex Work Order", filters={"status": "Completed"}),
		"average_response_time": calculate_average_response_time(),
	}


#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.card.get_work_order_count
