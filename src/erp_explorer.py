import os

def ingest_financials(erp, memory):
    print("📊 [EXPLORER] Extracting Sales and Projects...")
    
    # 1. Pull Sales Invoices (Revenue Analysis)
    # Using 'docstatus' filter to ensure we only get submitted/paid invoices (1), not drafts (0)
    invoices = erp.get_resource("Sales Invoice", 
        fields='["name", "customer", "grand_total", "status", "posting_date", "company"]',
        filters=[["docstatus", "=", 1]])
    
    for inv in invoices:
        text_blob = (f"Sales Invoice {inv['name']} for {inv['customer']} "
                     f"is {inv['status']} for a total of {inv['grand_total']} SAR. "
                     f"Dated {inv['posting_date']} under company {inv['company']}.")
        
        memory.save_entity("FINANCE", inv['name'], text_blob, 
                           {"type": "Invoice", "customer": inv['customer'], "company": inv['company']})

    # 2. Pull Tasks (Operational Analysis)
    # Note: In ERPNext, the table is usually 'Task', not 'Project Task'
    tasks = erp.get_resource("Task", 
        fields='["name", "project", "subject", "status", "exp_end_date"]',
        filters=[["docstatus", "<", 2]])
    
    for task in tasks:
        # Check if project exists to avoid NoneType errors in the blob
        project_name = task.get('project') if task.get('project') else "Unassigned"
        text_blob = (f"Task '{task['subject']}' in Project {project_name} "
                     f"is currently {task['status']}. Expected completion: {task.get('exp_end_date', 'N/A')}.")
        
        memory.save_entity("PROJECT", task['name'], text_blob, 
                           {"type": "Task", "project": project_name})

    print(f"✅ Indexed {len(invoices)} Invoices and {len(tasks)} Tasks.")


def ingest_general_ledger(erp, memory):
    print("💰 [EXPLORER] Analyzing General Ledger for spending patterns...")
    
    # Filtering from 2025 onwards to ensure the Brain has historical context
    # and to catch any late 2025 entries impacting 2026 budgets.
    filters = [
        ["posting_date", ">=", "2025-01-01"],
        ["is_cancelled", "=", 0]
    ]
    
    ledger_entries = erp.get_resource("GL Entry", 
        fields='["name", "account", "debit", "credit", "remarks", "voucher_no", "company", "posting_date"]',
        filters=filters)
    
    for entry in ledger_entries:
        # Determine if this was a spend (debit) or revenue (credit)
        amount = entry['debit'] if entry['debit'] > 0 else -entry['credit']
        action = "spent" if entry['debit'] > 0 else "received"
        
        text_blob = (f"On {entry['posting_date']}, {entry['company']} {action} {abs(amount)} SAR "
                     f"under account {entry['account']}. "
                     f"Reference: {entry['voucher_no']}. Remarks: {entry['remarks']}")
        
        memory.save_entity("LEDGER", entry['name'], text_blob, {
            "type": "GL_Entry",
            "company": entry['company'],
            "account": entry['account'],
            "date": entry['posting_date']
        })

    print(f"✅ Indexed {len(ledger_entries)} Ledger transactions.")
