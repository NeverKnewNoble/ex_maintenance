// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ex Requests", {
	setup(frm) {
		// Only enabled locations for the facility type in Maintenance Settings
		frm.set_query("location", () => ({
			query: "ex_maintenance.api.locations.search_locations",
		}));

		// Issues listed on the chosen location (any issue if the location lists none)
		frm.set_query("issue_type", "table_umyd", () => ({
			query: "ex_maintenance.api.locations.search_location_issues",
			filters: { location: frm.doc.location },
		}));
	},

	refresh(frm) {
		// ? The Work Order is created on the server when the request is inserted
		if (!frm.is_new()) {
			frm.add_custom_button(__("View Work Order"), () => {
				frappe.set_route("List", "Ex Work Order", { request_code: frm.doc.name });
			});
		}
	},
});
