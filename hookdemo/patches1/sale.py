# hookdemo/patches/custom_patch.py
import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

def custom_before_save(self):
    frappe.msgprint("Monkey patch before_save called")

    if self.customer == "Walk-in Customer":
        frappe.throw("Walk-in not allowed (patched)!")

SalesInvoice.before_save = custom_before_save
