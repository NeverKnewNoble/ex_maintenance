import frappe
from frappe import _

#  ! API call to get cards count and data
import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_work_order_count():
    # Query to count documents with status "Open" or "Completed"
    open_count = frappe.db.count('Ex Work Order', filters={'status': 'Open'})
    completed_count = frappe.db.count('Ex Work Order', filters={'status': 'Completed'})

    # Call the existing function and get the average response time
    average_response_time = frappe.call('ex_maintenance.ex_maintenance.doctype.response_time.response_time.calculate_average_response_time')

    return {
        "open_count": open_count,
        "completed_count": completed_count,
        "average_response_time": average_response_time
    }



#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.card.get_work_order_count
