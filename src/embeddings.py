import os
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
load_dotenv()

# This tells the huggingface_hub library to use your token automatically
if os.getenv("HF_TOKEN"):
    os.environ["HUGGINGFACE_HUB_TOKEN"] = os.getenv("HF_TOKEN")
class AgentMemory:
    def __init__(self):
        # Local path for the Vector Database
        self.db_path = os.path.join(os.getcwd(), "data", "logs_vector_db")
        os.makedirs(self.db_path, exist_ok=True)
        
        # Initialize ChromaDB (Local Persist)
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Self-hosted model (runs on your Proxmox/Ubuntu host)
        print("🧠 Loading all-MiniLM-L6-v2 model...")
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Create or Get the collection
        self.collection = self.client.get_or_create_collection(name="iicc_intelligence")
        print("✅ AI Memory Engine Ready.")

    def save_entity(self, category, entity_id, text_content, metadata=None):
        """
        The core storage method for all business knowledge.
        category: 'SECTOR', 'FINANCE', 'DOCUMENT', etc.
        """
        if metadata is None:
            metadata = {}
            
        # Add basic tracking to metadata
        metadata.update({
            "category": category,
            "id": entity_id
        })

        # Generate embedding locally
        embedding = self.model.encode(text_content).tolist()

        # Save to the local Vector DB
        self.collection.add(
            embeddings=[embedding],
            documents=[text_content],
            metadatas=[metadata],
            ids=[f"{category}_{entity_id}"]
        )

    def search(self, query, n_results=3):
        """Search the Brain for answers."""
        query_embedding = self.model.encode(query).tolist()
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
# src/embeddings.py

    def save_entity(self, category, entity_id, text_content, metadata=None):
        """The core storage method for all business knowledge."""
        if metadata is None:
            metadata = {}
            
        # Add basic tracking
        metadata.update({
            "category": str(category),
            "id": str(entity_id)
        })

        # --- SANITIZATION STEP ---
        # ChromaDB metadatas only allow: str, int, float, bool.
        # This loop converts everything else (like None) to an empty string.
        clean_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                clean_metadata[key] = value
            else:
                clean_metadata[key] = str(value) if value is not None else ""

        # Generate embedding locally
        embedding = self.model.encode(text_content).tolist()

        # Save to the local Vector DB
        try:
            self.collection.add(
                embeddings=[embedding],
                documents=[text_content],
                metadatas=[clean_metadata],  # Using sanitized version
                ids=[f"{category}_{entity_id}"]
            )
        except Exception as e:
            print(f"⚠️ Failed to save {entity_id}: {e}")
