import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from erp_interface import ERPConnector

erp = ERPConnector()

def test_visibility(doctype):
    print(f"\n🔍 Testing {doctype}...")
    # No filters, just try to get the first 5 records
    data = erp.get_resource(doctype, fields='["name"]')
    if data:
        print(f"✅ Success! Found {len(data)} total records.")
    else:
        print(f"❌ Zero records returned. Check Permissions for {doctype}.")

test_visibility("Sales Invoice")
test_visibility("Task")
test_visibility("GL Entry")
test_visibility("Employee")
