import frappe
from frappe import msgprint
from erpnext.selling.doctype.customer.customer import Customer as ERPNextCustomer

class CustomCustomer(ERPNextCustomer):
    def validate(self):
        super().validate()
        msgprint(f"Custom override: Customer {self.customer_name} validated successfully!")
    