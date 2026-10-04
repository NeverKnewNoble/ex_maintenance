import frappe

from ex_maintenance.setup.install import create_default_locations, ensure_issue, ensure_location


def execute():
	"""Location and issue fields became Links: create the defaults, plus a record for every
	value already used so existing requests, work orders and tasks keep valid links."""
	create_default_locations()

	for doctype in ("Ex Requests", "Ex Work Order", "Task Assignments"):
		for location in frappe.get_all(
			doctype, filters={"location": ["is", "set"]}, pluck="location", distinct=True
		):
			ensure_location(location, requires_room_number=int(location == "Guest Room"))

	for issue in frappe.get_all(
		"Ex Issue Type", filters={"issue_type": ["is", "set"]}, pluck="issue_type", distinct=True
	):
		ensure_issue(issue)
