import frappe

from ex_maintenance.setup.default_locations import DEFAULT_LOCATIONS


def after_install():
	create_default_locations()


def create_default_locations():
	"""Create the default locations and their issues; existing records are left untouched."""
	for location in DEFAULT_LOCATIONS:
		for issue in location["issues"]:
			ensure_issue(issue)

		if frappe.db.exists("Maintenance Location", location["location_name"]):
			continue

		doc = frappe.new_doc("Maintenance Location")
		doc.update(
			{
				"location_name": location["location_name"],
				"facility_type": location["facility_type"],
				"requires_room_number": location["requires_room_number"],
			}
		)
		doc.set("issues", [{"issue": issue} for issue in location["issues"]])
		doc.insert(ignore_permissions=True)


def ensure_location(name, **values):
	if name and not frappe.db.exists("Maintenance Location", name):
		frappe.get_doc({"doctype": "Maintenance Location", "location_name": name, **values}).insert(
			ignore_permissions=True
		)


def ensure_issue(name):
	if name and not frappe.db.exists("Maintenance Issue", name):
		frappe.get_doc({"doctype": "Maintenance Issue", "issue_name": name}).insert(ignore_permissions=True)
