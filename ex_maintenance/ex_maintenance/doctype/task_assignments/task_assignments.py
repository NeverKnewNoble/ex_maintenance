# Copyright (c) 2024, Nortex and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from frappe.utils import now, now_datetime


class TaskAssignments(Document):
    pass


#  ! Function To Update The Work Order For The Manager On Task Progress
# @frappe.whitelist()
# def update_linked_document(doc_reference, task_status, description_on_the_task, attach_work_progress=None):
#     try:
#         # Convert doc_reference from JSON string to dictionary if necessary
#         if isinstance(doc_reference, str):
#             doc_reference = json.loads(doc_reference)

#         # Prepare the field values to update
#         update_fields = {
#             'status': task_status,
#             'description_on_the_task': description_on_the_task,
#             'attach_image_rypl': attach_work_progress or ""
#         }

#         # Check if status is 'Completed' and set date and time accordingly
#         if task_status == 'Completed':
#             update_fields['completed_date'] = frappe.utils.nowdate()
#             update_fields['request_completed_time'] = frappe.utils.nowtime()
#         else:
#             # Clear the date and time if status is not 'Completed'
#             update_fields['completed_date'] = None
#             update_fields['request_completed_time'] = None

#         # Perform the update directly in the database
#         frappe.db.set_value(doc_reference['doctype'], doc_reference['name'], update_fields)

#         # Commit the changes to the database
#         frappe.db.commit()

#         frappe.log_error("Document updated directly using DB update", "Update Linked Document")
#         return "success"

#     except Exception as e:
#         # Log error if something goes wrong
#         frappe.log_error(f"Error during direct DB update: {str(e)}", "Update Linked Document - Error")
#         return "error"




@frappe.whitelist()
def update_linked_document(doc_reference, task_status, description_on_the_task, attach_work_progress=None):
    try:
        # Convert doc_reference from JSON string to dictionary if necessary
        if isinstance(doc_reference, str):
            doc_reference = json.loads(doc_reference)

        # Prepare the field values to update
        update_fields = {
            'status': task_status,
            'description_on_the_task': description_on_the_task,
            'attach_image_rypl': attach_work_progress or ""
        }

        # Check if status is 'Completed' and set date and time accordingly
        if task_status == 'Completed':
            update_fields['completed_date'] = frappe.utils.nowdate()
            update_fields['request_completed_time'] = frappe.utils.nowtime()
        else:
            # Clear the date and time if status is not 'Completed'
            update_fields['completed_date'] = None
            update_fields['request_completed_time'] = None

        # Fetch current status change logs and add a new entry
        current_logs = frappe.db.get_value(doc_reference['doctype'], doc_reference['name'], 'status_change_logs') or ""
        user = frappe.session.user
        timestamp = frappe.utils.format_datetime(now_datetime(), "MMM dd, yyyy hh:mm a")
        new_log_entry = f"{user} updated this document on {timestamp}"

        # Append new log entry to the existing logs
        updated_logs = f"{current_logs}\n{new_log_entry}" if current_logs else new_log_entry
        update_fields['status_change_logs'] = updated_logs

        # Perform the update directly in the database
        frappe.db.set_value(doc_reference['doctype'], doc_reference['name'], update_fields)

        # Commit the changes to the database
        frappe.db.commit()

        frappe.log_error("Document updated directly using DB update", "Update Linked Document")
        return "success"

    except Exception as e:
        # Log error if something goes wrong
        frappe.log_error(f"Error during direct DB update: {str(e)}", "Update Linked Document - Error")
        return "error"
