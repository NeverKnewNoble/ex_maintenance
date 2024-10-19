// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Ex Requests", {
// 	refresh(frm) {

// 	},
// });

// ? Function to get request time
frappe.ui.form.on("Ex Requests", {
    refresh(frm) {
        if (frm.is_new()) {
            frm.set_value('request_time', frappe.datetime.now_time());
        }
    },
}); 


//  ? Function to call python function 
// frappe.ui.form.on('Ex Requests', {
//     // You can use a custom button or a specific event like after save, before save, or validate.
//     onload(frm) {
//         frm.add_custom_button('Create Work Order', function() {
//             frappe.call({
//                 method: 'ex_maintenance.ex_maintenance.doctype.ex_requests.ex_requests.create_work_order',
//                 args: {
//                     event: {
//                         location: frm.doc.location,  // Fetching location from form
//                         room_number: frm.doc.room_number,  // Fetching room_number from form
//                         other: frm.doc.other,  // Fetching additional details from form
//                         id: frm.doc.name,  // Document name (used as request code)
//                         date: frm.doc.date,  // Date from form
//                         time: frm.doc.time,  // Time from form
//                         further_description: frm.doc.further_description,  // Additional description field
//                         table_umyd: frm.doc.table_umyd || []  // Assuming this is a child table (fetch data or empty array)
//                     }
//                 },
//                 callback: function(response) {
//                     if (!response.exc) {
//                         frappe.msgprint('Work Order created with ID: ' + response.message);
//                     } else {
//                         frappe.msgprint('An error occurred: ' + response.exc);
//                     }
//                 }
//             });
//         });
//     }
// });



// Function to call Python function when a button is clicked
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



