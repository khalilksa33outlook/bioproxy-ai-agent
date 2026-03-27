import os
import requests
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

class ERPConnector:
    def __init__(self):
        # Clean the URL
        self.url = os.getenv("ERP_URL", "https://erp.iicc.sa").strip().rstrip('/')
        
        # ERPNext API Keys
        self.api_key = os.getenv("ERP_API_KEY")
        self.api_secret = os.getenv("ERP_API_SECRET")
        
        # Cloudflare Service Tokens
        self.cf_id = os.getenv("CF_CLIENT_ID")
        self.cf_secret = os.getenv("CF_CLIENT_SECRET")
        
        self.headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.cf_id and self.cf_secret:
            self.headers["CF-Access-Client-Id"] = self.cf_id
            self.headers["CF-Access-Client-Secret"] = self.cf_secret
        
        self._verify_connection()

    def _verify_connection(self):
        test_url = f"{self.url}/api/method/frappe.auth.get_logged_user"
        try:
            response = requests.get(test_url, headers=self.headers, timeout=15)
            if response.status_code == 200:
                user = response.json().get("message")
                print(f"✅ Connected to ERP via Tunnel: {user}")
            else:
                print(f"❌ Connection Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Request Error: {e}")

    def get_resource(self, doctype, fields='["*"]', filters=None):
        """
        The missing method. Pulls any table from ERPNext.
        """
        endpoint = f"{self.url}/api/resource/{doctype}"
        params = {
            "fields": fields,
            "limit_page_length": 1000 
        }
        
        if filters:
            import json
            params["filters"] = json.dumps(filters)
            
        try:
            res = requests.get(endpoint, headers=self.headers, params=params, timeout=20)
            if res.status_code == 200:
                return res.json().get("data", [])
            else:
                print(f"⚠️ Failed to fetch {doctype}: {res.status_code}")
                return []
        except Exception as e:
            print(f"❌ API Error: {e}")
            return []

    def get_all_employees(self):
        return self.get_resource("Employee", fields='["name", "employee_name", "company"]')
