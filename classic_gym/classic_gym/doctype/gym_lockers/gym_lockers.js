// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Lockers', {
    refresh: function (frm) {
        frappe.call({
            method: 'classic_gym.services.rest.availabilityReset',
            args: {

            },
            callback: function (r) {
                
            },
           
        });
    }
});
