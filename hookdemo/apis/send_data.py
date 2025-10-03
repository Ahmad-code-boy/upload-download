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




def get_url():
    url="https://posttestserver.dev/p/4yascznld867xqiq/post"
    return url



@frappe.whitelist()
def payload(docname):
    doc = frappe.get_doc("Sales Invoice", docname)
    url=get_url()

    payload={
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

    res = requests.post(url, json=payload)
    
    if res:
        return {
            "Status":res.status_code,
            "Message":res.text,
            "Sent Data":payload
            
        }





# imported api to import.py file 

def exist(docname):
    if not frappe.db.exists("Sales Invoice", docname):
        frappe.throw(f"Your Invoice Name {docname} does not exist")

def get_url():
    return " https://posttestserver.dev/p/p1i6gmkg8xs2dxtt/post"

def get_valid_items(doc):
    return [
        {
            "item_code": i.item_code,
            "item_name": i.item_name,
            "qty": i.qty,
            "rate": i.rate,
            "amount": i.amount
        }
        for i in doc.items 
    ]



def prepare_payload(doc):
    items = get_valid_items(doc)

    return {
        "invoice_no": doc.name,
        "customer": doc.customer,
        "posting_date": str(doc.posting_date),
        "items": items,
        "system_total": doc.total,
        "grand_total": doc.grand_total
    }

def post_to_api(data):
    res = requests.post(get_url(), json=data)
    return {
        "Status": res.status_code,
        "Response": res.text,
        "Sent Data": data
    }


def send_invoice_to_api(docname):
    exist(docname)

    doc = frappe.get_doc("Sales Invoice", docname)

    payload = prepare_payload(doc)


    response = post_to_api(payload)
    
    return response


