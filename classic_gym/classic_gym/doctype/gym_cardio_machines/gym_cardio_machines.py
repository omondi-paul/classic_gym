# Copyright (c) 2024, Polito and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.document import Document

class GymCardioMachines(Document):
	pass
@frappe.whitelist(allow_guest=True)
def gym_machines_items():
		gym_machines = frappe.db.get_all("Gym Cardio Machines",{},{"name","machine_name","serial_number",})

		for machine  in gym_machines:
			existing_item = frappe.db.get_all("Item", {"item_name": machine.name}, {'item_name', 'item_group','item_code'})

			if existing_item:
				item = frappe.get_doc("Item", existing_item[0].item_name)
				item.item_group = "machines" 
				item.item_code = machine.name
				item.description = machine.description
				item.save()
				# frappe.db.commit()

				
			else:
				item = frappe.get_doc({
					"doctype": "Item",
					"item_code": machine.name,
					"item_name": machine.name,
					"item_group": "machines",  
					"description":machine.description
				})
				item.insert()
			frappe.db.commit()	
			
		return "success"

