# Copyright (c) 2024, Polito and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from frappe.utils import now, getdate

class GymLockerBooking(Document):
    def before_save(self):
        today_date = getdate(now())
        self.book_date=today_date

	