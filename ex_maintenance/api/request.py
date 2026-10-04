import frappe


@frappe.whitelist()
def get_all_ex_requests():
	return {"data": frappe.get_list("Ex Requests", fields=["name", "creation"], limit_page_length=0)}


#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.request.get_all_ex_requests
