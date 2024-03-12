// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Member', {
    
    onload: function (frm) {
        frm.set_query('locker_number', 'locker', () => {
            return {
                filters: {
                    "status": "Available"
                }
            }
        })
        frm.set_query('machine_name', 'cardio_machine', () => {
            return {
                filters: {
                    "current_status": "Available"
                }
            }
        })
    },
    email: function (frm) {
        let email = frm.doc.email;
     
        frappe.call({
            method: 'classic_gym.services.rest.check_email',
            args: {
                'email': email
            },
            callback: function (r) {

                
                if (r.message) {
                    frappe.msgprint('This email already exists.');
                    frappe.validate = false;
                }
                else {
                    frappe.validate = true;
                }
            }
        });
    },
    validate: function (frm) {
        let dateOfBirth=frm.doc.date_of_birth;
        let email=frm.doc.email;
        let full_name=frm.doc.full_name;
        let contact=frm.doc.contact
        let membership_type=frm.doc.membership_type || null
        frappe.call({
            method: 'classic_gym.classic_gym.doctype.gym_member.gym_member.customerInvoice',
            args: {
                'full_name':full_name,
                'email':email,
                'contact':contact,
                'membership_type':membership_type
            },
            callback: function (r) {
            }
        });


        frappe.call({
            method: 'classic_gym.services.rest.calculate_age',
            args: {
                "dateOfBirth":dateOfBirth
            },
            callback: function (r) {
                if (r.message >=0) {
                  frm.set_value('age',r.message)
                 
                }
                if (r.message <0){
                    frappe.msgprint('Invalid Date of Birth.');
                    frappe.validate = false;

                }
            }
        });
        frappe.call({
            method: 'classic_gym.services.rest.lockerAvailability',
            args: {

                "email": email

            },
            callback: function (r) {
            }
        });
        frappe.call({
            method: 'classic_gym.services.rest.lockerCharges',
            args: {
                "email": email
            },
            callback: function (r) {
                if (r.message) {
                    frm.set_value('locker_charges', r.message);
                } else {
                    frm.set_value('locker_charges', 0.0); // Setting default value to 0
                }
            },
            error: function(err) {
                // console.error("Error occurred during frappe.call:", err);
              
            }
        });
        frappe.call({
            method: 'classic_gym.services.rest.machineAvailabity',
            args: {

                "email": email

            },
            callback: function (r) {

            } 
        });
    },
    gym_membership_date: function (frm) {
        let membership = frm.doc.membership_type;
        let membership_date = frm.doc.gym_membership_date
        frappe.call({
            method: 'classic_gym.services.rest.expiry',
            args: {
                'membership': membership,
                'membership_date': membership_date

            },
            callback: function (r) {
                let expired = 'expired'
                // console.log(r)
                if (r.message > 0) {
                    frm.set_value('days_remaining', r.message);
                } else if (r.message <= 0) {
                    // Handle negative values
                    // For example, display a message to the user
                    frm.set_value('days_remaining', expired);
                    frappe.msgprint('The membership has expired.');
                }
            }
        });

    },
    subscribed_workout: function (frm) {
        let workout = frm.doc.subscribed_workout;
        frappe.call({
            method: 'classic_gym.services.rest.trainer',
            args: {
                'workout': workout
            },
            callback: function (r) {
                console.log(r)
                if (r.message) {
                    frm.set_value('trainer', r.message[0]);
                    frm.set_value('subscribed_work_out_cost', r.message[1])
                } else {
                    frm.set_value('trainer', 'None');
                    frappe.msgprint('No Trainer Found');
                }
            }
        });
    },
    membership_type: function (frm) {
        let type = frm.doc.membership_type;
        frappe.call({
            method: 'classic_gym.services.rest.subscription',
            args: {
                'type': type,
            },
            callback: function (r) {
                if (r.message) {
                    frm.set_value('membership_cost', r.message[0]);
                }
            }
        });
    },   
    
    gym_plan: function (frm) {
        let parent = frm.doc.gym_plan;
        frappe.call({
            method: 'classic_gym.services.rest.availablePlans',
            args: {
                'parent': parent
            },
            callback: function (r) {
                let availables = r.message;
                let debugText = '';
                for (let available of availables) {
                    debugText += available + '\n';
                }
                frm.set_value('available_plans', debugText+ "\n");
            }
        });
    },
     refresh: function (frm) {
            let member_ship_cost = frm.doc.membership_cost || 0;
            let subscribed_workout_cost = frm.doc.subscribed_work_out_cost || 0;
            let locker_charges = frm.doc.locker_charges || 0;
            let email=frm.doc.email;
    
            frappe.call({
                method: 'classic_gym.services.rest.totalCharges',
                args: {
                    "member_ship_cost": member_ship_cost,
                    "subscribed_workout_cost": subscribed_workout_cost,
                    "locker_charges": locker_charges
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value('price_total', r.message);
                    } else {
                        console.error("Error: No total charges received from server.");
                    }
                },
                error: function (err) {
                //    console.error("Error calling totalCharges function:", err);
                }
            });
            frappe.call({
                method: 'classic_gym.services.rest.booking',
                args: {
                    "email": email,

                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value('title', r.message);
                    }
                }
            });
            frappe.call({
                method: 'classic_gym.services.rest.machineAvailabilityReset',
                args: {
    
                },
                callback: function (r) {
                    
                },               
            });
            frappe.call({
                method: 'classic_gym.services.rest.lockerAvailabilityReset',
                args: {
    
                },
                callback: function (r) {
                    console.log(r.message)
                    
                },
               
            });
            
        },
    });
        






