from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import ollama
from typing import Optional
import os

app = FastAPI(title="Bowden Tech Local Grok MCP - Orlando MSP")

class MCPQuery(BaseModel):
    prompt: str
    context: Optional[str] = None

# Default MSP-tuned system prompt
DEFAULT_CONTEXT = """You are GrokMCP, the private AI assistant for Bowden Tech Solutions, an Orlando-based MSP.

Mission: We deliver reliable, affordable managed IT services and cybersecurity to small and medium businesses across Central Florida. 
We provide fast same-day local response, transparent flat-rate pricing, and proactive technology support so our clients can focus on growing their business.

Key strengths:
- Same-day onsite response in Orlando, Winter Park, Lake Nona, Kissimmee, Maitland & Altamonte Springs
- Honest flat-rate monthly pricing with no long contracts
- Founder-led by Antonio Bowden (Network & Security Engineer)
- Focus on practical, cost-conscious solutions for dental offices, law firms, property management, and other Central Florida SMBs

Always be helpful, proactive, and emphasize local advantage."""

@app.post("/mcp/query")
async def query_mcp(q: MCPQuery):
    try:
        system_prompt = q.context or DEFAULT_CONTEXT
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': q.prompt}
            ]
        )
        return {"status": "success", "response": response['message']['content']}
    except Exception as e:
        return {"status": "error", "response": str(e)}

@app.get("/health")
async def health():
    return {"status": "Bowden Tech Local Grok MCP is online 🚀 | Orlando MSP Edition"}

@app.get("/chat", response_class=HTMLResponse)
async def get_chat():
    chat_html_path = os.path.join(os.path.dirname(__file__), "chat.html")
    try:
        with open(chat_html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Chat interface not found</h1>"

if __name__ == "__main__":
    print("🚀 Starting Bowden Tech Local Grok MCP on http://localhost:8000")
    print("Chat interface: http://localhost:8000/chat")
    print("Keep Ollama serve running in another window.")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)