// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Trainer', {
	refresh: function(frm) {
		let trainer=frm.doc.full_name
		// console.log(trainer)
		frappe.call({
            method: 'classic_gym.services.rest.totalRating',
            args: {
				"trainer":trainer

            },
            callback: function (r) {
				
                
            },
           
        });

	}
});
