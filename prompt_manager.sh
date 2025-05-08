#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

# Check if the virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Set OpenRouter API key and model if not already set
if [ -z "$OPENROUTER_API_KEY" ]; then
    read -p "Enter your OpenRouter API key: " OPENROUTER_API_KEY
    export OPENROUTER_API_KEY
fi

if [ -z "$OPENROUTER_MODEL" ]; then
    read -p "Enter your OpenRouter model (default: anthropic/claude-3-opus-20240229): " OPENROUTER_MODEL
    if [ -z "$OPENROUTER_MODEL" ]; then
        OPENROUTER_MODEL="anthropic/claude-3-opus-20240229"
    fi
    export OPENROUTER_MODEL
fi

# Run the prompt manager with the provided arguments
python3 prompt_manager.py "$@"
