// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt

// Completion time, Task Assignments and Response Time are handled on the server
// (ExWorkOrder.validate / on_update), so saving the form is enough.

frappe.ui.form.on("Ex Work Order", {
	refresh(frm) {
		if (frm.is_new() || frm.doc.status === "Open") return;

		frm.add_custom_button(__("Reopen and Reassign Task"), () => {
			frappe.call({
				method: "ex_maintenance.ex_maintenance.doctype.ex_work_order.ex_work_order.reopen_and_assign_to_both_tasks",
				args: { ex_work_order_name: frm.doc.name },
				freeze: true,
				callback(r) {
					if (!r.exc) {
						frappe.show_alert({
							message: __("The task has been reopened and reassigned."),
							indicator: "green",
						});
						frm.reload_doc();
					}
				},
			});
		}).addClass("btn-primary");
	},
});
