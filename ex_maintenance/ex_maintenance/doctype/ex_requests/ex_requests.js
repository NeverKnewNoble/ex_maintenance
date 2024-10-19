// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt

// ? Function to get request time
frappe.ui.form.on("Ex Requests", {
    refresh(frm) {
        if (frm.is_new()) {
            frm.set_value('request_time', frappe.datetime.now_time());
        }
    },
}); 


//  ? Function to call python function 
frappe.ui.form.on('Ex Requests', {
    onload(frm) {
        frm.add_custom_button('Create Work Order', function() {
            console.log('Create Work Order button clicked');

            frappe.call({
                method: 'ex_maintenance.ex_maintenance.doctype.ex_requests.ex_requests.create_work_order',
                args: {
                    event: {
                        location: frm.doc.location,
                        room_number: frm.doc.room_number,
                        other: frm.doc.other,
                        id: frm.doc.name,
                        date: frm.doc.date,
                        time: frm.doc.time,
                        further_description: frm.doc.further_description,
                        table_umyd: frm.doc.table_umyd || []
                    }
                },
                callback: function(response) {
                    console.log('Response from create_work_order:', response);
                    if (!response.exc) {
                        frappe.msgprint('Work Order created with ID: ' + response.message);
                    } else {
                        frappe.msgprint('An error occurred: ' + response.exc);
                    }
                }
            });
        });
    }
});



