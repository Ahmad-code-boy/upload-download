# my_app/api/overrides.py

import frappe
from frappe.desk.search import search_link as original_search_link

@frappe.whitelist()
def custom_search_link(doctype, txt, query=None, filters=None, page_length=20, searchfield=None):
    if doctype == "Item":
        frappe.logger().info(f"📢 Custom search called for Item: {txt}")
    
    # original function call
    return original_search_link(doctype, txt, query, filters, page_length, searchfield)
