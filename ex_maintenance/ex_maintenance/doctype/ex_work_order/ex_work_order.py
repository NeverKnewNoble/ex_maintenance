
import frappe
from frappe.model.document import Document

class ExWorkOrder(Document):
    pass



# ! Function To assign Task to employees and create a New task Assignment Document
@frappe.whitelist()
def create_task_assignment(ex_work_order):
    try:
        if isinstance(ex_work_order, str):
            ex_work_order = frappe.parse_json(ex_work_order)

        name = ex_work_order.get("name")
        task_assignment_reference = ex_work_order.get("task_assignment_reference")
        priority_level = ex_work_order.get('priority_level')
        status = ex_work_order.get('status')
        deadline_date = ex_work_order.get('deadline_date')
        deadline_time = ex_work_order.get('deadline_time')
        request_code = ex_work_order.get('request_code')
        assign_task = ex_work_order.get('assign_task', [])
        user = ex_work_order.get('assign_task.employee')

        # If task_assignment_reference is empty, create new assignments
        if not task_assignment_reference:
            for task in assign_task:
                instructions = task.get('instructions')
                employee_user = task.get('employee')

                if instructions and employee_user:
                    task_assignment = frappe.get_doc({
                        'doctype': 'Task Assignments',
                        'priority': priority_level,
                        'status': status,
                        'instructions': instructions,
                        'deadline_set_date': deadline_date,
                        'deadline_set_time': deadline_time,
                        'request_code': request_code,
                        'doc_reference': name,
                        'assignee': employee_user,
                        'issue': []
                    })

                    if ex_work_order.get('issue'):
                        for item in ex_work_order.get('issue'):
                            task_assignment.append('issue', {
                                'issue_type': item.get('issue_type'),
                                'description': item.get('description')
                            })

                    task_assignment.insert(ignore_permissions=True)

                    # Update the task_assignment_reference field for tracking
                    frappe.db.set_value('Ex Work Order', name, 'task_assignment_reference', task_assignment.name)

                    # Assign to individual user
                    frappe.desk.form.assign_to.add({
                        'assign_to': [employee_user],
                        'doctype': 'Task Assignments',
                        'name': task_assignment.name,
                        'description': f"Assigned task based on instructions: {instructions}",
                        'notify': 1
                    })
        else:
            # Update the existing Task Assignment
            task_assignment = frappe.get_doc("Task Assignments", task_assignment_reference)
            task_assignment.priority = priority_level
            task_assignment.status = status
            task_assignment.deadline_set_date = deadline_date
            task_assignment.deadline_set_time = deadline_time
            task_assignment.request_code = request_code
            task_assignment.set("issue", [])

            if ex_work_order.get('issue'):
                for item in ex_work_order.get('issue'):
                    task_assignment.append('issue', {
                        'issue_type': item.get('issue_type'),
                        'description': item.get('description')
                    })

            task_assignment.save(ignore_permissions=True)

    except Exception as e:
        frappe.log_error(f"Error creating/updating Task Assignment: {str(e)}")
        frappe.msgprint(f"Error: {str(e)}")
        return str(e)






#  ! Function to assign Task to the Team and create a New task Assignment Document
# @frappe.whitelist()
# def assign_to_team(ex_work_order):
#     try:
#         # Deserialize the input if it's passed as a JSON string
#         if isinstance(ex_work_order, str):
#             ex_work_order = frappe.parse_json(ex_work_order)  # Convert to a Python dictionary if it's a string

#         # Check if 'is_a_team' is true
#         is_a_team = ex_work_order.get('is_a_team', False)

#         if is_a_team:
#             # Get the team instructions directly from the Ex Work Order field
#             team_descriptioninstructions = ex_work_order.get('team_descriptioninstructions')

#             # Get all users with the "Ex Maintenance Team Member" role
#             team_members = frappe.get_all(
#                 "Has Role",
#                 filters={"role": "Ex Maintenance Team Member"},
#                 fields=["parent"]
#             )

#             # Check if the expected fields are present
#             priority_level = ex_work_order.get('priority_level')
#             status = ex_work_order.get('status')
#             deadline_date = ex_work_order.get('deadline_date')
#             deadline_time = ex_work_order.get('deadline_time')
#             request_code = ex_work_order.get('request_code')


#             if team_descriptioninstructions and team_members:
#                 # ? Create the new Task Assignments document using the team instructions
#                 task_assignment = frappe.get_doc({
#                     'doctype': 'Task Assignments',
#                     'priority': priority_level,
#                     'status': status,
#                     'instructions': team_descriptioninstructions,
#                     'deadline_set_date': deadline_date,
#                     'deadline_set_time': deadline_time,
#                     'request_code': request_code, 
#                     'issue': [] 
#                 })


