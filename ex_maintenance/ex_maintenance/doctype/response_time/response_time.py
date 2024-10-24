
import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_seconds

class ResponseTime(Document):
    pass

# ! To calculate the average response time 
@frappe.whitelist()
def calculate_average_response_time():
    # Get all records from the "Response Time" doctype with request_time and completed_time fields
    all_docs = frappe.get_all('Response Time', fields=['request_time', 'completed_time'])

    total_time_diff = 0
    count = 0

    # Loop through each document and calculate the time difference
    for doc in all_docs:
        if doc.request_time and doc.completed_time:
            # Calculate the time difference in seconds
            time_diff = time_diff_in_seconds(doc.completed_time, doc.request_time)
            total_time_diff += time_diff
            count += 1

    # Calculate the average time difference in seconds
    if count > 0:
        average_time_diff_in_seconds = total_time_diff / count
    else:
        average_time_diff_in_seconds = 0

    # Determine the unit based on the average time difference
    if average_time_diff_in_seconds < 60:
        # Display in seconds if less than 60 seconds
        return f"{average_time_diff_in_seconds:.2f} seconds"
    elif average_time_diff_in_seconds < 3600:
        # Display in minutes if less than 60 minutes
        average_time_diff_in_minutes = average_time_diff_in_seconds / 60
        return f"{average_time_diff_in_minutes:.2f} minutes"
    else:
        # Display in hours if more than 60 minutes
        average_time_diff_in_hours = average_time_diff_in_seconds / 3600
        return f"{average_time_diff_in_hours:.2f} hours"
