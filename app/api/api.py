import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure Python can find your 'app' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.agents.analyzer_agent_ import FeasiblityAgent

app = FastAPI(title="CodeReuse Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize your agent
print("="*60)
print("🚀 Starting the Code Reuse Feasibility API! 🚀")
print("="*60)
try:
    agent = FeasiblityAgent(use_gemini_embeddings=False)
except Exception as e:
    print(f"❌ Failed to initialize the Agent: {e}")
    agent = None

class AnalyzeRequest(BaseModel):
    query: str
    repo: str = "All repositories"
    tech: str = "Python / FastAPI"

@app.post("/api/analyze")
async def analyze_codebase(req: AnalyzeRequest):
    print(f"\n🧠 Thinking... Searching codebase and writing report for: '{req.query}'")
    if not agent:
        return JSONResponse(content={"error": "Agent not initialized."})
    
    result = agent.analyze(req.query, as_json=True)
    return JSONResponse(content=result)

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🌐 Web interface running at: http://localhost:8000")
    print("="*60 + "\n")
    uvicorn.run("app.api.api:app", host="0.0.0.0", port=8000, reload=True)
