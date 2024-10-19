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


