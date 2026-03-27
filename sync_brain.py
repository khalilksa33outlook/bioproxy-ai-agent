import sys
import os

# Ensure the script can see the src/ folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from erp_interface import ERPConnector
from erp_explorer import ingest_general_ledger, ingest_financials
from document_loader import ingest_docs
from embeddings import AgentMemory

def auto_refresh():
    print(f"🕒 [CRON] Starting Scheduled Sync...")
    try:
        memory = AgentMemory()
        erp = ERPConnector()
        
        # 1. Sync any new PDF/Docx files in /data/company_docs/
        ingest_docs(memory)
        
        # 2. Sync latest ERP Sales & Projects
        ingest_financials(erp, memory)
        
        # 3. Sync latest General Ledger (Spending Patterns)
        ingest_general_ledger(erp, memory)
        
        print("✨ [CRON] Intelligence Base Updated Successfully.")
    except Exception as e:
        print(f"❌ [CRON] Sync Failed: {e}")

if __name__ == "__main__":
    auto_refresh()
