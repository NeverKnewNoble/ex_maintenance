import frappe
from frappe import _
from ex_maintenance.ex_maintenance.doctype.ex_work_order.ex_work_order import create_task_assignment, assign_to_team
from frappe.utils import nowdate, nowtime, now_datetime, format_datetime
import json


#  ! Function TO Display all data from the Doctpye to the app
@frappe.whitelist(allow_guest=True)
def get_all_ex_work_orders():
    # Define the fields to fetch from the main document
    fields_to_fetch = [
        "name", "location", "request_code", "room_number", "other",
        "image", "date", "time", "further_information", "priority_level",
        "status", "is_a_team", "team_descriptioninstructions", "is_an_indvidual",
        "deadline_date", "deadline_time", "status_change_logs"
    ]
    
    try:
        # Fetch all Ex Work Order documents with the specified fields
        ex_work_orders = frappe.get_all('Ex Work Order', fields=fields_to_fetch)
        
        # For each work order, fetch the related Issue and Assign Task table entries
        for work_order in ex_work_orders:
            # Fetch issues related to this work order
            issues = frappe.get_all(
                'Ex Issue Type',  # Replace with the correct doctype name of the Issue child table
                filters={'parent': work_order['name']},
                fields=['idx', 'issue_type', 'description']  # Fields in the Issue table
            )
            work_order['issues'] = issues  # Add issues data to the work order document
            
            # Fetch assign tasks related to this work order
            assign_tasks = frappe.get_all(
                'Ex Task Assignment',  # Replace with the correct doctype name of the Assign Task child table
                filters={'parent': work_order['name']},
                fields=['idx', 'employee', 'instructions'] 
            )
            work_order['assign_task'] = assign_tasks  
            
        return {"data": ex_work_orders}
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error fetching Ex Work Order documents")
        return {"error": str(e)}




#  ! Function TO display Doctype List view into app
@frappe.whitelist(allow_guest=True)
def ex_work_ui():
    # Fetch all "Ex Work Order" documents
    try:
        ex_work_orders = frappe.get_all('Ex Work Order', fields=["name","date", "status", "priority_level"])  
        return {"data": ex_work_orders}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error fetching Ex Work Order documents")
        return {"error": str(e)}
    



# ! Function to Update the Doctype from the app
@frappe.whitelist(allow_guest=True)
def update_and_assign_ex_work_order(data):
    try:
        # Parse JSON input if it's a string
        if isinstance(data, str):
            data = frappe.parse_json(data)

        # Extract necessary data
        doc_name = data.get("name")
        priority_level = data.get("priority_level")
        status = data.get("status")
        is_a_team = data.get("is_a_team", 0)
        team_descriptioninstructions = data.get("team_descriptioninstructions")
        is_an_indvidual = data.get("is_an_indvidual", 0)
        deadline_date = data.get("deadline_date")
        deadline_time = data.get("deadline_time")
        assign_task = data.get("assign_task", [])  # List of task assignments

        # Debugging: Log received data to verify structure
        frappe.log_error(f"Received data for update: {data}", "Update and Assign Ex Work Order")

        # Fetch the Ex Work Order document
        ex_work_order = frappe.get_doc("Ex Work Order", doc_name)

        # Update fields in the Ex Work Order document
        ex_work_order.priority_level = priority_level
        ex_work_order.status = status
        ex_work_order.is_a_team = is_a_team
        ex_work_order.team_descriptioninstructions = team_descriptioninstructions
        ex_work_order.is_an_indvidual = is_an_indvidual
        ex_work_order.deadline_date = deadline_date
        ex_work_order.deadline_time = deadline_time

        # Update completion date and time if status is 'Completed'
        if status == 'Completed':
            ex_work_order.completed_date = nowdate()
            ex_work_order.request_completed_time = nowtime()
        else:
            ex_work_order.completed_date = None
            ex_work_order.request_completed_time = None


        # Clear existing assign tasks to update with new data
        ex_work_order.assign_task = []

        for task in assign_task:
            ex_work_order.append("assign_task", {
                "employee": task.get("employee"),
                "instructions": task.get("instructions")
            })

        # Save updates to Ex Work Order
        ex_work_order.save(ignore_permissions=True)

        # Log success message
        frappe.log_error("Ex Work Order updated with new data", "Update and Assign Ex Work Order")

        return {
            "status": "success",
            "message": _("Ex Work Order updated and assigned successfully.")
        }
    except Exception as e:
        # Log any errors for debugging
        frappe.log_error(f"Error during update: {str(e)}", "Update and Assign Ex Work Order - Error")
        return {"status": "error", "message": str(e)}


# ! Function to get all Users
@frappe.whitelist(allow_guest=True)
def get_user_emails():
    # Query to get all active user emails
    user_emails = frappe.get_all("User", filters={"enabled": 1}, fields=["email"])
    
    # Extract email addresses from the result
    emails = [user["email"] for user in user_emails if user["email"]]
    return emails




#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.orderview.get_all_ex_work_orders
#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.orderview.ex_work_ui
#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.orderview.update_and_assign_ex_work_order
#  http://127.0.0.1:8001/api/v2/method/ex_maintenance.api.orderview.get_user_emails