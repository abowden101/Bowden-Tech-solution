@echo off
echo Starting Bowden Tech Local Grok MCP Setup...
echo.

echo Checking if Ollama is installed...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not installed. Please install Ollama from https://ollama.ai/
    pause
    exit /b 1
)

echo Pulling llama3.2:3b model (if not already available)...
ollama pull llama3.2:3b

echo.
echo Starting Ollama serve in background...
start "Ollama Serve" ollama serve

timeout /t 5 /nobreak >nul

echo.
echo Starting Bowden Tech MCP Server...
python mcp_server.py

echo.
echo Setup complete! Opening chat interface...
start http://localhost:8000/chat

pause