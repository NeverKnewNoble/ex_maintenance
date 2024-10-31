// Copyright (c) 2024, Nortex and contributors
// For license information, please see license.txt


//  ! Function to toggle system notifications on or off
frappe.ui.form.on('Maintenance Settings', {
    after_save: function(frm) {
        frappe.call({
            method: 'ex_maintenance.ex_maintenance.doctype.maintenance_settings.maintenance_settings.toggle_notification',
            args: {
                notification_title: 'MainReq',
                enabled: frm.doc.send_system_message ? 1 : 0  // ? Enable if checked, disable if unchecked
            },
            callback: function(response) {
                if (response.message === 'success') {
                    frappe.msgprint(__('Notification has been updated successfully.'));
                } else {
                    frappe.msgprint(__('Failed to update the notification.'));
                }
            }
        });
    }
});





//  ! Consolidated function to toggle multiple email and SMS notifications on or off
frappe.ui.form.on('Maintenance Settings', {
    after_save: function(frm) {
        frappe.call({
            method: 'ex_maintenance.ex_maintenance.doctype.maintenance_settings.maintenance_settings.toggle_notification',
            args: {
                notification_title: 'MainReq (Email)',
                enabled: frm.doc.send_email ? 1 : 0  // ? Enable if checked, disable if unchecked
            },
            callback: function(response) {
                if (response.message === 'success') {
                    frappe.msgprint(__('Notification has been updated successfully.'));
                } else {
                    frappe.msgprint(__('Failed to update the notification.'));
                }
            }
        });

        frappe.call({
            method: 'ex_maintenance.ex_maintenance.doctype.maintenance_settings.maintenance_settings.toggle_notification',
            args: {
                notification_title: 'TaskAss (Email)',
                enabled: frm.doc.send_email ? 1 : 0  // ? Enable if checked, disable if unchecked
            },
        });

        frappe.call({
            method: 'ex_maintenance.ex_maintenance.doctype.maintenance_settings.maintenance_settings.toggle_notification',
            args: {
                notification_title: 'MainReq (SMS)',
                enabled: frm.doc.send_sms ? 1 : 0  // ? Enable if checked, disable if unchecked
            },
            callback: function(response) {
                if (response.message === 'success') {
                    frappe.msgprint(__('Notification has been updated successfully.'));
                } else {
                    frappe.msgprint(__('Failed to update the notification.'));
                }
            }
        });

        frappe.call({
            method: 'ex_maintenance.ex_maintenance.doctype.maintenance_settings.maintenance_settings.toggle_notification',
            args: {
                notification_title: 'TaskAss (SMS)',
                enabled: frm.doc.send_sms ? 1 : 0  // ? Enable if checked, disable if unchecked
            },
        });
    }
});

