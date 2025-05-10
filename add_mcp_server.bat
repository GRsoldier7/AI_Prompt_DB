@echo off
echo ==================================================
echo ADD NEW MCP SERVER TO CONFIGURATION
echo ==================================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Run the add MCP server script
node add_mcp_server.js

REM If the script exits, wait for user input
echo.
pause
