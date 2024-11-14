// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt


frappe.ui.form.on("Ex Work Order", {
// ! Function to call current data and time when order is completed
    status: function(frm) {
        // Check if the status is 'Completed'
        if (frm.doc.status === 'Completed') {
            // ? Set the current date and time if the status is 'Completed'
            frm.set_value('completed_date', frappe.datetime.now_date());
            frm.set_value('request_completed_time', frappe.datetime.now_time());
        } else {
            // ? Clear the date and time fields if status is changed from 'Completed' to something else
            frm.set_value('completed_date', null);
            frm.set_value('request_completed_time', null);
        }
    }
});


// ! On save, it calls the assign to individual function
frappe.ui.form.on('Ex Work Order', {
    after_save: function(frm) {
        frappe.call({
            method: 'ex_maintenance.ex_maintenance.doctype.ex_work_order.ex_work_order.create_task_assignment',
            args: {
                ex_work_order: frm.doc  // This will pass the form data as an object
            },
            callback: function(response) {
                if (response.message) {
                    frappe.msgprint(__('Task Assignment(s) created successfully.'));
                }
            }
        });
    }
});


// ! On save, it calls the assign to Team function
frappe.ui.form.on('Ex Work Order', {
    after_save: function(frm) {
        if (frm.doc.is_a_team) {
            frappe.call({
                method: 'ex_maintenance.ex_maintenance.doctype.ex_work_order.ex_work_order.assign_to_team',
                args: {
                    ex_work_order: frm.doc  // This will pass the form data as an object
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(__('Task Assignment(s) created and assigned to the team successfully.'));
                    }
                }
            });
        }
    }
});


frappe.ui.form.on("Ex Work Order", {
    // ! Function to call response code when order is completed
    after_save: function(frm) {
        // Check if the status is 'Completed'
        if (frm.doc.status === 'Completed') {
            frappe.call({
                method: 'ex_maintenance.ex_maintenance.doctype.ex_work_order.ex_work_order.response',  // Corrected method name
                args: {
                    ex_request: frm.doc  // Pass the form data as an object
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(__('Response time updated successfully!'));
                    }
                }
            });
        }
    }
});

    
// !
frappe.ui.form.on('Ex Work Order', {
    refresh: function(frm) {
        // Add a custom button to reopen and reassign the task
        frm.add_custom_button(__('Reopen and Reassign Task'), function() {
            frappe.call({
                method: "ex_maintenance.ex_maintenance.doctype.ex_work_order.ex_work_order.reopen_and_assign_to_both_tasks",
                args: {
                    ex_work_order_name: frm.doc.name
                },
                callback: function(response) {
                    if (!response.exc) {
                        frappe.msgprint(__('The task has been reopened and reassigned successfully.'));
                        frm.reload_doc(); // Refresh the document to reflect the updated status
                    }
                }
            });
        }).addClass('btn-primary');
    }
});
