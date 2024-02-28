// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Cardio Machines', {
	refresh: function(frm) {
		frappe.call({
            method: 'classic_gym.services.rest.machineAvailabilityUpdate',
            args: {

            },
            callback: function (r) {
                
            },
           
        });

	}
});

