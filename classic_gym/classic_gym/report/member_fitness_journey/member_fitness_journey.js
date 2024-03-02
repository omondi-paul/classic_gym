// Copyright (c) 2024, Polito and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Member Fitness Journey"] = {
	"filters": [
		{
		"fieldname" : "member_name",
		"label":__('Member Name'),
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
			"fieldname" : "member_weight",
			"label":__('Member Weight'),
			"fieldtype": 'Link',
			"options":"Gym Member Weight",
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
