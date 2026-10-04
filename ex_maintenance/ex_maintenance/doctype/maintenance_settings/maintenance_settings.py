# Copyright (c) 2024, Nortex and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class MaintenanceSettings(Document):
	# Each standard Notification of this app has a condition that reads these checkboxes
	# (send_system_message / send_email / send_sms), so nothing needs toggling here.
	pass
