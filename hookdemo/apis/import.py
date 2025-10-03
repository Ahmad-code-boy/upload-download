import frappe
from hookdemo.apis.send_data import send_invoice_to_api

@frappe.whitelist()
def ahmad(docname):
    ahmad=send_invoice_to_api(docname)
    return ahmad
    
    
    
    
    
    

