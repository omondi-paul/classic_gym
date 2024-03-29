# Copyright (c) 2024, Polito and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class GymMember(WebsiteGenerator):
	pass

@frappe.whitelist(allow_guest=True)
def customerInvoice(full_name, email, contact,membership_type):
    # Check if email exists for the customer
    existing_customer = frappe.get_all("Customer", filters={"email_id": email})

    if existing_customer:
        # Update existing customer document
        customer = frappe.get_doc("Customer", existing_customer[0].name)
        customer.customer_name = full_name
        customer.territory = "Kenya"  # Assuming you want to update territory as well
        customer.mobile_number = contact  # Fixed syntax issue
        customer.save()
        # frappe.msgprint(f"Customer '{full_name}' updated successfully.")
    else:
        # Create a new customer document
        customer = frappe.get_doc({
            'doctype': 'Customer',
            'customer_name': full_name,
            'customer_type': 'Individual',
            'customer_group': 'Individual',
            'mobile_number': contact,
            'territory': "Kenya",
            'email_id': email
        })
        customer.insert()

    locker_bookings = frappe.get_all('Gym Locker Booking', filters={'email': email}, fields=['name', 'email', 'book_end_date', 'end_time', 'total_price'])
    if locker_bookings:
        existing_invoice = frappe.get_all("Sales Invoice", filters={"customer": full_name, "status": "Draft"})
        if existing_invoice:
            invoice = frappe.get_doc("Sales Invoice", existing_invoice[0].name)
        else:
            invoice = frappe.get_doc({
                "doctype": "Sales Invoice",
                "customer": full_name,
                "items": [],
            })

        for locker_booking in locker_bookings:
            item_name = locker_booking.name
            item_amount = locker_booking.total_price  
            existing_item = frappe.get_all("Item",{"item_name": item_name},{'item_name','item_group'}) 
            if existing_item:
                item = frappe.get_doc("Item", existing_item[0].get('item_name'))
                item.item_code = item_name  
                item.item_group = "Services"  
                item.description = "Booking of locker for gym members"
                item.save()
                frappe.db.commit()
            else:
                item = frappe.get_doc({
                    "doctype": "Item",
                    "item_code": item_name,
                    "item_name": item_name,
                    "item_group": "Services",
                    "description": "Booking of locker for gym members"
                })
                item.insert()
                frappe.db.commit()
                
            existing_item_codes = [item.item_code for item in invoice.get("items")]

            if item_name not in existing_item_codes:
                invoice.append("items", {
                    "item_code": item_name,
                    "rate": item_amount,
                    "amount": item_amount,
                    "qty": 1,
                })


        if not existing_invoice:
            invoice.insert()
        else:
            invoice.save()

    if membership_type:
        existing_invoice = frappe.get_all("Sales Invoice", filters={"customer": full_name, "status": "Draft"})
        if existing_invoice:
            invoice = frappe.get_doc("Sales Invoice", existing_invoice[0].name)
        else:
            invoice = frappe.get_doc({
                "doctype": "Sales Invoice",
                "customer": full_name,
                "items": [],
            })
        item_name=email+"membership"
        existing_item=frappe.get_all("Item",{"item_code":item_name},{'item_name','item_group'})
        membership=frappe.get_all("Gym Membership",{"type":membership_type},{'type','price'})
        if existing_item:
            item=frappe.get_doc('Item',existing_item[0].item_name)
            item.item_code = item_name  
            item.item_group = "membership_type"  
            item.description = "Membership Charges"
            item.save()
    
        else:
            item = frappe.get_doc({
                        "doctype": "Item",
                        "item_code": item_name,
                        "item_name": item_name,
                        "item_group": "membership_type",
                        "description": "Membership Charges"
                    })
            item.insert()
        frappe.db.commit()
        existing_item_codes = [item.item_code for item in invoice.get("items")]
        if item_name not in existing_item_codes:
            invoice.append("items", {
                        "item_code": item_name,
                        "rate": membership[0].price,
                        "amount":membership[0].price,
                        "qty": 1,
                })
        if not existing_invoice:
            invoice.insert()
        else:
            invoice.save()
        frappe.db.commit()

    existing_invoice = frappe.get_all("Sales Invoice", filters={"customer": full_name, "status": "Draft"})
    if existing_invoice:
        invoice = frappe.get_doc("Sales Invoice", existing_invoice[0].name)

    
        locker_bookings = frappe.get_all('Gym Locker Booking', filters={'email': invoice.customer}, fields=['name'])
        locker_booking_names = [booking.name for booking in locker_bookings]

        items_to_remove = []
        for item in invoice.items:
            if item.item_code in locker_booking_names:
                continue
            else:
                items_to_remove.append(item)

        for item in items_to_remove:
            invoice.remove_item(item)

        invoice.save()
        frappe.db.commit()


        
            # print("Invoice items adjusted successfully.")
       


        
        
           

    #     frappe.db.commit()
    # return

# @frappe.whitelist(allow_guest=True)
# def membership_items(full_name, email, contact,membership_type):
#     existing_customer = frappe.get_all("Customer", filters={"email_id": email})

#     if existing_customer:
#         customer = frappe.get_doc("Customer", existing_customer[0].name)
#         customer.customer_name = full_name
#         customer.territory = "Kenya"
#         customer.mobile_number = contact
#         customer.save()

#     else:
#         customer = frappe.get_doc({
#             'doctype': 'Customer',
#             'customer_name': full_name,
#             'customer_type': 'Individual',
#             'customer_group': 'Individual',
#             'mobile_number': contact,
#             'territory': "Kenya",
#             'email_id': email
#         })
#         customer.insert()

