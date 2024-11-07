# api.py
import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_all_ex_requests():
    # Fetch only the "name" and "creation" fields from the "Ex Request" doctype
    try:
        ex_requests = frappe.get_all('Ex Requests', fields=["name", "creation"])
        return {"data": ex_requests}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error fetching Ex Request documents")
        return {"error": str(e)}


#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.request.get_all_ex_requests