import frappe
from frappe.utils import now

@frappe.whitelist(allow_guest=False)
def sendmail(to=None, subject=None, message=None):
    if not (to and subject and message):
        frappe.throw("Email subject and message are required to send mail.")

    try:
        frappe.sendmail(
            recipients=[to],   
            subject=subject,
            message=message,
           
        )
   
    except Exception as e:
        email_status = f"Email failed: {str(e)}"

    try:
        doc = frappe.get_doc({
            "doctype": "Send Mails",   
            "to": to,
            "subject": subject,
            "message": message,
            "current_time": now()
        })
        doc.insert()
        frappe.db.commit()
        log_status = "Data stored successfully"
    except Exception as e:
        log_status = f"Log insert failed: {str(e)}"

    return {
        "email_status": email_status,
        "log_status": log_status
    }

@frappe.whitelist()

def csrf_token():
    return {
        "csrf_token":frappe.local.session.csrf_token
    }