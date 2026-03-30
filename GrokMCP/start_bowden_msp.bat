@echo off
title Bowden Tech Solutions - Local Grok MCP
echo ================================================
echo   Bowden Tech Solutions
echo   Orlando MSP • Local Grok MCP
echo ================================================

cd /d C:\BowdenTech\GrokMCP

echo Starting Ollama...
start "Ollama" ollama serve

timeout /t 10 /nobreak >nul

echo Starting MCP Server...
start "MCP Server" python mcp_server.py

timeout /t 3 /nobreak >nul

echo Opening Chat Interface...
start "" chat.html

echo All systems launched. Use the browser chat for MSP tasks.
pause