// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt


//  !
frappe.ui.form.on('Task Assignments', {
    refresh: function(frm) {
        frm.add_custom_button(__('Update Linked Document'), function() {
            if (!frm.doc.doc_reference) {
                frappe.msgprint(__('Please specify a document reference.'));
                return;
            }

            // Call the server-side function to update the linked document
            frappe.call({
                method: 'ex_maintenance.ex_maintenance.doctype.task_assignments.task_assignments.update_linked_document',
                args: {
                    doc_reference: {
                        doctype: "Ex Work Order",
                        name: frm.doc.doc_reference
                    },
                    task_status: frm.doc.task_status,
                    description_on_the_task: frm.doc.description_on_the_task,
                    attach_work_progress: frm.doc.attach_work_progress || ""
                },
                callback: function(response) {
                    if (response.message === 'success' || response.message === 'success (DB update)') {
                        frappe.msgprint(__('The linked document has been updated successfully.'));
                    } else {
                        frappe.msgprint(__('Failed to update the linked document.'));
                    }
                }
            });
        }).addClass('btn-primary');
    }
});








