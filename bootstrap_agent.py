import os
import sys
# Ensure the script can see the src/ folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from erp_interface import ERPConnector
from embeddings import AgentMemory

def bootstrap():
    print("🚀 [DEBUG] Script started...")
    
    try:
        # 1. Initialize Brain and Connection
        erp = ERPConnector()
        memory = AgentMemory()
        print("✅ [DEBUG] Systems Initialized.")

        # 2. Define your Business Hierarchy
        print("🏢 [DEBUG] Indexing Company Hierarchy...")
        business_units = [
            {"id": "IHTS", "name": "Ibrahim Home Textile Sourcing", "parent": None, "type": "Group"},
            {"id": "ITMC", "name": "Ibrahim Textile Manufacturing Company", "parent": "IHTS", "type": "Manufacturing Hub"},
            {"id": "IICC", "name": "Insight International Contracting Company", "parent": "ITMC", "type": "Contracting"},
            {"id": "ITT", "name": "Insight Travel & Tourism", "parent": "ITMC", "type": "Services"},
            {"id": "SEC-201", "name": "Home Textile Manufacturing", "parent": "ITMC", "type": "Sector"},
            {"id": "SEC-202", "name": "Agriculture", "parent": "ITMC", "type": "Sector"}
        ]

        for unit in business_units:
            desc = f"{unit['name']} is a {unit['type']} under {unit['parent'] or 'Top Level'}"
            memory.save_entity("BusinessUnit", unit['id'], desc, unit)
            print(f"   🔹 Logged: {unit['name']}")

        # 3. Fetch and Index Employees
        print("📡 [DEBUG] Fetching Employees from erp.iicc.sa...")
        employees = erp.get_all_employees()
        
        if employees:
            for emp in employees:
                # Semantic description for the AI to understand roles later
                desc = f"Employee {emp['employee_name']} working at {emp['company']}"
                memory.save_entity("Employee", emp['name'], desc, {"company": emp['company']})
            print(f"✅ [DEBUG] {len(employees)} Employees Vectorized.")
        else:
            print("⚠️ [DEBUG] No employees found in ERP. Check API permissions.")

        print("\n✨ [SUCCESS] Overall Business Brain Initialized for 2026.")

    except Exception as e:
        print(f"❌ [CRITICAL ERROR] {str(e)}")

if __name__ == "__main__":
    bootstrap()
