@echo off
echo ==================================================
echo SMART MCP SERVER MANAGER
echo ==================================================
echo This script will:
echo 1. Scan all ports to find available ones
echo 2. Start all MCP servers on available ports
echo 3. Provide a clean shutdown mechanism
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

REM Check if required packages are installed
echo Checking required packages...
npm list dotenv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installing dotenv package...
    npm install dotenv
)

REM Run the smart MCP server manager
echo Starting Smart MCP Server Manager...
echo.
node smart_mcp_server.js

REM If the script exits, wait for user input
echo.
echo All MCP servers have been stopped.
pause
