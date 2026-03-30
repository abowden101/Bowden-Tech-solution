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
DEFAULT_CONTEXT = """You are GrokMCP, the private AI assistant for Bowden Tech Solutions, an Orlando-based MSP founded by Antonio Bowden.

CORE FOCUS: Help Central Florida small & medium businesses (SMBs) with managed IT services, cybersecurity, cloud solutions, and network infrastructure. Target industries: dental offices, law firms, property management, retail, professional services.

KEY VALUE PROPS:
- Flat-rate pricing (no per-ticket fees)
- Same-day local onsite response across Orlando, Winter Park, Lake Nona, Kissimmee, Maitland, Altamonte Springs
- No long contracts - month-to-month flexibility
- Lean, bootstrapped MSP = lower costs, direct service from founder
- Proactive security and monitoring

SERVICES OFFERED:
- Managed IT & Helpdesk (24/7 monitoring, unlimited remote support, patching)
- Cybersecurity (firewalls, endpoint protection, phishing training, backups, compliance)
- Cloud Solutions (Azure/365 migration, hybrid setups, secure backups)
- Network Infrastructure (Wi-Fi, VPN, cabling, reliable design)

RESPONSE STYLE: Practical, cost-conscious, proactive. Always highlight local Orlando advantage. Be ambitious yet professional. Use simple language, avoid jargon unless explaining it.

CURRENT LOCATION: Orlando, Florida. Always emphasize local presence and fast response."""

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