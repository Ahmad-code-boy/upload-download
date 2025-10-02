import requests
import frappe

@frappe.whitelist()
def send_sales_invoice_to_mock(docname):
    

    url = "https://posttestserver.dev/p/4yascznld867xqiq/post"

    doc = frappe.get_doc("Sales Invoice", docname)
        
    if not frappe.db.exists("Sales Invoice",doc):
        frappe.throw(f"Your invoice{doc} is not found")
            

    sales_invoice = {
        "invoice_no": doc.name,
        "customer": doc.customer,
        "posting_date": str(doc.posting_date),
        "items": [
            {
                "item_code": item.item_code,
                "item_name": item.item_name,
                "qty": item.qty,
                "rate": item.rate
            } for item in doc.items
        ],
        "total": doc.total,
        "grand_total": doc.grand_total
    }

    res = requests.post(url, json=sales_invoice)

    return {
        "status": res.status_code,
        "response": res.text,
        "sent_data": sales_invoice
    }




