import os
from datetime import datetime
from embeddings import AgentMemory
from erp_interface import ERPConnector

class BioProxyAgent:
    def __init__(self):
        self.memory = AgentMemory()
        self.erp = ERPConnector()
        self.state_file = "./data/last_sync.txt"

    def run_sync(self):
        print(f"--- Agent Heartbeat: {datetime.now()} ---")
        # 1. Fetch from ZKTeco
        # 2. For each log, use self.memory.find_match() 
        # 3. Push to ERPNext
        # 4. Update state_file so we never process the same log twice
