# /home/frappe/bioproxy-ai-agent/run_agent.py
from src.erp_interface import ERPConnector

def main():
    agent_link = ERPConnector()
    employees = agent_link.get_all_employees()
    print(f"Successfully fetched {len(employees)} employees for the AI model.")

if __name__ == "__main__":
    main()