#                 # ? Iterate over the child table of issue and get its content and apply to array
#                 if ex_work_order.issue:
#                     for item in ex_work_order.get('issue', []):
#                         # Append each issue in the child table to the Work Order's issue field
#                         task_assignment.append('issue', {
#                             'issue_type': item.get('issue_type'),
#                             'description': item.get('description')
#                         })


#                 # ? Save the new Task Assignments document (as draft)
#                 task_assignment.insert(ignore_permissions=True)

#                 # Assign to all team members
#                 for member in team_members:
#                     frappe.desk.form.assign_to.add({
#                         'assign_to': [member['parent']],
#                         'doctype': 'Task Assignments',
#                         'name': task_assignment.name,
#                         'description': f"Assigned task to team: {team_descriptioninstructions}",
#                         'notify': 1  # Send email notification to each assigned user
#                     })

#     except Exception as e:
#         frappe.log_error(f"Error creating Task Assignment for team: {str(e)}")
#         frappe.msgprint(f"Error: {str(e)}")
#         return str(e)



@frappe.whitelist()
def assign_to_team(ex_work_order):
    try:
        if isinstance(ex_work_order, str):
            ex_work_order = frappe.parse_json(ex_work_order)

        name = ex_work_order.get("name")
        task_assignment_reference = ex_work_order.get("task_assignment_reference")
        is_a_team = ex_work_order.get('is_a_team', False)
        priority_level = ex_work_order.get('priority_level')
        status = ex_work_order.get('status')
        deadline_date = ex_work_order.get('deadline_date')
        deadline_time = ex_work_order.get('deadline_time')
        request_code = ex_work_order.get('request_code')
        team_descriptioninstructions = ex_work_order.get('team_descriptioninstructions')

        if is_a_team:
            team_members = frappe.get_all(
                "Has Role",
                filters={"role": "Ex Maintenance Team Member"},
                fields=["parent"]
            )

            # If task_assignment_reference is empty, create a new Task Assignment
            if not task_assignment_reference:
                task_assignment = frappe.get_doc({
                    'doctype': 'Task Assignments',
                    'priority': priority_level,
                    'status': status,
                    'instructions': team_descriptioninstructions,
                    'deadline_set_date': deadline_date,
                    'deadline_set_time': deadline_time,
                    'request_code': request_code,
                    'doc_reference': name,
                    'issue': []
                })

                if ex_work_order.get('issue'):
                    for item in ex_work_order.get('issue'):
                        task_assignment.append('issue', {
                            'issue_type': item.get('issue_type'),
                            'description': item.get('description')
                        })

                task_assignment.insert(ignore_permissions=True)

                # Save the new Task Assignment reference in Ex Work Order
                frappe.db.set_value('Ex Work Order', name, 'task_assignment_reference', task_assignment.name)

                # Assign to all team members
                for member in team_members:
                    frappe.desk.form.assign_to.add({
                        'assign_to': [member['parent']],
                        'doctype': 'Task Assignments',
                        'name': task_assignment.name,
                        'description': f"Assigned task to team: {team_descriptioninstructions}",
                        'notify': 1
                    })
            else:
                # Update the existing Task Assignment
                task_assignment = frappe.get_doc("Task Assignments", task_assignment_reference)
                task_assignment.priority = priority_level
                task_assignment.status = status
                task_assignment.instructions = team_descriptioninstructions
                task_assignment.deadline_set_date = deadline_date
                task_assignment.deadline_set_time = deadline_time
                task_assignment.request_code = request_code
                task_assignment.set("issue", [])

                if ex_work_order.get('issue'):
                    for item in ex_work_order.get('issue'):
                        task_assignment.append('issue', {
                            'issue_type': item.get('issue_type'),
                            'description': item.get('description')
                        })

                task_assignment.save(ignore_permissions=True)

    except Exception as e:
        frappe.log_error(f"Error creating/updating Task Assignment for team: {str(e)}")
        frappe.msgprint(f"Error: {str(e)}")
        return str(e)








# ! Function to create Response Time doc 
@frappe.whitelist()
def response(ex_request):
    try:
        # Ensure ex_request is a dictionary if it's not already a Frappe document
        if isinstance(ex_request, str):
            ex_request = frappe.parse_json(ex_request)

        # Create the new Response document
        response_order = frappe.get_doc({
            'doctype': 'Response Time',
            'management_document': ex_request.get('name'),
            'request_document': ex_request.get('request_code'),
        })

        # Save the new Work Order (as draft)
        response_order.insert()


    except Exception as e:
        frappe.log_error(f"Error creating Response Time Updated: {str(e)}")
        frappe.msgprint(f"Error: {str(e)}")
        return str(e)
