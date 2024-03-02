# Copyright (c) 2024, Polito and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_data(filters):
    conditions = "1=1"
    if filters.get("member_email"):
        conditions += f" AND gm.email='{filters.get('member_email')}'"

    SQL = f"""
        SELECT 
            gm.email,
            gm.age,
            ci.calorie_intake,
            ci.date
        FROM
            `tabGym Member` AS gm
        JOIN 
            `tabCalorie Intake` AS ci
        ON
            gm.email = ci.parent
        WHERE
            {conditions}
    """
    data = frappe.db.sql(SQL)
    return data


def get_columns():
    return [
        "Member Name:Link/Gym Member:200",
        "Age:Data:200",
        "Calorie Intake:Link/Calorie Intake:250",
        "Date:Date:200"
        
    ]

