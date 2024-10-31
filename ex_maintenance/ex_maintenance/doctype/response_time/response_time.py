import frappe
from frappe.model.document import Document
from frappe.utils import time_diff_in_seconds
from datetime import datetime, time, timedelta  # Added 'timedelta'

class ResponseTime(Document):
    pass

# Function to calculate the average response time
@frappe.whitelist()
def calculate_average_response_time():
    # Get all records from the "Response Time" doctype with the relevant fields
    all_docs = frappe.get_all('Response Time', fields=['request_date', 'request_time', 'completed_date', 'completed_time'])

    total_time_diff = 0
    count = 0

    # Loop through each document and calculate the time difference
    for doc in all_docs:
        if doc.request_date and doc.completed_date and doc.request_time and doc.completed_time:
            # Ensure request_time and completed_time are of type datetime.time
            if isinstance(doc.request_time, timedelta):
                doc.request_time = (datetime.min + doc.request_time).time()
            if isinstance(doc.completed_time, timedelta):
                doc.completed_time = (datetime.min + doc.completed_time).time()

            # Combine dates and times into full datetime objects
            request_datetime = datetime.combine(doc.request_date, doc.request_time)
            completed_datetime = datetime.combine(doc.completed_date, doc.completed_time)

            # Calculate the time difference in seconds
            time_diff = time_diff_in_seconds(completed_datetime, request_datetime)
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
