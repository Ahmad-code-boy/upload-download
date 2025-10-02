# hookdemo/hookdemo/report/send_mails/send_mails.py

import frappe

def execute(filters=None):
    columns = [
        {"label": "To", "fieldname": "to", "fieldtype": "Data", "width": 200},
        {"label": "Subject", "fieldname": "subject", "fieldtype": "Data", "width": 200},
        {"label": "Message", "fieldname": "message", "fieldtype": "Small Text", "width": 300},
        {"label": "Current Time", "fieldname": "current_time", "fieldtype": "Time", "width": 120},
    ]

    data = frappe.db.sql("""
        SELECT 
            `to`, 
            subject, 
            message, 
            current_time
        FROM `tabSend Mails`
    """, as_dict=True)

    # Chart Example → count mails by subject
    subject_counts = {}
    for row in data:
        subject = row.get("subject") or "No Subject"
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

    chart = {
        "data": {
            "labels": list(subject_counts.keys()),     
            "datasets": [
                {
                    "name": "Mails",
                    "values": list(subject_counts.values())   # y-axis → count
                }
            ]
        },
        "type": "bar",   
        "height": 100,
        "colors": [ "#AB2626"]    }

    # Important → always return 4 values for chart
    return columns, data, None, chart
