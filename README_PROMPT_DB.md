# Prompt Management System

A comprehensive system for managing, categorizing, and improving AI prompts using Google Sheets and OpenRouter.

## Features

- **Store prompts** in a Google Sheet with detailed metadata
- **Auto-categorize** prompts using AI
- **Analyze prompts** for effectiveness and get improvement suggestions
- **Generate improved versions** of prompts for specific AI models
- **Filter and search** prompts by category, subcategory, tool, and tags
- **Batch process** prompts to create variations for multiple models
- **Web interface** for easy management

## System Components

### 1. Google Sheet Database

The system uses a Google Sheet as the database for storing prompts with the following structure:

- **Prompt ID**: A unique identifier (e.g., P001, P002)
- **Prompt Title**: A descriptive title
- **Prompt Text**: The full text of the prompt
- **Category**: Main category (e.g., Writing, Coding, Research)
- **Subcategory**: More specific classification
- **Primary Tool**: The main tool the prompt is designed for (e.g., Claude, GPT-4)
- **Compatible Tools**: Other tools the prompt works with
- **Effectiveness Rating**: A score from 1-10 rating how well the prompt performs
- **Tags**: Keywords for additional filtering
- **Creation Date**: When the prompt was created
- **Last Modified**: When the prompt was last updated
- **Notes**: Additional information about the prompt
- **Improvement Suggestions**: Ideas for enhancing the prompt
- **Improved Versions**: Improved versions of the prompt for different models

### 2. Command-Line Interface

The system provides a command-line interface for managing prompts:

- **List** all prompts
- **Add** new prompts
- **Update** existing prompts
- **Filter** prompts by various criteria
- **Analyze** prompts for effectiveness
- **Improve** prompts for specific models
- **Generate variations** for multiple models

### 3. Web Interface

A user-friendly web interface for managing prompts with the following features:

- **Dashboard** with a list of all prompts
- **Filtering** capabilities
- **Add/Edit** forms
- **Prompt analysis** and improvement tools
- **Variation generation** for multiple models

### 4. OpenRouter Integration

The system uses OpenRouter to:

1. **Categorize prompts**: Automatically assign categories, subcategories, and tags
2. **Analyze effectiveness**: Rate prompts and provide improvement suggestions
3. **Improve prompts**: Generate enhanced versions of prompts
4. **Create variations**: Optimize prompts for different AI models

## Prerequisites

- Python 3.6 or higher
- Google Sheets API credentials (service account JSON file)
- OpenRouter API key and model

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Place your Google service account JSON file in the same directory as the script
4. Set your OpenRouter API key and model as environment variables:

```bash
# On Windows
set OPENROUTER_API_KEY=your_api_key
set OPENROUTER_MODEL=anthropic/claude-3-opus-20240229

# On macOS/Linux
export OPENROUTER_API_KEY=your_api_key
export OPENROUTER_MODEL=anthropic/claude-3-opus-20240229
```

## Usage

### Command-Line Interface

#### Using the Batch Script (Windows)

On Windows, you can use the provided batch script for easier execution:

```bash
prompt_manager.bat [command] [options]
```

#### Using the Shell Script (macOS/Linux)

On macOS/Linux, you can use the provided shell script:

```bash
./prompt_manager.sh [command] [options]
```

#### Commands

##### List all prompts

```bash
python prompt_manager.py list
```

##### Add a new prompt

```bash
python prompt_manager.py add --title "My Prompt" --text "This is a prompt for generating creative stories" --category "Writing" --subcategory "Creative" --tool "GPT-4" --compatible "Claude,Gemini" --tags "creative,story,writing"
```

To automatically categorize the prompt:

```bash
python prompt_manager.py add --title "My Prompt" --text "This is a prompt for generating creative stories" --auto-categorize
```

##### Update an existing prompt

```bash
python prompt_manager.py update --id P001 --title "Updated Title" --text "Updated prompt text"
```

##### Filter prompts

```bash
python prompt_manager.py filter --category "Writing" --tags "creative,story"
```

##### Analyze a prompt for effectiveness

```bash
python prompt_manager.py analyze --id P001
```

##### Improve a prompt for a specific model

```bash
python prompt_manager.py improve --id P001 --model "gpt-4"
```

##### Generate variations for multiple models

```bash
python prompt_manager.py variations --id P001 --models "gpt-4,claude-3,gemini-pro"
```

### Web Interface

To start the web interface:

#### On Windows

```bash
run_web_interface.bat
```

#### On macOS/Linux

```bash
./run_web_interface.sh
```

Then open your browser and go to http://localhost:5000

The web interface provides the following features:

- **Home page**: List of all prompts with filtering options
- **View prompt**: Detailed view of a prompt with all metadata
- **Add prompt**: Form to add a new prompt
- **Edit prompt**: Form to edit an existing prompt
- **Analyze prompt**: Analyze a prompt for effectiveness
- **Improve prompt**: Generate an improved version of a prompt for a specific model
- **Generate variations**: Create variations of a prompt for multiple models

### Sample Prompts

To populate your database with sample prompts:

```bash
python sample_prompts.py
```

This will add several example prompts across different categories and demonstrate the various features of the system.

## Customization

### Adding New Categories

The system automatically learns categories as you add them. You can also modify the categorization logic in the `OpenRouterClient.categorize_prompt` method.

### Adding New Models

To add support for new models, update the model lists in the web interface templates and the `OpenRouterClient.generate_variations` method.

### Extending the Schema

To add new fields to the prompt schema:

1. Update the `COLUMNS` list in `prompt_manager.py`
2. Update the Google Sheet structure
3. Modify the relevant functions in the `PromptDB` class
4. Update the web interface templates

## Troubleshooting

### Authentication Issues

- Make sure your service account JSON file is in the correct location
- Verify that the service account has access to the Google Sheet
- Check that the spreadsheet ID is correct

### API Errors

- Verify that your OpenRouter API key is valid
- Check that the model you specified is available
- Look for error messages in the console output

### Rate Limiting

- If you're processing many prompts, add delays between API calls
- Consider batching requests to avoid hitting rate limits

## Future Enhancements

- **Bulk import/export**: Add support for importing and exporting prompts in various formats
- **Version history**: Track changes to prompts over time
- **Collaboration features**: Allow multiple users to work on the same prompt database
- **Advanced analytics**: Provide insights into prompt effectiveness across different models
- **Integration with other AI platforms**: Add support for directly testing prompts with different AI models

## License

This project is licensed under the MIT License - see the LICENSE file for details.
