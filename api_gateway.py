from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Ensure we can see our local logic
sys.path.append(os.path.join(os.getcwd(), 'src'))
from ceo_intel_agent import CEOIntelAgent

app = FastAPI(title="IICC Group Intelligence API")
agent = CEOIntelAgent()

class QueryRequest(BaseModel):
    prompt: str

@app.get("/")
def health_check():
    return {"status": "online", "sectors": 16, "location": "Madinah Host"}

@app.post("/ask")
async def ask_ceo_agent(request: QueryRequest):
    # This uses the Master Logic we built (ChromaDB + Ollama)
    raw_results = agent.memory.search(request.prompt, n_results=5)
    
    # Generate the "Smart" answer
    smart_answer = agent.synthesize_with_ollama(request.prompt, raw_results['documents'][0])
    
    return {
        "answer": smart_answer,
        "sources": raw_results['metadatas'][0],
        "intent": "financial" if any(w in request.prompt.lower() for w in agent.fin_keywords) else "general"
    }

if __name__ == "__main__":
    import uvicorn
    # Run on 0.0.0.0 so you can access it from your mobile device via the local IP
    uvicorn.run(app, host="0.0.0.0", port=8002)
# Mount the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')
