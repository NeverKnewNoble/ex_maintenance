import frappe

# Standard records removed from the app; delete them from existing sites too
OBSOLETE_NOTIFICATIONS = ("Test", "Maintenance Request", "Maintenance request (Email)")


def execute():
	for name in OBSOLETE_NOTIFICATIONS:
		if frappe.db.get_value("Notification", {"name": name, "module": "Ex Maintenance"}):
			frappe.delete_doc("Notification", name, force=True, ignore_permissions=True)
