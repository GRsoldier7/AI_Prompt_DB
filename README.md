# AI Prompt Database

A comprehensive tool for managing, categorizing, and optimizing AI prompts.

## Features

- **Prompt Management**: Store, retrieve, and organize prompts in a Google Sheet
- **Auto-categorization**: Automatically categorize prompts based on content
- **Effectiveness Analysis**: Rate prompts on their effectiveness
- **Prompt Improvement**: Generate improved versions of prompts
- **Batch Processing**: Process multiple prompts at once
- **Local Fallbacks**: Continue working even when API calls fail

## Commands

- `python prompt_manager.py list` - List all prompts
- `python prompt_manager.py get --id <prompt_id>` - Get details of a specific prompt
- `python prompt_manager.py add --title <title> --text <text>` - Add a new prompt
- `python prompt_manager.py update --id <prompt_id> [options]` - Update an existing prompt
- `python prompt_manager.py analyze --id <prompt_id>` - Analyze a prompt's effectiveness
- `python prompt_manager.py improve --id <prompt_id>` - Generate an improved version of a prompt
- `python prompt_manager.py variations --id <prompt_id> --models <models>` - Generate variations of a prompt
- `python prompt_manager.py process-new` - Process all new prompts
- `python prompt_manager.py auto-fill --id <prompt_id>` - Auto-fill missing information for a prompt

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file:
   ```
   OPENROUTER_API_KEY=your_api_key
   OPENROUTER_MODEL=your_preferred_model
   GOOGLE_SHEETS_ID=your_google_sheet_id
   ```
4. Run the tool: `python prompt_manager.py list`

## Requirements

- Python 3.6+
- Google Sheets API credentials
- OpenRouter API key
