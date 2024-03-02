# Copyright (c) 2024, Polito and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_data(filters):
    conditions = "1=1"
    if filters.get("member_name"):
        conditions += f" AND gm.email='{filters.get('member_name')}'"

    SQL = f"""
        SELECT 
            gm.email,
            gm.age,
            mw.weight,
            mw.date
        FROM
            `tabGym Member` AS gm
        JOIN 
            `tabGym Member Weight` AS mw
        ON
            gm.email = mw.member_email
        WHERE
            {conditions}
    """
    data = frappe.db.sql(SQL)
    return data


def get_columns():
    return [
        "Member Name:Link/Gym Member:200",
        "Age:Data:200",
        "Member Weight:Link/Gym Member Weight:250",
        "Date:Date:200"
        
    ]
