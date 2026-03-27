import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. Load Environment Variables (including HF_TOKEN, ERP, and CF keys)
load_dotenv()

# Set Hugging Face Token for the environment before importing AI modules
if os.getenv("HF_TOKEN"):
    os.environ["HUGGINGFACE_HUB_TOKEN"] = os.getenv("HF_TOKEN")

# 2. Import your local CEO Intel Logic
sys.path.append(os.path.join(os.getcwd(), 'src'))
from ceo_intel_agent import CEOIntelAgent

# 3. Initialize FastAPI and the AI Agent
app = FastAPI(title="IICC Group Intelligence API")
agent = CEOIntelAgent()

# Create static directory if it doesn't exist
if not os.path.exists("static"):
    os.makedirs("static")

# Mount the static folder to serve index.html and assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. Data Models
class QueryRequest(BaseModel):
    prompt: str

# 5. API Routes

@app.get("/")
async def read_index():
    """Serves the CEO Dashboard UI."""
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "IICC AI Online. Dashboard (index.html) not found in /static."}

@app.get("/health")
def health_check():
    """System diagnostic for the Madinah Host."""
    return {
        "status": "active",
        "host": "Madinah_OptiPlex_7010",
        "sectors_indexed": 16,
        "llm_engine": "Ollama/Llama3"
    }

@app.post("/ask")
async def ask_ceo_agent(request: QueryRequest):
    """The main intelligence endpoint."""
    try:
        # Step A: Intent Detection & Search (via ChromaDB)
        query = request.prompt
        results = agent.memory.search(query, n_results=5)
        raw_docs = results['documents'][0]
        metadatas = results['metadatas'][0]

        # Step B: Synthesize human-like response via Ollama
        # This calls the method we added to ceo_intel_agent.py
        smart_answer = agent.synthesize_with_ollama(query, raw_docs)

        # Step C: Return structured intelligence
        return {
            "answer": smart_answer,
            "sources": metadatas,
            "is_financial": any(w in query.lower() for w in agent.fin_keywords)
        }
    except Exception as e:
        print(f"❌ API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Listen on all interfaces so your Samsung device can connect via IP
    uvicorn.run(app, host="0.0.0.0", port=8000)
