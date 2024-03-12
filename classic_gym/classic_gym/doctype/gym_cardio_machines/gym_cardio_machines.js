// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Cardio Machines', {
	refresh: function(frm) {
		frappe.call({
            method: 'classic_gym.services.rest.machineAvailabilityReset',
            args: {

            },
            callback: function (r) {
                
            },
           
        });

	},
    validate: function (frm) {
  
        frappe.call({
            method: 'classic_gym.classic_gym.doctype.gym_cardio_machines.gym_cardio_machines.gym_machines_items',
            args: {
             
            },
            callback: function (r) {
                console.log(r.message)
            }
        });

    },
   
    });
        