frappe.ui.form.on('Gym Locker Booking', {
    locker_number(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        let email = frm.doc.email;
        let locker_number=item.locker_number || 0;
     
        frappe.call({
            method: 'classic_gym.services.rest.booking',
            args: {
                "email": email,
                // "name": name,
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, {
                        email: r.message,
                    });
                    // frappe.model.set_value(cdt,cdn,{
                    //     member:r.message[1],
                    // });
                }
            }
        });
        frappe.call({
            method: 'classic_gym.services.rest.check_locker_number',
            args: {
                'locker_number': locker_number
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint('This locker is not available.');
                    frappe.validate = false;
                }
                else {
                    frappe.validate = true;
                }
            }
        });

    },

    
    number_of_days(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        let startDate = item.book_date;
        let number_of_days = item.number_of_days;

        frappe.call({
            method: 'classic_gym.services.rest.endDate',
            args: {
                "startDate_str": startDate,
                "number_of_days": number_of_days,
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, {
                        book_end_date: r.message[0]
                    });
                    frappe.model.set_value(cdt, cdn, {
                        total_price: r.message[1]
                    });

                }
                else {
                    frappe.msgprint("Error calculating end date");
                }
            }
        });
    },

    end_time(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        let startTime = item.start_time ;
        let endTime = item.end_time

        frappe.call({
            method: 'classic_gym.services.rest.totalHours',
            args: {
                "start_time_str": startTime,
                "end_time_str": endTime,
            },
            callback: function (r) {
                if (r.message) {
                    console.log(r.message)
                    frappe.model.set_value(cdt, cdn, {
                        number__of_hours: r.message[0],
                        total_price: r.message[1],
                    });
                }
                else {
                   
                }
            }
        });


    },
});




frappe.ui.form.on('Cardio Machine Booking', {
    machine_name(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        let email = frm.doc.email;
        let machine_name=item.machine_name
     
        frappe.call({
            method: 'classic_gym.services.rest.booking',
            args: {
                "email": email,
                // "name": name,
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, {
                        email: r.message,
                    });
                    // frappe.model.set_value(cdt,cdn,{
                    //     member:r.message[1],
                    // });
                }
            }
        });
        frappe.call({
            method: 'classic_gym.services.rest.check_machine_name',
            args: {
                'machine_name': machine_name
            },
            callback: function (r) {
                if (r.message) {
                    
                    frappe.msgprint('This machine is not available.');
                    frappe.validate = false;
                }
                else {
                    frappe.validate = true;
                }
            }
        });
    }
});




frappe.ui.form.on('Trainer Ratings', {
        trainer_name(frm, cdt, cdn) {
            let item = locals[cdt][cdn];
            let email = frm.doc.email;
         
            frappe.call({
                method: 'classic_gym.services.rest.booking',
                args: {
                    "email": email,
                    // "name": name,
                },
                callback: function (r) {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, {
                            member: r.message,
                        });
                        
                    }
                }
            });
         
      
    },
});


frappe.ui.form.on('Group Class Booking', {
    class_name(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        let email = frm.doc.email;
     
        frappe.call({
            method: 'classic_gym.services.rest.booking',
            args: {
                "email": email,
              
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, {
                        member_email: r.message,
                    });
                    // frappe.model.set_value(cdt,cdn,{
                    //     member:r.message[1],
                    // });
                }
            }
        });

    
    },
});


frappe.ui.form.on('Gym Member Weight', {
    weight(frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        let email = frm.doc.email;
     
        frappe.call({
            method: 'classic_gym.services.rest.weight',
            args: {
                "email": email,
              
            },
            callback: function (r) {
                if (r.message) {
                    frappe.model.set_value(cdt, cdn, {
                        member_email: r.message[0],
                        date: r.message[1]
                    });
                }
            }
        });
    },
});

