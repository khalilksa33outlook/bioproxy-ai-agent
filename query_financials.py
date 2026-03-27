import sys
import os
import re

# Ensure the script can see the src/ folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from embeddings import AgentMemory

def extract_amount(text):
    """Helper to pull the SAR value from the indexed sentence."""
    match = re.search(r"(\d+\.?\d*)\s*SAR", text)
    return float(match.group(1)) if match else 0.0

def query_financial_intelligence():
    memory = AgentMemory()
    
    print("\n--- 💹 IICC Financial Intelligence Portal ---")
    print("Ask about spending, revenue, or project costs (Type 'exit' to quit).")

    while True:
        query = input("\n🧐 Question: ")
        if query.lower() in ['exit', 'quit']:
            break

        # Search the Vector DB for the top 10 relevant financial records
        results = memory.collection.query(
            query_embeddings=[memory.model.encode(query).tolist()],
            n_results=10,
            where={"type": {"$in": ["GL_Entry", "Invoice", "Task"]}}
        )

        documents = results['documents'][0]
        metadatas = results['metadatas'][0]

        if not documents:
            print("❌ No matching financial records found in the Brain.")
            continue

        print(f"\n📊 [ANALYSIS FOR: {query}]")
        print("-" * 50)
        
        total_sum = 0.0
        found_records = 0

        for i in range(len(documents)):
            doc_text = documents[i]
            meta = metadatas[i]
            
            # Logic: If the query mentions a specific company, filter the results
            # (e.g., 'IICC' or 'ITMC')
            amount = extract_amount(doc_text)
            total_sum += amount
            found_records += 1
            
            print(f"📍 {doc_text}")

        print("-" * 50)
        print(f"📈 Total identified in these records: {total_sum:,.2f} SAR")
        print(f"𝌐 Source count: {found_records} matching entries found.")

if __name__ == "__main__":
    try:
        query_financial_intelligence()
    except KeyboardInterrupt:
        print("\n👋 Financial Analyst session ended.")
