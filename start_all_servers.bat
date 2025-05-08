@echo off
echo Starting all MCP servers...

start "Context7" cmd /k ".\start_context7.bat"
start "Exa Search" cmd /k ".\start_exa.bat"
start "Taskmaster" cmd /k ".\start_taskmaster.bat"
start "Memory" cmd /k ".\start_memory.bat"
start "Knowledge" cmd /k ".\start_knowledge.bat"
start "MCP-use" cmd /k ".\start_mcp_use.bat"

echo All MCP servers started in separate windows.
echo Press any key to close all servers...
pause > nul

echo Closing all MCP servers...
taskkill /FI "WINDOWTITLE eq Context7*" /T /F
taskkill /FI "WINDOWTITLE eq Exa Search*" /T /F
taskkill /FI "WINDOWTITLE eq Taskmaster*" /T /F
taskkill /FI "WINDOWTITLE eq Memory*" /T /F
taskkill /FI "WINDOWTITLE eq Knowledge*" /T /F
taskkill /FI "WINDOWTITLE eq MCP-use*" /T /F
echo All MCP servers closed.
