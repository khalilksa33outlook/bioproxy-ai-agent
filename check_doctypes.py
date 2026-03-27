import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from erp_interface import ERPConnector

erp = ERPConnector()
# We test for the most common naming variations
test_list = ["Sales Invoice", "Project Task", "GL Entry", "Task", "Project"]

print("\n🔍 Checking DocType Availability...")
for dt in test_list:
    res = erp.get_resource(dt, fields='["name"]', filters=[["docstatus", "<", 2]])
    status = "✅ Found" if len(res) > 0 else "❌ Not Found / Empty"
    print(f"{dt}: {status} ({len(res)} records)")
