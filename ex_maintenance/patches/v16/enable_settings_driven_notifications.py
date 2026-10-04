import frappe

# These now read Maintenance Settings in their condition instead of being toggled on/off.
# `enabled` is not overwritten when standard notifications are synced, so set it once here.
NOTIFICATIONS = (
	"MainReq",
	"MainReq (Email)",
	"Maintenance Request SMS",
	"Maintenance Task Assigned",
	"TaskAss (Email)",
	"TaskAss (SMS)",
)


def execute():
	for name in NOTIFICATIONS:
		if frappe.db.exists("Notification", name):
			frappe.db.set_value("Notification", name, "enabled", 1, update_modified=False)
