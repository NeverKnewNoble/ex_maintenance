
import frappe
from frappe.model.document import Document

class ExWorkOrder(Document):
    pass



# ! Function To assign Task to employees and create a New task Assignment Document
@frappe.whitelist()
def create_task_assignment(ex_work_order):
    try:
        # Deserialize the input if it's passed as a JSON string
        if isinstance(ex_work_order, str):
            ex_work_order = frappe.parse_json(ex_work_order)  # Convert to a Python dictionary if it's a string

        # Check if the expected fields are present
        priority_level = ex_work_order.get('priority_level')
        status = ex_work_order.get('status')
        deadline_date = ex_work_order.get('deadline_date')
        deadline_time = ex_work_order.get('deadline_time')
        assign_task = ex_work_order.get('assign_task', [])

        # ? Iterate over the child table (assign_task) in Ex Work Order, if it exists
        if assign_task:
            for task in assign_task:
                # Retrieve instructions and employee from each row in the assign_task table
                instructions = task.get('instructions')
                employee_user = task.get('employee')  # Assuming 'employee' holds the user ID or email

                if instructions and employee_user:
                    # ? Create the new Task Assignments document for each instruction
                    task_assignment = frappe.get_doc({
                        'doctype': 'Task Assignments',
                        'priority': priority_level,
                        'status': status,
                        'instructions': instructions,
                        'deadline_set_date': deadline_date,
                        'deadline_set_time': deadline_time,
                    })

                    # ? Save the new Task Assignments document (as draft)
                    task_assignment.insert(ignore_permissions=True)

                    # Use Frappe's "assign to" feature to assign the document to the user
                    frappe.desk.form.assign_to.add({
                        'assign_to': [employee_user],
                        'doctype': 'Task Assignments',
                        'name': task_assignment.name,
                        'description': f"Assigned task based on instructions: {instructions}",
                        'notify': 1  # Send email notification to the assigned user
                    })

        frappe.msgprint("Task Assignment(s) created and assigned successfully!")
        return "Task Assignment(s) created and assigned successfully!"

    except Exception as e:
        frappe.log_error(f"Error creating Task Assignment: {str(e)}")
        frappe.msgprint(f"Error: {str(e)}")
        return str(e)



#  ! Function to assign Task to the Team and create a New task Assignment Document
@frappe.whitelist()
def assign_to_team(ex_work_order):
    try:
        # Deserialize the input if it's passed as a JSON string
        if isinstance(ex_work_order, str):
            ex_work_order = frappe.parse_json(ex_work_order)  # Convert to a Python dictionary if it's a string

        # Check if 'is_a_team' is true
        is_a_team = ex_work_order.get('is_a_team', False)

        if is_a_team:
            # Get the team instructions directly from the Ex Work Order field
            team_descriptioninstructions = ex_work_order.get('team_descriptioninstructions')

            # Get all users with the "Ex Maintenance Team Member" role
            team_members = frappe.get_all(
                "Has Role",
                filters={"role": "Ex Maintenance Team Member"},
                fields=["parent"]
            )

            # Check if the expected fields are present
            priority_level = ex_work_order.get('priority_level')
            status = ex_work_order.get('status')
            deadline_date = ex_work_order.get('deadline_date')
            deadline_time = ex_work_order.get('deadline_time')

            if team_descriptioninstructions and team_members:
                # ? Create the new Task Assignments document using the team instructions
                task_assignment = frappe.get_doc({
                    'doctype': 'Task Assignments',
                    'priority': priority_level,
                    'status': status,
                    'instructions': team_descriptioninstructions,
                    'deadline_set_date': deadline_date,
                    'deadline_set_time': deadline_time,
                })

                # ? Save the new Task Assignments document (as draft)
                task_assignment.insert(ignore_permissions=True)

                # Assign to all team members
                for member in team_members:
                    frappe.desk.form.assign_to.add({
                        'assign_to': [member['parent']],
                        'doctype': 'Task Assignments',
                        'name': task_assignment.name,
                        'description': f"Assigned task to team: {team_descriptioninstructions}",
                        'notify': 1  # Send email notification to each assigned user
                    })

        frappe.msgprint("Task Assignment(s) created and assigned to the team successfully!")
        return "Task Assignment(s) created and assigned to the team successfully!"

    except Exception as e:
        frappe.log_error(f"Error creating Task Assignment for team: {str(e)}")
        frappe.msgprint(f"Error: {str(e)}")
        return str(e)
