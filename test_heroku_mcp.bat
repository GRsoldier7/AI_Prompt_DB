@echo off
echo ==================================================
echo HEROKU MCP SERVER TEST SUITE
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

REM Check if Heroku CLI is installed
where heroku >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Heroku CLI is not installed or not in PATH
    echo Please install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

REM Check if HEROKU_API_KEY is set
if "%HEROKU_API_KEY%"=="" (
    echo Warning: HEROKU_API_KEY environment variable is not set
    echo You can get a token by running: heroku authorizations:create
    
    REM Try to get a token automatically
    echo Attempting to get a Heroku API token automatically...
    for /f "tokens=*" %%a in ('heroku auth:token 2^>nul') do set HEROKU_API_KEY=%%a
    
    if "%HEROKU_API_KEY%"=="" (
        echo Could not get a token automatically.
        echo Please set HEROKU_API_KEY manually or run: heroku authorizations:create
        set /p HEROKU_API_KEY=Enter your Heroku API token: 
    ) else (
        echo Successfully retrieved Heroku API token.
    )
)

REM Run the test script
echo Running Heroku MCP Server tests...
echo.
node test_heroku_mcp.js

REM If the script exits, wait for user input
echo.
pause
