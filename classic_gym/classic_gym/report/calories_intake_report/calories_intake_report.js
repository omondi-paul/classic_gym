// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Calories Intake Report"] = {
	"filters": [
		{
		"fieldname" : "member_email",
		"label":__('Member Email'),
		"fieldtype": 'Link',
		"options":"Gym Member",
		 "width": 200,
		"reqd": 0

		},
		{
				
			"fieldname": "age",
            "label": __("Age"),
            "fieldtype": "Data",
            "width": 200,
            "reqd": 0
		
				},
		{
			"fieldname" : "calorie_intake",
			"label":__('Calorie Intake'),
			"fieldtype": 'Link',
			"options":"Calorie Intake",
			"width": 200,
			"reqd": 0
	
			},
		{
				
			"fieldname": "date",
            "label": __("Date"),
            "fieldtype": "Date",
            "width": 200,
            "reqd": 0
		
				}
	]
};
