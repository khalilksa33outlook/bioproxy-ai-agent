import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from embeddings import AgentMemory

def query_group_info():
    memory = AgentMemory()
    print("\n🏢 [IICC GROUP INTELLIGENCE CENTER]")
    print("Ask about: Company History, Policies, Sectors, or General Info.")

    while True:
        query = input("\n🧐 Question: ")
        if query.lower() in ['exit', 'quit']: break

        # Search the Brain - specifically looking for DOCUMENT and SECTOR categories
        results = memory.search(query, n_results=5)

        print(f"\n📖 [RELEVANT INFORMATION FOUND]:")
        print("-" * 50)
        
        for i in range(len(results['documents'][0])):
            doc_text = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            category = meta.get('category', 'GENERAL')
            
            # Highlight where the info came from
            source = meta.get('source', meta.get('id', 'Internal Knowledge'))
            print(f"📍 SOURCE: [{category}] - {source}")
            print(f"Content: {doc_text}\n")

if __name__ == "__main__":
    query_group_info()
