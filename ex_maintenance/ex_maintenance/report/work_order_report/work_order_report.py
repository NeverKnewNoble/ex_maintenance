import frappe
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns()

	# Build conditions for filtering data
	conditions = get_conditions(filters)

	# Fetch data from the database
	data = frappe.db.sql(
		f"""
        SELECT
            request_code,
            status,
            priority_level,
            location,
            room_number,
            other,
            request_date_created,
            request_time_created,
            further_information
        FROM `tabEx Work Order`
        WHERE {conditions}
        ORDER BY request_date_created DESC, request_time_created DESC
    """,
		filters,
		as_dict=True,
	)

	return columns, data


def get_columns():
	return [
		{
			"label": _("Request Code"),
			"fieldname": "request_code",
			"fieldtype": "Link",
			"options": "Ex Requests",
			"width": 130,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Select",
			"options": "Open\nIn Progress\nCompleted\nOverdue",
			"width": 130,
		},
		{
			"label": _("Priority Level"),
			"fieldname": "priority_level",
			"fieldtype": "Select",
			"options": "Low\nMedium\nHigh\nUrgent",
			"width": 130,
		},
		{
			"label": _("Location"),
			"fieldname": "location",
			"fieldtype": "Link",
			"options": "Maintenance Location",
			"width": 130,
		},
		{"label": _("Room Number"), "fieldname": "room_number", "fieldtype": "Data", "width": 120},
		{"label": _("Other"), "fieldname": "other", "fieldtype": "Data", "width": 160},
		{"label": _("Request Date"), "fieldname": "request_date_created", "fieldtype": "Date", "width": 150},
		{"label": _("Request Time"), "fieldname": "request_time_created", "fieldtype": "Time", "width": 150},
		{
			"label": _("Further Information"),
			"fieldname": "further_information",
			"fieldtype": "Small Text",
			"width": 280,
		},
	]


def get_conditions(filters):
	conditions = []
	if filters.get("status"):
		conditions.append("status = %(status)s")
	if filters.get("priority_level"):
		conditions.append("priority_level = %(priority_level)s")
	if filters.get("location"):
		conditions.append("location = %(location)s")
	if filters.get("request_date_created"):
		conditions.append("request_date_created >= %(request_date_created)s")
	if filters.get("request_time_created"):
		conditions.append("request_time_created >= %(request_time_created)s")

	return " AND ".join(conditions) if conditions else "1=1"
