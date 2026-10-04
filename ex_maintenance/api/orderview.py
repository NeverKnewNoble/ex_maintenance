import frappe
from frappe import _

WORK_ORDER_FIELDS = [
	"name",
	"location",
	"request_code",
	"room_number",
	"other",
	"image",
	"date",
	"time",
	"further_information",
	"priority_level",
	"status",
	"is_a_team",
	"team_descriptioninstructions",
	"is_an_indvidual",
	"deadline_date",
	"deadline_time",
	"status_change_logs",
]


#  ! Function TO Display all data from the Doctype to the app
@frappe.whitelist()
def get_all_ex_work_orders(limit_start=0, limit_page_length=0):
	ex_work_orders = frappe.get_list(
		"Ex Work Order",
		fields=WORK_ORDER_FIELDS,
		limit_start=limit_start,
		limit_page_length=limit_page_length,
	)
	names = [work_order.name for work_order in ex_work_orders]

	issues = _get_child_rows("Ex Issue Type", "issue", names, ["idx", "issue_type", "description"])
	assign_tasks = _get_child_rows(
		"Ex Task Assignment", "assign_task", names, ["idx", "employee", "instructions"]
	)

	for work_order in ex_work_orders:
		work_order["issues"] = issues.get(work_order.name, [])
		work_order["assign_task"] = assign_tasks.get(work_order.name, [])

	return {"data": ex_work_orders}


def _get_child_rows(child_doctype, parentfield, parents, fields):
	"""Child rows of the given Ex Work Orders in one query, grouped by parent."""
	if not parents:
		return {}

	rows = frappe.get_all(
		child_doctype,
		filters={"parenttype": "Ex Work Order", "parentfield": parentfield, "parent": ["in", parents]},
		fields=["parent", *fields],
		order_by="idx asc",
	)
	grouped = {}
	for row in rows:
		grouped.setdefault(row.pop("parent"), []).append(row)
	return grouped


#  ! Function TO display Doctype List view into app
@frappe.whitelist()
def ex_work_ui(limit_start=0, limit_page_length=0):
	ex_work_orders = frappe.get_list(
		"Ex Work Order",
		fields=["name", "date", "status", "priority_level"],
		limit_start=limit_start,
		limit_page_length=limit_page_length,
	)
	return {"data": ex_work_orders}


# ! Function to Update the Doctype from the app
# Task Assignments, completion time and Response Time are handled by ExWorkOrder on save.
@frappe.whitelist(methods=["POST", "PUT"])
def update_and_assign_ex_work_order(data):
	data = frappe.parse_json(data)

	ex_work_order = frappe.get_doc("Ex Work Order", data.get("name"))
	ex_work_order.update(
		{
			"priority_level": data.get("priority_level"),
			"status": data.get("status"),
			"is_a_team": data.get("is_a_team", 0),
			"team_descriptioninstructions": data.get("team_descriptioninstructions"),
			"is_an_indvidual": data.get("is_an_indvidual", 0),
			"deadline_date": data.get("deadline_date"),
			"deadline_time": data.get("deadline_time"),
		}
	)
	ex_work_order.set(
		"assign_task",
		[
			{"employee": task.get("employee"), "instructions": task.get("instructions")}
			for task in data.get("assign_task") or []
		],
	)
	ex_work_order.save()

	return {
		"status": "success",
		"message": _("Ex Work Order updated and assigned successfully."),
	}


# ! Function to get the users that can be assigned tasks
@frappe.whitelist()
def get_user_emails():
	frappe.only_for(["System Manager", "Ex Maintenance Manager"])

	return frappe.get_all(
		"User",
		filters={"enabled": 1, "user_type": "System User", "email": ["is", "set"]},
		pluck="email",
	)


#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.orderview.get_all_ex_work_orders
#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.orderview.ex_work_ui
#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.orderview.update_and_assign_ex_work_order
#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.orderview.get_user_emails
