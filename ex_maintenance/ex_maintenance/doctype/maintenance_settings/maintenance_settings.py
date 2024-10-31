# Copyright (c) 2024, Nortex and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceSettings(Document):
    pass

# ! Toggle Notification On/Off
@frappe.whitelist()
def toggle_notification(notification_title, enabled):
    try:
        # Fetch the specific notification by title
        notification = frappe.get_all(
            "Notification",
            filters={"name": notification_title},
            limit=1
        )

        if notification:
            # Enable or disable the found notification
            notification_doc = frappe.get_doc("Notification", notification[0].name)
            notification_doc.enabled = enabled  # Set based on the argument
            notification_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return "success"
        else:
            frappe.log_error(f"Notification with title '{notification_title}' not found.")
            return "error"
    except Exception as e:
        frappe.log_error(f"Error toggling notification: {str(e)}")
        return "error"

