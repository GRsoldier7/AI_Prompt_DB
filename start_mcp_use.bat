@echo off
echo Starting MCP-use server...
pip install mcp_use fastembed
python -m mcp_use.cli
