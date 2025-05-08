@echo off
setlocal

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.6 or higher.
    exit /b 1
)

REM Check if the virtual environment exists, if not create it
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    pip install flask
) else (
    call venv\Scripts\activate
)

REM Set OpenRouter API key and model if not already set
if "%OPENROUTER_API_KEY%"=="" (
    set /p OPENROUTER_API_KEY=Enter your OpenRouter API key: 
)

if "%OPENROUTER_MODEL%"=="" (
    set /p OPENROUTER_MODEL=Enter your OpenRouter model (default: anthropic/claude-3-opus-20240229): 
    if "%OPENROUTER_MODEL%"=="" set OPENROUTER_MODEL=anthropic/claude-3-opus-20240229
)

REM Run the web interface
echo Starting web interface...
echo Open your browser and go to http://localhost:5000
python web_interface.py

endlocal
