import os
from zk import ZK, const
from src.erp_interface import ERPConnector
from src.embeddings import AgentMemory
from datetime import datetime

# Configuration - Update with your Madinah Machine IP
ZKT_IP = "192.168.1.201" # Your local ZKTeco IP
ZKT_PORT = 4370

def sync_and_categorize():
    print(f"🚀 [START] Connecting to ZKTeco Machine at {ZKT_IP}...")
    zk = ZK(ZKT_IP, port=ZKT_PORT, timeout=5, password=0, force_udp=False)
    conn = None
    
    try:
        conn = zk.connect()
        erp = ERPConnector()
        memory = AgentMemory()
        
        # 1. Pull Attendance Logs
        attendance = conn.get_attendance()
        print(f"📡 Found {len(attendance)} raw logs on device.")

        for record in attendance:
            # 2. Get Employee Context from ERP (via our cached mapping)
            # In a real 10-year scale, we'd cache this to avoid hitting ERP every log
            emp_id = record.user_id
            timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            
            # 3. AI Categorization
            # We ask the "Brain" which sector this log belongs to based on the device location
            device_context = "ZKTeco Terminal in Madinah Construction Site"
            results = memory.collection.query(
                query_embeddings=[memory.model.encode(device_context).tolist()],
                n_results=1
            )
            
            best_match_sector = results['metadatas'][0][0]['id']
            sector_name = results['documents'][0][0]

            print(f"🕒 Log: Emp {emp_id} at {timestamp} -> AI Classified: {sector_name}")

            # 4. Push to ERPNext with the Sector Tag
            erp.push_checkin(
                employee_id=emp_id, 
                timestamp=timestamp, 
                device_id=f"ZKT_{best_match_sector}"
            )

        print("✅ [FINISH] All logs processed and categorized.")

    except Exception as e:
        print(f"❌ Hardware/Sync Error: {e}")
    finally:
        if conn:
            conn.disconnect()

if __name__ == "__main__":
    sync_and_categorize()
