// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt

frappe.ui.form.on("Task Assignments", {
	refresh(frm) {
		if (frm.is_new() || !frm.doc.doc_reference) return;

		frm.add_custom_button(__("Update Linked Document"), () => {
			frappe.call({
				method: "ex_maintenance.ex_maintenance.doctype.task_assignments.task_assignments.update_linked_document",
				args: {
					doc_reference: frm.doc.doc_reference,
					task_status: frm.doc.task_status,
					description_on_the_task: frm.doc.description_on_the_task,
					attach_work_progress: frm.doc.attach_work_progress || "",
				},
				freeze: true,
				callback(r) {
					if (r.message === "success") {
						frappe.show_alert({
							message: __("The linked document has been updated successfully."),
							indicator: "green",
						});
						frm.reload_doc();
					}
				},
			});
		}).addClass("btn-primary");
	},
});
