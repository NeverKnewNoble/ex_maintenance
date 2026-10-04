import frappe


def get_location_filters():
	"""Enabled locations for the facility type chosen in Maintenance Settings (plus General ones)."""
	filters = {"disabled": 0}
	facility_type = frappe.db.get_single_value("Maintenance Settings", "facility_type") or "All"
	if facility_type != "All":
		filters["facility_type"] = ["in", [facility_type, "General"]]
	return filters


def get_location_issues(location):
	"""Issues listed on the location; an empty list means any issue may be picked."""
	if not location:
		return []
	return frappe.get_all(
		"Maintenance Location Issue",
		filters={"parenttype": "Maintenance Location", "parent": location},
		pluck="issue",
		order_by="idx asc",
	)


# ! Link field queries for the desk forms
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def search_locations(doctype, txt, searchfield, start, page_len, filters):
	return frappe.get_all(
		"Maintenance Location",
		filters=get_location_filters(),
		or_filters={"name": ["like", f"%{txt}%"], "facility_type": ["like", f"%{txt}%"]} if txt else None,
		fields=["name", "facility_type"],
		order_by="name asc",
		limit_start=start,
		limit_page_length=page_len,
		as_list=True,
	)


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def search_location_issues(doctype, txt, searchfield, start, page_len, filters):
	issue_filters = {"disabled": 0}
	if txt:
		issue_filters["name"] = ["like", f"%{txt}%"]

	location_issues = get_location_issues((filters or {}).get("location"))
	if location_issues:
		issue_filters["name"] = ["in", [i for i in location_issues if txt.lower() in i.lower()] or [""]]

	return frappe.get_all(
		"Maintenance Issue",
		filters=issue_filters,
		order_by="name asc",
		limit_start=start,
		limit_page_length=page_len,
		as_list=True,
	)


# ! Options for the public Maintenance Request web form (submitted as Guest).
# Only location and issue names are exposed; both are already visible on the form.
@frappe.whitelist(allow_guest=True)
def get_request_options():
	locations = frappe.get_all(
		"Maintenance Location",
		filters=get_location_filters(),
		fields=["name", "requires_room_number"],
		order_by="name asc",
	)
	names = [location.name for location in locations]

	issues = {}
	if names:
		for row in frappe.get_all(
			"Maintenance Location Issue",
			filters={"parenttype": "Maintenance Location", "parent": ["in", names]},
			fields=["parent", "issue"],
			order_by="idx asc",
		):
			issues.setdefault(row.parent, []).append(row.issue)

	return {
		"locations": names,
		"requires_room_number": [location.name for location in locations if location.requires_room_number],
		"issues": issues,
		"all_issues": frappe.get_all(
			"Maintenance Issue", filters={"disabled": 0}, pluck="name", order_by="name asc"
		),
	}
