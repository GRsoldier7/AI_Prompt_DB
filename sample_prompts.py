#!/usr/bin/env python3
"""
Sample script to demonstrate the Prompt Management System with example prompts.
"""

import os
import sys
import subprocess
import time

# Sample prompts for different categories
SAMPLE_PROMPTS = [
    {
        "title": "Creative Story Generator",
        "text": "Write a short story about a character who discovers they have the ability to communicate with animals. Include a beginning, middle, and end. The story should have a surprising twist and a meaningful message.",
        "category": "Writing",
        "subcategory": "Creative",
        "tool": "GPT-4",
        "compatible": "Claude,Gemini",
        "tags": "creative,story,writing"
    },
    {
        "title": "Python Function Refactoring",
        "text": "Refactor the following Python function to make it more efficient, readable, and maintainable. Add appropriate comments and error handling. Explain your changes and why they improve the code.",
        "category": "Coding",
        "subcategory": "Python",
        "tool": "Claude",
        "compatible": "GPT-4,Codey",
        "tags": "coding,python,refactoring"
    },
    {
        "title": "Research Literature Review",
        "text": "Conduct a comprehensive literature review on the topic of [TOPIC]. Identify key researchers, major findings, methodologies used, and gaps in the current research. Organize the information in a structured format with sections for background, key studies, methodologies, findings, and future research directions.",
        "category": "Research",
        "subcategory": "Literature Review",
        "tool": "Claude",
        "compatible": "GPT-4",
        "tags": "research,academic,literature"
    },
    {
        "title": "Business SWOT Analysis",
        "text": "Perform a detailed SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis for a [TYPE OF BUSINESS] in the current market. For each category, provide at least 5 points with explanations. Conclude with strategic recommendations based on the analysis.",
        "category": "Business",
        "subcategory": "Strategy",
        "tool": "GPT-4",
        "compatible": "Claude,Gemini",
        "tags": "business,strategy,analysis"
    },
    {
        "title": "Technical Documentation Generator",
        "text": "Create comprehensive technical documentation for the following code snippet. Include an overview of what the code does, detailed explanations of each function/method, parameter descriptions, return value descriptions, usage examples, and potential edge cases or limitations.",
        "category": "Technical",
        "subcategory": "Documentation",
        "tool": "Claude",
        "compatible": "GPT-4,Codey",
        "tags": "technical,documentation,coding"
    }
]

def run_command(command):
    """Run a command and print the output."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result

def main():
    """Main function to add sample prompts and demonstrate functionality."""
    # Check if Python is in the path
    try:
        subprocess.run(["python", "--version"], capture_output=True, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Python is not installed or not in PATH. Please install Python 3.6 or higher.")
        sys.exit(1)
    
    # Check if the prompt_manager.py script exists
    if not os.path.exists("prompt_manager.py"):
        print("prompt_manager.py not found. Please make sure you're in the correct directory.")
        sys.exit(1)
    
    # Check for OpenRouter API key and model
    if not os.environ.get('OPENROUTER_API_KEY'):
        api_key = input("Enter your OpenRouter API key: ")
        os.environ['OPENROUTER_API_KEY'] = api_key
    
    if not os.environ.get('OPENROUTER_MODEL'):
        model = input("Enter your OpenRouter model (default: anthropic/claude-3-opus-20240229): ")
        if not model:
            model = "anthropic/claude-3-opus-20240229"
        os.environ['OPENROUTER_MODEL'] = model
    
    # Add sample prompts
    prompt_ids = []
    for i, prompt in enumerate(SAMPLE_PROMPTS):
        print(f"\n=== Adding Sample Prompt {i+1}/{len(SAMPLE_PROMPTS)} ===")
        
        # Add the prompt
        command = [
            "python", "prompt_manager.py", "add",
            "--title", prompt["title"],
            "--text", prompt["text"],
            "--category", prompt["category"],
            "--subcategory", prompt["subcategory"],
            "--tool", prompt["tool"],
            "--compatible", prompt["compatible"],
            "--tags", prompt["tags"]
        ]
        
        result = run_command(command)
        
        # Extract the prompt ID from the output
        for line in result.stdout.splitlines():
            if "Added new prompt with ID:" in line:
                prompt_id = line.split(":")[-1].strip()
                prompt_ids.append(prompt_id)
                break
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)
    
    # List all prompts
    print("\n=== Listing All Prompts ===")
    run_command(["python", "prompt_manager.py", "list"])
    
    # Filter prompts by category
    print("\n=== Filtering Prompts by Category 'Coding' ===")
    run_command(["python", "prompt_manager.py", "filter", "--category", "Coding"])
    
    # Analyze a prompt
    if prompt_ids:
        print(f"\n=== Analyzing Prompt {prompt_ids[0]} ===")
        run_command(["python", "prompt_manager.py", "analyze", "--id", prompt_ids[0]])
        
        # Improve a prompt
        print(f"\n=== Improving Prompt {prompt_ids[0]} for GPT-4 ===")
        run_command(["python", "prompt_manager.py", "improve", "--id", prompt_ids[0], "--model", "gpt-4"])
        
        # Generate variations for multiple models
        print(f"\n=== Generating Variations for Prompt {prompt_ids[0]} ===")
        run_command([
            "python", "prompt_manager.py", "variations", 
            "--id", prompt_ids[0], 
            "--models", "gpt-4,claude-3,gemini-pro"
        ])
    
    print("\n=== Sample Script Complete ===")
    print("You now have a populated prompt database with examples and improvements.")
    print("Use 'python prompt_manager.py list' to see all prompts.")

if __name__ == "__main__":
    main()
