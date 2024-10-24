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

