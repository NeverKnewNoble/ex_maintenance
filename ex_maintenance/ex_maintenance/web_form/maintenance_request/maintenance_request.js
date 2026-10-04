// Link fields become plain autocompletes on web forms (listing every record), so the
// enabled locations and each location's issues are loaded from the app instead.

frappe.ready(async () => {
	const { message: options } = await frappe.call({
		method: "ex_maintenance.api.locations.get_request_options",
	});

	frappe.web_form.fields_dict.location.set_data(options.locations);

	const refresh = () => apply_location(options);
	frappe.web_form.on("location", refresh);
	refresh();
});

function apply_location(options) {
	const location = frappe.web_form.get_value("location");
	const needs_room = options.requires_room_number.includes(location);

	frappe.web_form.set_df_property("room_number", "hidden", needs_room ? 0 : 1);
	frappe.web_form.set_df_property("room_number", "reqd", needs_room ? 1 : 0);
	frappe.web_form.set_df_property("other", "hidden", location === "Other" ? 0 : 1);

	const issues = options.issues[location] || options.all_issues;
	frappe.web_form.fields_dict.table_umyd.grid.update_docfield_property(
		"issue_type",
		"options",
		issues
	);
}
