import sys
import os
sys.path.append('src')
from embeddings import AgentMemory
from document_loader import ingest_docs

def ask_business_intel(query):
    memory = AgentMemory()
    
    # Search the Local Vector DB
    results = memory.collection.query(
        query_embeddings=[memory.model.encode(query).tolist()],
        n_results=3
    )
    
    print(f"\n💡 [AGENT RESPONSE for: {query}]")
    for i, doc in enumerate(results['documents'][0]):
        source = results['metadatas'][0][i].get('source', 'ERP System')
        print(f"\n--- Source: {source} ---")
        print(doc)

if __name__ == "__main__":
    # 1. First, re-index new documents (Optional)
    # ingest_docs(AgentMemory())
    
    # 2. Ask a question
    user_q = input("What would you like to know about the company? ")
    ask_business_intel(user_q)
