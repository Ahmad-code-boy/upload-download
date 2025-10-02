import frappe

@frappe.whitelist(allow_guest=True)
def custom_signup(email, full_name, password):
    if frappe.db.exists("User", email):
        return {"status": "fail", "message": "Email already registered"}

    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,    
        "enabled": 1,
        "new_password": password,
        "send_welcome_email": 1
        })
    user.insert(ignore_permissions=True)
    
    return {"status": "success", "message": "User created successfully"}




def after_insert(doc, method=None):
    frappe.msgprint(f"Customer Created: {doc.customer_name}")
    
    
@frappe.whitelist(allow_guest=False)
def images():
    images= frappe.get_list("Item",fields=["image"])
    
    return images    
    