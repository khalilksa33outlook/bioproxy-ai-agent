import sys
import os
import re
import requests
import json

# Inside your CEOIntelAgent class, add this method:

    def synthesize_with_ollama(self, query, context_docs):
        """Sends the search results to Ollama to generate a human response."""
        
        # Combine the top database rows into one 'context' block
        context_text = "\n".join(context_docs)
        
        prompt = f"""
        You are the AI Executive Assistant for the IICC Group (Insight International Contracting Company).
        Use the following internal data to answer the CEO's question in a professional, concise manner.
        
        DATA FROM ERP & DOCUMENTS:
        {context_text}
        
        QUESTION: {query}
        
        ANSWER:
        """

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json().get("response", "I couldn't synthesize a response.")
        except Exception as e:
            return f"⚠️ Ollama Error: {e}. (Make sure Ollama is running)"

# Now, update your route_query to use this synthesis:

    def route_query(self, query):
        query_lower = query.lower()
        is_financial = any(word in query_lower for word in self.fin_keywords)
        
        # 1. Get the raw data from ChromaDB
        results = self.memory.search(query, n_results=5)
        raw_docs = results['documents'][0]
        
        # 2. Let Ollama explain it
        print("\n🧠 [AI THINKING...]")
        final_answer = self.synthesize_with_ollama(query, raw_docs)
        
        print("\n🤖 [EXECUTIVE SUMMARY]:")
        print(final_answer)
        
        # 3. Still show the source for verification (SysAdmin style)
        print("\n📍 [SOURCES USED]:", [m.get('id') for m in results['metadatas'][0]])

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
from embeddings import AgentMemory

class CEOIntelAgent:
    def __init__(self):
        self.memory = AgentMemory()
        # Keywords that trigger the Financial "Auditor" mode
        self.fin_keywords = [
            'sar', 'spend', 'cost', 'invoice', 'ledger', 'payment', 
            'revenue', 'budget', 'price', 'profit', 'debit', 'credit'
        ]

    def route_query(self, query):
        query_lower = query.lower()
        
        # 1. Detect Intent
        is_financial = any(word in query_lower for word in self.fin_keywords)
        
        if is_financial:
            print("\n🔍 [MODE: FINANCIAL AUDITOR]")
            self.analyze_finances(query)
        else:
            print("\n📚 [MODE: GENERAL KNOWLEDGE]")
            self.get_general_info(query)

    def analyze_finances(self, query):
        results = self.memory.search(query, n_results=10)
        total_found = 0.0
        
        print("-" * 50)
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            
            # Only show Finance/Ledger/Invoice categories
            if meta.get('category') in ['FINANCE', 'LEDGER']:
                print(f"💰 {doc}")
                # Simple regex to extract SAR values for a quick sum
                match = re.search(r"(\d+\.?\d*)\s*SAR", doc)
                if match:
                    total_found += float(match.group(1))
        
        print("-" * 50)
        print(f"📈 Estimated Total in Search Results: {total_sum:,.2f} SAR")

    def get_general_info(self, query):
        results = self.memory.search(query, n_results=5)
        
        print("-" * 50)
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            
            # Show Documents, Sectors, and Employee info
            category = meta.get('category', 'INFO')
            source = meta.get('id', 'Internal')
            print(f"📍 [{category}] (Source: {source})")
            print(f"{doc}\n")

    def run(self):
        print("\n⚡ IICC MASTER INTELLIGENCE AGENT v1.0")
        print("Connected to 16 Sectors. Type 'exit' to close.")
        
        while True:
            q = input("\n💬 CEO Query: ")
            if q.lower() in ['exit', 'quit']: break
            if not q.strip(): continue
            self.route_query(q)

if __name__ == "__main__":
    agent = CEOIntelAgent()
    agent.run()
