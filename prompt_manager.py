#!/usr/bin/env python3
"""
Prompt Management System

This script provides functionality to manage prompts in a Google Sheet and leverage
OpenRouter to categorize and improve prompts for different AI models.
"""

import os
import sys
import json
import datetime
import time
import argparse
import pandas as pd
import requests
from typing import List, Dict, Any, Optional, Union
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'n8n-integrations-452015-811dc210bea2.json'
SPREADSHEET_ID = '1gBM_HxkjCrlBhmHT7i0CZoEpdKRkJa9ZGjd2xX3755M'
SHEET_NAME = 'Prompts'

# Column definitions
COLUMNS = [
    'Prompt ID', 'Prompt Title', 'Prompt Text', 'Category', 'Subcategory',
    'Primary Tool', 'Compatible Tools', 'Effectiveness Rating', 'Tags',
    'Creation Date', 'Last Modified', 'Notes', 'Improvement Suggestions',
    'Improved Versions'
]

# OpenRouter configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"  # Best free model for prompt categorization and improvement

class OpenRouterClient:
    """Client for interacting with the OpenRouter API."""

    def __init__(self, api_key: str, model: str):
        """Initialize the OpenRouter client with API key and model."""
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://promptdb.local",  # Replace with your actual domain
            "X-Title": "Prompt Management System"
        }

    def categorize_prompt(self, prompt_text: str) -> Dict[str, Any]:
        """
        Use OpenRouter to categorize a prompt.

        Returns a dictionary with suggested category, subcategory, and tags.
        """
        system_message = """
        You are an expert at analyzing and categorizing AI prompts. Your task is to analyze the given prompt
        and determine the most appropriate category, subcategory, and tags for it. Respond in JSON format only.

        Categories should be one of: Writing, Coding, Research, Creative, Business, Education, Personal, Technical, Other

        Subcategories should be more specific classifications within the main category.

        Tags should be relevant keywords that describe the prompt's content or purpose.
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Analyze and categorize this prompt: {prompt_text}"}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(OPENROUTER_API_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Extract the JSON response from the model
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
            categorization = json.loads(content)

            return {
                "Category": categorization.get("category", ""),
                "Subcategory": categorization.get("subcategory", ""),
                "Tags": ", ".join(categorization.get("tags", []))
            }

        except Exception as e:
            print(f"Error categorizing prompt: {e}")
            return {"Category": "", "Subcategory": "", "Tags": ""}

    def improve_prompt(self, prompt_text: str, target_model: str = None) -> str:
        """
        Use OpenRouter to improve a prompt for a specific model.

        Args:
            prompt_text: The original prompt text
            target_model: The model to optimize the prompt for (e.g., "gpt-4", "claude-3")

        Returns:
            Improved prompt text
        """
        target_model = target_model or "general"

        system_message = f"""
        You are an expert at improving prompts for AI models. Your task is to enhance the given prompt
        to make it more effective, clear, and likely to produce better results specifically for {target_model}.

        Consider the following in your improvements:
        1. Clarity and specificity
        2. Proper context and background information
        3. Clear instructions and expectations
        4. Appropriate formatting and structure
        5. Removal of ambiguities

        Respond with ONLY the improved prompt text, without explanations or commentary.
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Improve this prompt for {target_model}: {prompt_text}"}
        ]

        payload = {
            "model": self.model,
            "messages": messages
        }

        try:
            response = requests.post(OPENROUTER_API_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Extract the improved prompt
            improved_prompt = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return improved_prompt

        except Exception as e:
            print(f"Error improving prompt: {e}")
            return prompt_text

    def analyze_prompt_effectiveness(self, prompt_text: str) -> Dict[str, Any]:
        """
        Analyze the effectiveness of a prompt and provide suggestions for improvement.

        Returns a dictionary with rating and improvement suggestions.
        """
        system_message = """
        You are an expert at analyzing AI prompts. Your task is to evaluate the given prompt
        for effectiveness and provide specific suggestions for improvement. Respond in JSON format only.

        Include the following in your analysis:
        1. A numerical rating from 1-10
        2. Specific suggestions for improvement
        3. Strengths of the prompt
        4. Weaknesses of the prompt
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Analyze this prompt for effectiveness: {prompt_text}"}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(OPENROUTER_API_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Extract the JSON response from the model
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
            analysis = json.loads(content)

            return {
                "Effectiveness Rating": str(analysis.get("rating", "")),
                "Improvement Suggestions": analysis.get("suggestions", ""),
                "Notes": f"Strengths: {analysis.get('strengths', '')}\nWeaknesses: {analysis.get('weaknesses', '')}"
            }

        except Exception as e:
            print(f"Error analyzing prompt: {e}")
            return {"Effectiveness Rating": "", "Improvement Suggestions": "", "Notes": ""}

    def generate_variations(self, prompt_text: str, models: List[str]) -> Dict[str, str]:
        """
        Generate variations of a prompt optimized for different models.

        Args:
            prompt_text: The original prompt text
            models: List of model names to optimize for

        Returns:
            Dictionary mapping model names to optimized prompts
        """
        variations = {}

        for model in models:
            print(f"Generating variation for {model}...")
            improved = self.improve_prompt(prompt_text, model)
            variations[model] = improved
            # Add a small delay to avoid rate limiting
            time.sleep(1)

        return variations

class PromptDB:
    """Class to manage the prompt database in Google Sheets."""

    def __init__(self, service_account_file: str = SERVICE_ACCOUNT_FILE,
                 spreadsheet_id: str = SPREADSHEET_ID,
                 sheet_name: str = SHEET_NAME):
        """Initialize the PromptDB with Google Sheets credentials."""
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name

        try:
            # Authenticate with Google Sheets API
            credentials = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=SCOPES)
            self.service = build('sheets', 'v4', credentials=credentials)
            self.sheet = self.service.spreadsheets()

            # Check if the sheet exists, if not create it
            self._initialize_sheet()

            print(f"Successfully connected to Google Sheet: {spreadsheet_id}")
        except Exception as e:
            print(f"Error initializing PromptDB: {e}")
            sys.exit(1)

    def _initialize_sheet(self):
        """Initialize the sheet with headers if it doesn't exist."""
        try:
            # Check if the sheet exists
            sheet_metadata = self.sheet.get(spreadsheetId=self.spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', [])
            sheet_exists = False

            for sheet in sheets:
                if sheet['properties']['title'] == self.sheet_name:
                    sheet_exists = True
                    break

            if not sheet_exists:
                # Create the sheet
                request = {
                    'addSheet': {
                        'properties': {
                            'title': self.sheet_name
                        }
                    }
                }
                self.sheet.batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={'requests': [request]}
                ).execute()

                # Add headers
                self.sheet.values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{self.sheet_name}!A1:N1",
                    valueInputOption="RAW",
                    body={
                        "values": [COLUMNS]
                    }
                ).execute()

                # Format headers (make bold)
                request = {
                    "repeatCell": {
                        "range": {
                            "sheetId": self._get_sheet_id(),
                            "startRowIndex": 0,
                            "endRowIndex": 1
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "textFormat": {"bold": True}
                            }
                        },
                        "fields": "userEnteredFormat.textFormat.bold"
                    }
                }
                self.sheet.batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={'requests': [request]}
                ).execute()

                print(f"Created new sheet: {self.sheet_name}")

        except HttpError as error:
            print(f"Error initializing sheet: {error}")
            sys.exit(1)

    def _get_sheet_id(self) -> int:
        """Get the sheet ID for the current sheet."""
        sheet_metadata = self.sheet.get(spreadsheetId=self.spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])

        for sheet in sheets:
            if sheet['properties']['title'] == self.sheet_name:
                return sheet['properties']['sheetId']

        raise ValueError(f"Sheet {self.sheet_name} not found")

    def _get_next_id(self) -> str:
        """Generate the next available Prompt ID."""
        data = self.get_all_prompts()

        if not data:
            return "P001"

        # Extract existing IDs and find the highest number
        ids = [row.get('Prompt ID', 'P000') for row in data]
        max_id = max(ids, key=lambda x: int(x[1:]) if x[1:].isdigit() else 0)

        # Generate next ID
        next_num = int(max_id[1:]) + 1
        return f"P{next_num:03d}"

    def get_all_prompts(self) -> List[Dict[str, Any]]:
        """Retrieve all prompts from the sheet."""
        try:
            result = self.sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A:N"
            ).execute()

            values = result.get('values', [])

            if not values:
                return []

            # Check if headers exist
            if len(values) >= 1:
                headers = values[0]
                # Check if headers match expected columns
                if 'Prompt ID' not in headers and len(headers) > 0:
                    # Headers don't match expected format, try to map them
                    print("Headers don't match expected format. Attempting to map...")
                    # Create a mapping from existing headers to expected headers
                    header_mapping = {}
                    for i, header in enumerate(headers):
                        if header.lower() in [col.lower() for col in COLUMNS]:
                            # Direct match (case-insensitive)
                            header_mapping[i] = header
                        elif 'title' in header.lower() or 'name' in header.lower():
                            header_mapping[i] = 'Prompt Title'
                        elif 'text' in header.lower() or 'content' in header.lower() or 'prompt' in header.lower():
                            header_mapping[i] = 'Prompt Text'
                        elif 'category' in header.lower():
                            header_mapping[i] = 'Category'
                        elif 'subcategory' in header.lower() or 'sub' in header.lower():
                            header_mapping[i] = 'Subcategory'
                        elif 'tool' in header.lower() and 'primary' in header.lower():
                            header_mapping[i] = 'Primary Tool'
                        elif 'tool' in header.lower() and 'compatible' in header.lower():
                            header_mapping[i] = 'Compatible Tools'
                        elif 'rating' in header.lower() or 'effectiveness' in header.lower():
                            header_mapping[i] = 'Effectiveness Rating'
                        elif 'tag' in header.lower():
                            header_mapping[i] = 'Tags'
                        elif 'create' in header.lower() or 'date' in header.lower():
                            header_mapping[i] = 'Creation Date'
                        elif 'modified' in header.lower() or 'update' in header.lower():
                            header_mapping[i] = 'Last Modified'
                        elif 'note' in header.lower():
                            header_mapping[i] = 'Notes'
                        elif 'suggestion' in header.lower() or 'improve' in header.lower():
                            header_mapping[i] = 'Improvement Suggestions'
                        elif 'version' in header.lower():
                            header_mapping[i] = 'Improved Versions'

                    # Create new headers based on mapping
                    new_headers = []
                    for i in range(len(headers)):
                        if i in header_mapping:
                            new_headers.append(header_mapping[i])
                        else:
                            new_headers.append(headers[i])

                    # Add Prompt ID if it doesn't exist
                    if 'Prompt ID' not in new_headers:
                        new_headers.insert(0, 'Prompt ID')

                    # Update the sheet with the new headers
                    self.sheet.values().update(
                        spreadsheetId=self.spreadsheet_id,
                        range=f"{self.sheet_name}!A1",
                        valueInputOption="RAW",
                        body={
                            "values": [new_headers]
                        }
                    ).execute()

                    # Add a delay to avoid quota limits
                    time.sleep(1)

                    # Add Prompt IDs to existing data
                    data = []
                    for i, row in enumerate(values[1:]):
                        prompt_id = f"P{i+1:03d}"
                        # Pad row if it's shorter than headers
                        padded_row = row + [''] * (len(new_headers) - len(row) - 1)
                        # Insert Prompt ID at the beginning
                        padded_row.insert(0, prompt_id)
                        data.append(dict(zip(new_headers, padded_row)))

                    # Update the sheet with the new data
                    for i, prompt in enumerate(data):
                        row_data = []
                        for header in new_headers:
                            row_data.append(prompt.get(header, ''))

                        self.sheet.values().update(
                            spreadsheetId=self.spreadsheet_id,
                            range=f"{self.sheet_name}!A{i+2}",
                            valueInputOption="RAW",
                            body={
                                "values": [row_data]
                            }
                        ).execute()

                        # Add a delay to avoid quota limits
                        time.sleep(1)

                    return data
                else:
                    # Headers match expected format
                    data = []
                    for i, row in enumerate(values[1:]):
                        # Check if Prompt ID exists
                        if len(row) > 0 and row[0]:
                            prompt_id = row[0]
                        else:
                            prompt_id = f"P{i+1:03d}"
                            # Update the Prompt ID in the sheet
                            self.sheet.values().update(
                                spreadsheetId=self.spreadsheet_id,
                                range=f"{self.sheet_name}!A{i+2}",
                                valueInputOption="RAW",
                                body={
                                    "values": [[prompt_id]]
                                }
                            ).execute()

                            # Add a delay to avoid quota limits
                            time.sleep(1)

                        # Pad row if it's shorter than headers
                        padded_row = row + [''] * (len(headers) - len(row))
                        # Make sure Prompt ID is set
                        padded_row[0] = prompt_id
                        data.append(dict(zip(headers, padded_row)))

                    return data

            return []

        except HttpError as error:
            print(f"Error retrieving prompts: {error}")
            return []

    def add_prompt(self, prompt_data: Dict[str, Any]) -> str:
        """
        Add a new prompt to the database.

        Returns the ID of the newly added prompt.
        """
        try:
            # Generate a new ID
            prompt_id = self._get_next_id()

            # Set creation and modification dates
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")

            # Prepare row data
            row_data = [
                prompt_id,
                prompt_data.get('Prompt Title', ''),
                prompt_data.get('Prompt Text', ''),
                prompt_data.get('Category', ''),
                prompt_data.get('Subcategory', ''),
                prompt_data.get('Primary Tool', ''),
                prompt_data.get('Compatible Tools', ''),
                prompt_data.get('Effectiveness Rating', ''),
                prompt_data.get('Tags', ''),
                current_date,  # Creation Date
                current_date,  # Last Modified
                prompt_data.get('Notes', ''),
                prompt_data.get('Improvement Suggestions', ''),
                prompt_data.get('Improved Versions', '')
            ]

            # Append to sheet
            self.sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A:N",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={
                    "values": [row_data]
                }
            ).execute()

            print(f"Added new prompt with ID: {prompt_id}")
            return prompt_id

        except HttpError as error:
            print(f"Error adding prompt: {error}")
            return ""

    def update_prompt(self, prompt_id: str, prompt_data: Dict[str, Any]) -> bool:
        """Update an existing prompt."""
        try:
            # Get all prompts
            prompts = self.get_all_prompts()

            # Find the prompt with the given ID
            row_index = None
            prompt_index = None
            for i, prompt in enumerate(prompts):
                if prompt.get('Prompt ID') == prompt_id:
                    row_index = i + 2  # +2 because of 0-indexing and header row
                    prompt_index = i
                    break

            if row_index is None:
                print(f"Prompt with ID {prompt_id} not found")
                return False

            # Update the last modified date
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            prompt_data['Last Modified'] = current_date

            # Prepare row data
            row_data = [
                prompt_id,
                prompt_data.get('Prompt Title', prompts[prompt_index].get('Prompt Title', '')),
                prompt_data.get('Prompt Text', prompts[prompt_index].get('Prompt Text', '')),
                prompt_data.get('Category', prompts[prompt_index].get('Category', '')),
                prompt_data.get('Subcategory', prompts[prompt_index].get('Subcategory', '')),
                prompt_data.get('Primary Tool', prompts[prompt_index].get('Primary Tool', '')),
                prompt_data.get('Compatible Tools', prompts[prompt_index].get('Compatible Tools', '')),
                prompt_data.get('Effectiveness Rating', prompts[prompt_index].get('Effectiveness Rating', '')),
                prompt_data.get('Tags', prompts[prompt_index].get('Tags', '')),
                prompts[prompt_index].get('Creation Date', ''),  # Keep original creation date
                current_date,  # Update last modified
                prompt_data.get('Notes', prompts[prompt_index].get('Notes', '')),
                prompt_data.get('Improvement Suggestions', prompts[prompt_index].get('Improvement Suggestions', '')),
                prompt_data.get('Improved Versions', prompts[prompt_index].get('Improved Versions', ''))
            ]

            # Add a delay to avoid quota limits
            time.sleep(1)

            # Update the row
            self.sheet.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A{row_index}:N{row_index}",
                valueInputOption="RAW",
                body={
                    "values": [row_data]
                }
            ).execute()

            print(f"Updated prompt with ID: {prompt_id}")
            return True

        except HttpError as error:
            print(f"Error updating prompt: {error}")
            return False

    def get_prompt(self, prompt_id: str) -> Dict[str, Any]:
        """Get a specific prompt by ID."""
        prompts = self.get_all_prompts()

        for prompt in prompts:
            if prompt.get('Prompt ID') == prompt_id:
                # Print the prompt details in a nicely formatted way
                print(f"\n{'=' * 80}")
                print(f"PROMPT: {prompt.get('Prompt Title', 'Untitled')} (ID: {prompt_id})")
                print(f"{'=' * 80}")

                # Print metadata in a clean format
                print(f"\n{'-' * 30} METADATA {'-' * 30}")
                metadata_fields = ['Category', 'Subcategory', 'Primary Tool', 'Compatible Tools',
                                  'Effectiveness Rating', 'Tags', 'Creation Date', 'Last Modified']
                for field in metadata_fields:
                    if prompt.get(field):
                        print(f"{field:20}: {prompt.get(field)}")

                # Print the prompt text with proper formatting
                print(f"\n{'-' * 30} PROMPT TEXT {'-' * 30}")
                prompt_text = prompt.get('Prompt Text', '')
                # Format the prompt text for better readability
                formatted_text = self._format_text_for_display(prompt_text)
                print(formatted_text)

                # Print analysis if available
                if prompt.get('Notes') or prompt.get('Improvement Suggestions'):
                    print(f"\n{'-' * 30} ANALYSIS {'-' * 30}")
                    if prompt.get('Notes'):
                        print(f"Notes: {prompt.get('Notes')}")
                    if prompt.get('Improvement Suggestions'):
                        print("\nImprovement Suggestions:")
                        suggestions = prompt.get('Improvement Suggestions', '').split('\n')
                        for suggestion in suggestions:
                            if suggestion.strip():
                                print(f"• {suggestion.strip()}")

                # Print improved versions if available
                if prompt.get('Improved Versions'):
                    print(f"\n{'-' * 30} IMPROVED VERSIONS {'-' * 30}")
                    improved_versions = prompt.get('Improved Versions', '')
                    # Format the improved versions for better readability
                    formatted_versions = self._format_improved_versions(improved_versions)
                    print(formatted_versions)

                print(f"\n{'=' * 80}")
                return prompt

        print(f"Prompt with ID {prompt_id} not found")
        return {}

    def _format_text_for_display(self, text: str) -> str:
        """Format text for better console display."""
        if not text:
            return ""

        # Wrap long lines at 80 characters
        lines = []
        for line in text.split('\n'):
            # Preserve empty lines
            if not line.strip():
                lines.append("")
                continue

            # Wrap long lines
            while len(line) > 80:
                # Find a good breaking point
                break_point = line[:80].rfind(' ')
                if break_point == -1:  # No space found, force break at 80
                    break_point = 80

                lines.append(line[:break_point])
                line = line[break_point:].strip()

            if line:  # Add remaining text
                lines.append(line)

        return '\n'.join(lines)

    def _format_improved_versions(self, improved_versions: str) -> str:
        """Format improved versions for better console display."""
        if not improved_versions:
            return ""

        formatted = []
        sections = improved_versions.split('---')

        for i, section in enumerate(sections):
            if i == 0:  # Skip the first empty section
                continue

            # Extract model name and content
            if i < len(sections) - 1:
                model = section.strip()
                content = sections[i+1].split('---')[0] if i+1 < len(sections) else ""

                # Format the model header
                formatted.append(f"\n>> {model} <<")

                # Format the content with indentation
                if content:
                    content_lines = self._format_text_for_display(content.strip()).split('\n')
                    formatted.append('\n'.join(['   ' + line for line in content_lines]))

                # Skip the next section as we've already processed it
                i += 1

        return '\n'.join(formatted)

    def filter_prompts(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter prompts based on criteria."""
        prompts = self.get_all_prompts()
        filtered_prompts = []

        for prompt in prompts:
            match = True

            for key, value in filters.items():
                if key in prompt:
                    # For tags, check if any of the filter tags are in the prompt tags
                    if key == 'Tags' and value:
                        filter_tags = [tag.strip().lower() for tag in value.split(',')]
                        prompt_tags = [tag.strip().lower() for tag in prompt.get('Tags', '').split(',')]
                        if not any(tag in prompt_tags for tag in filter_tags):
                            match = False
                            break
                    # For other fields, check for exact match or substring
                    elif value and value.lower() not in prompt.get(key, '').lower():
                        match = False
                        break

            if match:
                filtered_prompts.append(prompt)

        return filtered_prompts

    def detect_new_prompts(self) -> List[Dict[str, Any]]:
        """
        Detect prompts that have text but are missing other information.
        Returns a list of prompts that need to be processed.
        """
        prompts = self.get_all_prompts()
        new_prompts = []

        for prompt in prompts:
            # Check if the prompt has text but is missing other key information
            has_text = prompt.get('Prompt Text', '').strip() != ''
            missing_category = prompt.get('Category', '').strip() == ''
            missing_subcategory = prompt.get('Subcategory', '').strip() == ''
            missing_tags = prompt.get('Tags', '').strip() == ''
            missing_analysis = prompt.get('Effectiveness Rating', '').strip() == ''

            if has_text and (missing_category or missing_subcategory or missing_tags or missing_analysis):
                new_prompts.append(prompt)

        return new_prompts

    def auto_process_prompt(self, prompt_id: str, openrouter_client: 'OpenRouterClient') -> bool:
        """
        Automatically process a prompt to fill in missing information.

        Args:
            prompt_id: The ID of the prompt to process
            openrouter_client: An instance of OpenRouterClient for AI-powered processing

        Returns:
            True if processing was successful, False otherwise
        """
        prompt = self.get_prompt(prompt_id, silent=True)
        if not prompt:
            print(f"Prompt with ID {prompt_id} not found")
            return False

        prompt_text = prompt.get('Prompt Text', '')
        if not prompt_text.strip():
            print(f"Prompt with ID {prompt_id} has no text to process")
            return False

        print(f"\n{'=' * 80}")
        print(f"AUTO-PROCESSING PROMPT: {prompt.get('Prompt Title', 'Untitled')} (ID: {prompt_id})")
        print(f"{'=' * 80}")

        updates = {}

        # Step 1: Categorize the prompt if category or subcategory is missing
        if not prompt.get('Category') or not prompt.get('Subcategory'):
            print("\nCategorizing prompt...")
            try:
                # Try using OpenRouter for categorization
                categorization = openrouter_client.categorize_prompt(prompt_text)
                if categorization.get('Category'):
                    updates.update(categorization)
                    print(f"✓ Categorized as: {categorization.get('Category')} / {categorization.get('Subcategory')}")
                    print(f"✓ Tags: {categorization.get('Tags')}")
                else:
                    # Fallback to local categorization
                    print("Using local categorization...")
                    category, subcategory, tags = self._local_categorize_prompt(prompt_text)
                    updates['Category'] = category
                    updates['Subcategory'] = subcategory
                    updates['Tags'] = tags
                    print(f"✓ Categorized as: {category} / {subcategory}")
                    print(f"✓ Tags: {tags}")
            except Exception as e:
                print(f"Error during categorization: {e}")
                # Fallback to local categorization
                category, subcategory, tags = self._local_categorize_prompt(prompt_text)
                updates['Category'] = category
                updates['Subcategory'] = subcategory
                updates['Tags'] = tags
                print(f"✓ Categorized as: {category} / {subcategory}")
                print(f"✓ Tags: {tags}")

        # Step 2: Analyze the prompt if effectiveness rating is missing
        if not prompt.get('Effectiveness Rating'):
            print("\nAnalyzing prompt effectiveness...")
            try:
                # Try using OpenRouter for analysis
                analysis = openrouter_client.analyze_prompt_effectiveness(prompt_text)
                if analysis.get('Effectiveness Rating'):
                    updates.update(analysis)
                    print(f"✓ Effectiveness Rating: {analysis.get('Effectiveness Rating')}/10")
                    print(f"✓ Added improvement suggestions")
                else:
                    # Fallback to local analysis
                    print("Using local analysis...")
                    rating, suggestions, notes = self._local_analyze_prompt(prompt_text)
                    updates['Effectiveness Rating'] = rating
                    updates['Improvement Suggestions'] = suggestions
                    updates['Notes'] = notes
                    print(f"✓ Effectiveness Rating: {rating}/10")
                    print(f"✓ Added improvement suggestions")
            except Exception as e:
                print(f"Error during analysis: {e}")
                # Fallback to local analysis
                rating, suggestions, notes = self._local_analyze_prompt(prompt_text)
                updates['Effectiveness Rating'] = rating
                updates['Improvement Suggestions'] = suggestions
                updates['Notes'] = notes
                print(f"✓ Effectiveness Rating: {rating}/10")
                print(f"✓ Added improvement suggestions")

        # Step 3: Generate improved version if none exists
        if not prompt.get('Improved Versions'):
            print("\nGenerating improved version...")
            try:
                # Try using OpenRouter for improvement
                target_model = prompt.get('Primary Tool') or "general"
                improved_prompt = openrouter_client.improve_prompt(prompt_text, target_model)
                if improved_prompt and improved_prompt != prompt_text:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    updates['Improved Versions'] = f"--- {target_model} (Auto-Improved on {timestamp}) ---\n{improved_prompt}"
                    print(f"✓ Generated improved version for {target_model}")
                else:
                    # Fallback to local improvement
                    print("Using local improvement...")
                    improved_prompt = self._local_improve_prompt(prompt_text, prompt)
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    updates['Improved Versions'] = f"--- Auto-Improved on {timestamp} ---\n{improved_prompt}"
                    print(f"✓ Generated improved version")
            except Exception as e:
                print(f"Error during improvement: {e}")
                # Fallback to local improvement
                improved_prompt = self._local_improve_prompt(prompt_text, prompt)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                updates['Improved Versions'] = f"--- Auto-Improved on {timestamp} ---\n{improved_prompt}"
                print(f"✓ Generated improved version")

        # Step 4: Set primary tool if missing
        if not prompt.get('Primary Tool'):
            # Determine the best tool based on the prompt content
            primary_tool = self._determine_primary_tool(prompt_text)
            updates['Primary Tool'] = primary_tool
            print(f"\n✓ Set Primary Tool to: {primary_tool}")

        # Step 5: Set title if missing
        if not prompt.get('Prompt Title') or prompt.get('Prompt Title') == 'Untitled':
            # Generate a title based on the prompt content
            title = self._generate_title(prompt_text)
            updates['Prompt Title'] = title
            print(f"\n✓ Set Title to: {title}")

        # Add a delay before updating to avoid quota limits
        time.sleep(2)

        # Update the prompt with all the new information
        if updates:
            success = self.update_prompt(prompt_id, updates)
            if success:
                print(f"\n{'=' * 80}")
                print(f"Successfully auto-processed prompt {prompt_id}")
                print(f"{'=' * 80}")
                return True
            else:
                print(f"\n{'=' * 80}")
                print(f"Failed to update prompt {prompt_id}")
                print(f"{'=' * 80}")
                return False
        else:
            print(f"\n{'=' * 80}")
            print(f"No updates needed for prompt {prompt_id}")
            print(f"{'=' * 80}")
            return True

    def _local_categorize_prompt(self, prompt_text: str) -> tuple:
        """
        Perform local categorization of a prompt without using external API.

        Returns:
            Tuple of (category, subcategory, tags)
        """
        # Default values
        category = "Other"
        subcategory = ""
        tags = []

        # Simple keyword-based categorization
        prompt_lower = prompt_text.lower()

        # Check for writing-related content
        if any(kw in prompt_lower for kw in ['write', 'essay', 'blog', 'article', 'content', 'story', 'book']):
            category = "Writing"
            if 'blog' in prompt_lower:
                subcategory = "Blog"
                tags.append("blog")
            elif 'story' in prompt_lower or 'fiction' in prompt_lower:
                subcategory = "Creative Writing"
                tags.append("creative")
                tags.append("story")
            elif 'essay' in prompt_lower or 'academic' in prompt_lower:
                subcategory = "Academic"
                tags.append("academic")
            elif 'article' in prompt_lower:
                subcategory = "Articles"
                tags.append("article")
            elif 'book' in prompt_lower:
                subcategory = "Book Writing"
                tags.append("book")
            else:
                subcategory = "General Writing"

            tags.append("writing")

        # Check for coding-related content
        elif any(kw in prompt_lower for kw in ['code', 'program', 'function', 'algorithm', 'python', 'javascript', 'java', 'c++', 'html', 'css']):
            category = "Coding"
            if 'python' in prompt_lower:
                subcategory = "Python"
                tags.append("python")
            elif 'javascript' in prompt_lower or 'js' in prompt_lower:
                subcategory = "JavaScript"
                tags.append("javascript")
            elif 'java' in prompt_lower:
                subcategory = "Java"
                tags.append("java")
            elif 'c++' in prompt_lower or 'c#' in prompt_lower:
                subcategory = "C/C++/C#"
                tags.append("c++")
            elif 'html' in prompt_lower or 'css' in prompt_lower or 'web' in prompt_lower:
                subcategory = "Web Development"
                tags.append("web-dev")
            else:
                subcategory = "General Programming"

            tags.append("coding")
            tags.append("programming")

        # Check for business-related content
        elif any(kw in prompt_lower for kw in ['business', 'marketing', 'sales', 'strategy', 'startup', 'product', 'customer']):
            category = "Business"
            if 'marketing' in prompt_lower:
                subcategory = "Marketing"
                tags.append("marketing")
            elif 'sales' in prompt_lower:
                subcategory = "Sales"
                tags.append("sales")
            elif 'strategy' in prompt_lower:
                subcategory = "Strategy"
                tags.append("strategy")
            elif 'startup' in prompt_lower:
                subcategory = "Startup"
                tags.append("startup")
            elif 'product' in prompt_lower:
                subcategory = "Product Management"
                tags.append("product")
            else:
                subcategory = "General Business"

            tags.append("business")

        # Check for research-related content
        elif any(kw in prompt_lower for kw in ['research', 'study', 'analysis', 'data', 'investigate', 'examine']):
            category = "Research"
            if 'data' in prompt_lower:
                subcategory = "Data Analysis"
                tags.append("data")
            elif 'market' in prompt_lower:
                subcategory = "Market Research"
                tags.append("market-research")
            elif 'academic' in prompt_lower or 'scientific' in prompt_lower:
                subcategory = "Academic Research"
                tags.append("academic")
            else:
                subcategory = "General Research"

            tags.append("research")

        # Check for creative content
        elif any(kw in prompt_lower for kw in ['creative', 'imagine', 'design', 'art', 'music', 'poem', 'song']):
            category = "Creative"
            if 'design' in prompt_lower:
                subcategory = "Design"
                tags.append("design")
            elif 'art' in prompt_lower:
                subcategory = "Art"
                tags.append("art")
            elif 'music' in prompt_lower or 'song' in prompt_lower:
                subcategory = "Music"
                tags.append("music")
            elif 'poem' in prompt_lower or 'poetry' in prompt_lower:
                subcategory = "Poetry"
                tags.append("poetry")
            else:
                subcategory = "General Creative"

            tags.append("creative")

        # Check for educational content
        elif any(kw in prompt_lower for kw in ['teach', 'learn', 'education', 'student', 'course', 'lesson', 'explain']):
            category = "Education"
            if 'course' in prompt_lower:
                subcategory = "Course Creation"
                tags.append("course")
            elif 'lesson' in prompt_lower:
                subcategory = "Lesson Planning"
                tags.append("lesson")
            elif 'explain' in prompt_lower:
                subcategory = "Explanations"
                tags.append("explanation")
            else:
                subcategory = "General Education"

            tags.append("education")
            tags.append("learning")

        # Check for personal content
        elif any(kw in prompt_lower for kw in ['personal', 'self', 'improve', 'goal', 'plan', 'life', 'career']):
            category = "Personal"
            if 'career' in prompt_lower:
                subcategory = "Career Development"
                tags.append("career")
            elif 'goal' in prompt_lower:
                subcategory = "Goal Setting"
                tags.append("goals")
            elif 'plan' in prompt_lower:
                subcategory = "Planning"
                tags.append("planning")
            elif 'improve' in prompt_lower:
                subcategory = "Self Improvement"
                tags.append("self-improvement")
            else:
                subcategory = "General Personal"

            tags.append("personal")

        # Check for technical content
        elif any(kw in prompt_lower for kw in ['technical', 'technology', 'system', 'software', 'hardware', 'engineering']):
            category = "Technical"
            if 'software' in prompt_lower:
                subcategory = "Software"
                tags.append("software")
            elif 'hardware' in prompt_lower:
                subcategory = "Hardware"
                tags.append("hardware")
            elif 'system' in prompt_lower:
                subcategory = "Systems"
                tags.append("systems")
            elif 'engineering' in prompt_lower:
                subcategory = "Engineering"
                tags.append("engineering")
            else:
                subcategory = "General Technical"

            tags.append("technical")
            tags.append("technology")

        # Add additional tags based on specific keywords
        if 'linkedin' in prompt_lower:
            tags.append("linkedin")
        if 'social media' in prompt_lower:
            tags.append("social-media")
        if 'email' in prompt_lower:
            tags.append("email")
        if 'ai' in prompt_lower or 'artificial intelligence' in prompt_lower:
            tags.append("ai")
        if 'data' in prompt_lower:
            tags.append("data")
        if 'analysis' in prompt_lower:
            tags.append("analysis")

        return category, subcategory, ",".join(tags)

    def _local_analyze_prompt(self, prompt_text: str) -> tuple:
        """
        Perform local analysis of a prompt without using external API.

        Returns:
            Tuple of (rating, suggestions, notes)
        """
        # Calculate basic metrics
        word_count = len(prompt_text.split())
        char_count = len(prompt_text)
        sentence_count = len([s for s in prompt_text.split('.') if s.strip()])

        # Calculate rating based on multiple factors
        length_score = min(5, max(1, word_count // 20))
        structure_score = 1
        if ":" in prompt_text:
            structure_score += 1
        if prompt_text.count("\n") > 2:
            structure_score += 1
        if any(marker in prompt_text for marker in ["1.", "2.", "•", "-", "*"]):
            structure_score += 1
        if "?" in prompt_text:
            structure_score += 1

        clarity_score = min(5, structure_score)
        rating = min(10, max(1, (length_score + clarity_score) // 1))

        # Generate suggestions
        suggestions = []

        # Basic suggestions
        if "[insert" in prompt_text or "[INSERT" in prompt_text:
            suggestions.append("Replace placeholder text with specific examples")
        if word_count < 50:
            suggestions.append("Add more detail to make the prompt more specific")
        if word_count > 300:
            suggestions.append("Consider breaking this into multiple smaller prompts")
        if "?" not in prompt_text:
            suggestions.append("Consider adding specific questions to guide the response")
        if prompt_text.count("\n") < 2:
            suggestions.append("Add more structure with line breaks and sections")
        if not any(marker in prompt_text for marker in ["1.", "2.", "•", "-", "*"]):
            suggestions.append("Use numbered lists or bullet points to organize instructions")

        # Notes about the analysis
        notes = f"Word count: {word_count}. Character count: {char_count}. Sentence count: {sentence_count}. This is a local analysis."

        return str(rating), "\n".join(suggestions), notes

    def _local_improve_prompt(self, prompt_text: str, prompt: Dict[str, Any]) -> str:
        """
        Perform local improvement of a prompt without using external API.

        Returns:
            Improved prompt text
        """
        improved_prompt = prompt_text
        category = prompt.get('Category', '').lower()
        subcategory = prompt.get('Subcategory', '').lower()

        # Replace placeholder text
        if "[insert" in improved_prompt:
            if "marketing" in category or "linkedin" in subcategory:
                improved_prompt = improved_prompt.replace("[insert Your Category]", "Digital Marketing Consultant")
            elif "writing" in category:
                improved_prompt = improved_prompt.replace("[insert Your Category]", "Content Writer")
            elif "coding" in category or "tech" in category:
                improved_prompt = improved_prompt.replace("[insert Your Category]", "Software Developer")
            else:
                improved_prompt = improved_prompt.replace("[insert Your Category]", "Professional")

        # Add specific audience if relevant
        if "linkedin" in improved_prompt.lower() and "target audience" not in improved_prompt.lower():
            improved_prompt += "\n\nMy target audience is business professionals aged 30-50 who are looking to improve their digital presence."

        # Add request for metrics if relevant
        if ("marketing" in category or "business" in category) and "metrics" not in improved_prompt.lower() and "kpi" not in improved_prompt.lower():
            improved_prompt += "\n\nPlease also suggest 3-5 key metrics I should track to measure the success of this strategy."

        # Add examples request if relevant
        if "example" not in improved_prompt.lower():
            improved_prompt += "\n\nPlease provide specific examples to illustrate your recommendations."

        # Add structure if needed
        if improved_prompt.count("\n") < 2:
            # Add basic structure with sections
            structured_prompt = "I need the following:\n\n"
            structured_prompt += improved_prompt
            improved_prompt = structured_prompt

        return improved_prompt

    def _determine_primary_tool(self, prompt_text: str) -> str:
        """
        Determine the best AI tool for a prompt based on its content.

        Returns:
            Name of the recommended primary tool
        """
        prompt_lower = prompt_text.lower()

        # Check for specific tool mentions
        if "gpt" in prompt_lower:
            return "GPT-4"
        elif "claude" in prompt_lower:
            return "Claude"
        elif "gemini" in prompt_lower:
            return "Gemini"
        elif "mistral" in prompt_lower:
            return "Mistral"

        # Determine based on content and complexity
        word_count = len(prompt_text.split())
        has_code = any(kw in prompt_lower for kw in ['code', 'function', 'programming', 'algorithm', 'python', 'javascript'])
        has_creative = any(kw in prompt_lower for kw in ['creative', 'imagine', 'story', 'art', 'design'])
        has_reasoning = any(kw in prompt_lower for kw in ['analyze', 'explain', 'reason', 'logic', 'why', 'how'])
        has_structured_output = any(kw in prompt_lower for kw in ['json', 'table', 'format', 'structure'])

        # Make recommendation based on content
        if has_code:
            return "Claude"
        elif has_creative:
            return "Claude"
        elif has_reasoning and word_count > 100:
            return "Claude"
        elif has_structured_output:
            return "GPT-4"
        elif word_count > 200:
            return "Claude"
        else:
            return "GPT-4"

    def _generate_title(self, prompt_text: str) -> str:
        """
        Generate a title for a prompt based on its content.

        Returns:
            Generated title
        """
        # Extract the first sentence or first 10 words
        first_sentence = prompt_text.split('.')[0].strip()
        words = first_sentence.split()

        if len(words) <= 10:
            title = first_sentence
        else:
            title = ' '.join(words[:10]) + "..."

        # Clean up the title
        title = title.replace("\n", " ").strip()

        # Make sure it's not too long
        if len(title) > 50:
            title = title[:47] + "..."

        # Make sure it's not empty
        if not title:
            title = "Untitled Prompt"

        return title

    def get_prompt(self, prompt_id: str, silent: bool = False) -> Dict[str, Any]:
        """Get a specific prompt by ID."""
        prompts = self.get_all_prompts()

        for prompt in prompts:
            if prompt.get('Prompt ID') == prompt_id:
                # Print the prompt details in a nicely formatted way
                if not silent:
                    print(f"\n{'=' * 80}")
                    print(f"PROMPT: {prompt.get('Prompt Title', 'Untitled')} (ID: {prompt_id})")
                    print(f"{'=' * 80}")

                    # Print metadata in a clean format
                    print(f"\n{'-' * 30} METADATA {'-' * 30}")
                    metadata_fields = ['Category', 'Subcategory', 'Primary Tool', 'Compatible Tools',
                                      'Effectiveness Rating', 'Tags', 'Creation Date', 'Last Modified']
                    for field in metadata_fields:
                        if prompt.get(field):
                            print(f"{field:20}: {prompt.get(field)}")

                    # Print the prompt text with proper formatting
                    print(f"\n{'-' * 30} PROMPT TEXT {'-' * 30}")
                    prompt_text = prompt.get('Prompt Text', '')
                    # Format the prompt text for better readability
                    formatted_text = self._format_text_for_display(prompt_text)
                    print(formatted_text)

                    # Print analysis if available
                    if prompt.get('Notes') or prompt.get('Improvement Suggestions'):
                        print(f"\n{'-' * 30} ANALYSIS {'-' * 30}")
                        if prompt.get('Notes'):
                            print(f"Notes: {prompt.get('Notes')}")
                        if prompt.get('Improvement Suggestions'):
                            print("\nImprovement Suggestions:")
                            suggestions = prompt.get('Improvement Suggestions', '').split('\n')
                            for suggestion in suggestions:
                                if suggestion.strip():
                                    print(f"• {suggestion.strip()}")

                    # Print improved versions if available
                    if prompt.get('Improved Versions'):
                        print(f"\n{'-' * 30} IMPROVED VERSIONS {'-' * 30}")
                        improved_versions = prompt.get('Improved Versions', '')
                        # Format the improved versions for better readability
                        formatted_versions = self._format_improved_versions(improved_versions)
                        print(formatted_versions)

                    print(f"\n{'=' * 80}")
                return prompt

        if not silent:
            print(f"Prompt with ID {prompt_id} not found")
        return {}

def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description='Prompt Management System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  List all prompts:
    python prompt_manager.py list

  Get a specific prompt:
    python prompt_manager.py get --id P001

  Add a new prompt:
    python prompt_manager.py add --title "My Prompt" --text "This is my prompt text" --category "Writing" --tags "creative,story"

  Update a prompt:
    python prompt_manager.py update --id P001 --title "Updated Title" --category "Marketing"

  Analyze a prompt:
    python prompt_manager.py analyze --id P001

  Improve a prompt:
    python prompt_manager.py improve --id P001 --model "claude-3"

  Generate variations:
    python prompt_manager.py variations --id P001 --models "gpt-4,claude-3,gemini-pro"

  Filter prompts:
    python prompt_manager.py filter --category "Writing" --tags "creative"

  Process new prompts:
    python prompt_manager.py process-new

  Auto-fill a specific prompt:
    python prompt_manager.py auto-fill --id P001
"""
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List all prompts
    list_parser = subparsers.add_parser('list',
        help='List all prompts',
        description='Display a table of all prompts in the database with their key metadata.')

    # Get a specific prompt
    get_parser = subparsers.add_parser('get',
        help='Get a specific prompt',
        description='Display detailed information about a specific prompt, including its text, metadata, analysis, and improved versions.')
    get_parser.add_argument('--id', required=True, help='Prompt ID (e.g., P001)')

    # Add a new prompt
    add_parser = subparsers.add_parser('add',
        help='Add a new prompt',
        description='Add a new prompt to the database with metadata.')
    add_parser.add_argument('--title', required=True, help='Descriptive title for the prompt')
    add_parser.add_argument('--text', required=True, help='The full text of the prompt')
    add_parser.add_argument('--category', help='Main category (e.g., Writing, Coding, Research)')
    add_parser.add_argument('--subcategory', help='More specific classification within the category')
    add_parser.add_argument('--tool', help='Primary AI model/tool the prompt is designed for')
    add_parser.add_argument('--compatible', help='Other tools the prompt works with (comma-separated)')
    add_parser.add_argument('--tags', help='Keywords for filtering and organization (comma-separated)')
    add_parser.add_argument('--notes', help='Additional information about the prompt')
    add_parser.add_argument('--auto-categorize', action='store_true', help='Automatically categorize the prompt using AI')

    # Update an existing prompt
    update_parser = subparsers.add_parser('update',
        help='Update an existing prompt',
        description='Update the metadata or content of an existing prompt.')
    update_parser.add_argument('--id', required=True, help='Prompt ID to update (e.g., P001)')
    update_parser.add_argument('--title', help='New title for the prompt')
    update_parser.add_argument('--text', help='New text for the prompt')
    update_parser.add_argument('--category', help='New category')
    update_parser.add_argument('--subcategory', help='New subcategory')
    update_parser.add_argument('--tool', help='New primary tool')
    update_parser.add_argument('--compatible', help='New compatible tools (comma-separated)')
    update_parser.add_argument('--tags', help='New tags (comma-separated)')
    update_parser.add_argument('--notes', help='New additional notes')

    # Filter prompts
    filter_parser = subparsers.add_parser('filter',
        help='Filter prompts',
        description='Display prompts that match specific criteria.')
    filter_parser.add_argument('--category', help='Filter by category (e.g., Writing, Coding)')
    filter_parser.add_argument('--subcategory', help='Filter by subcategory')
    filter_parser.add_argument('--tool', help='Filter by primary tool (e.g., GPT-4, Claude)')
    filter_parser.add_argument('--tags', help='Filter by tags (comma-separated)')

    # Analyze a prompt
    analyze_parser = subparsers.add_parser('analyze',
        help='Analyze a prompt for effectiveness',
        description='Evaluate a prompt and provide suggestions for improvement.')
    analyze_parser.add_argument('--id', required=True, help='Prompt ID to analyze (e.g., P001)')

    # Improve a prompt
    improve_parser = subparsers.add_parser('improve',
        help='Improve a prompt',
        description='Generate an improved version of a prompt based on analysis and best practices.')
    improve_parser.add_argument('--id', required=True, help='Prompt ID to improve (e.g., P001)')
    improve_parser.add_argument('--model', help='Target model to optimize for (e.g., gpt-4, claude-3, gemini-pro)')

    # Generate variations for multiple models
    variations_parser = subparsers.add_parser('variations',
        help='Generate variations for multiple models',
        description='Create multiple versions of a prompt optimized for different AI models.')
    variations_parser.add_argument('--id', required=True, help='Prompt ID to generate variations for (e.g., P001)')
    variations_parser.add_argument('--models', required=True, help='Comma-separated list of models (e.g., "gpt-4,claude-3,gemini-pro")')

    # Process new prompts
    process_new_parser = subparsers.add_parser('process-new',
        help='Process all new prompts',
        description='Automatically detect and process all prompts that have text but are missing other information.')
    process_new_parser.add_argument('--auto-approve', action='store_true', help='Process all new prompts without confirmation')

    # Auto-fill a specific prompt
    auto_fill_parser = subparsers.add_parser('auto-fill',
        help='Auto-fill a specific prompt',
        description='Automatically fill in missing information for a specific prompt.')
    auto_fill_parser.add_argument('--id', required=True, help='Prompt ID to auto-fill (e.g., P001)')

    args = parser.parse_args()

    # Check for OpenRouter API key and model
    openrouter_api_key = os.environ.get('OPENROUTER_API_KEY')
    openrouter_model = os.environ.get('OPENROUTER_MODEL', DEFAULT_OPENROUTER_MODEL)

    # Initialize the database client
    db = PromptDB()

    # Check for new prompts on startup (only if no command is specified)
    if not args.command:
        new_prompts = db.detect_new_prompts()
        if new_prompts:
            print(f"\nFound {len(new_prompts)} new prompts that need processing.")
            print("Run 'python prompt_manager.py process-new' to process them.")
            print("Or 'python prompt_manager.py list' to see all prompts.")
            sys.exit(0)
        else:
            print("\nNo new prompts found that need processing.")
            print("Use 'python prompt_manager.py list' to see all prompts.")
            sys.exit(0)

    # Initialize the OpenRouter client
    if openrouter_api_key:
        print(f"API Key: {openrouter_api_key[:5]}...{openrouter_api_key[-5:] if openrouter_api_key else ''}")
        print(f"Using OpenRouter model: {openrouter_model}")
        openrouter = OpenRouterClient(openrouter_api_key, openrouter_model)
    else:
        print("Warning: OPENROUTER_API_KEY environment variable not set")
        print("Using local fallback methods for all operations")
        # Create a dummy OpenRouter client that will trigger fallbacks
        openrouter = OpenRouterClient("dummy_key", DEFAULT_OPENROUTER_MODEL)

    if args.command == 'list':
        prompts = db.get_all_prompts()
        if prompts:
            print("\n" + "=" * 110)
            print(f"{'ID':<6} {'TITLE':<40} {'CATEGORY':<15} {'TOOL':<15} {'RATING':<8} {'TAGS':<20} {'STATUS'}")
            print("=" * 110)

            needs_processing_count = 0

            for prompt in prompts:
                prompt_id = prompt.get('Prompt ID', 'Unknown')
                prompt_title = prompt.get('Prompt Title', 'Untitled')
                category = prompt.get('Category', '')
                tool = prompt.get('Primary Tool', '')
                rating = prompt.get('Effectiveness Rating', '')
                tags = prompt.get('Tags', '')

                # Check if prompt needs processing
                needs_processing = False
                has_text = prompt.get('Prompt Text', '').strip() != ''
                missing_category = prompt.get('Category', '').strip() == ''
                missing_subcategory = prompt.get('Subcategory', '').strip() == ''
                missing_tags = prompt.get('Tags', '').strip() == ''
                missing_analysis = prompt.get('Effectiveness Rating', '').strip() == ''

                if has_text and (missing_category or missing_subcategory or missing_tags or missing_analysis):
                    needs_processing = True
                    needs_processing_count += 1

                # Truncate long fields for display
                if len(prompt_title) > 37:
                    prompt_title = prompt_title[:34] + "..."
                if len(category) > 12:
                    category = category[:9] + "..."
                if len(tool) > 12:
                    tool = tool[:9] + "..."
                if len(tags) > 17:
                    tags = tags[:14] + "..."

                # Format the output in a table-like format
                status = "NEEDS PROCESSING" if needs_processing else "Complete"
                print(f"{prompt_id:<6} {prompt_title:<40} {category:<15} {tool:<15} {rating:<8} {tags:<20} {status}")

            print("=" * 110)
            print(f"Total: {len(prompts)} prompts ({needs_processing_count} need processing)")

            # Show instructions if there are prompts that need processing
            if needs_processing_count > 0:
                print("\nTo process all incomplete prompts:")
                print("  python prompt_manager.py process-new")
                print("\nTo process a specific prompt:")
                print("  python prompt_manager.py auto-fill --id <prompt_id>")
        else:
            print("\nNo prompts found in the database.")

    elif args.command == 'get':
        prompt = db.get_prompt(args.id)
        if not prompt:
            sys.exit(1)

    elif args.command == 'add':
        prompt_data = {
            'Prompt Title': args.title,
            'Prompt Text': args.text,
            'Category': args.category or '',
            'Subcategory': args.subcategory or '',
            'Primary Tool': args.tool or '',
            'Compatible Tools': args.compatible or '',
            'Tags': args.tags or '',
            'Notes': args.notes or ''
        }

        # Auto-categorize if requested
        if args.auto_categorize:
            print("Auto-categorizing prompt...")
            categorization = openrouter.categorize_prompt(args.text)
            prompt_data.update(categorization)

        db.add_prompt(prompt_data)

    elif args.command == 'update':
        prompt_data = {}
        if args.title:
            prompt_data['Prompt Title'] = args.title
        if args.text:
            prompt_data['Prompt Text'] = args.text
        if args.category:
            prompt_data['Category'] = args.category
        if args.subcategory:
            prompt_data['Subcategory'] = args.subcategory
        if args.tool:
            prompt_data['Primary Tool'] = args.tool
        if args.compatible:
            prompt_data['Compatible Tools'] = args.compatible
        if args.tags:
            prompt_data['Tags'] = args.tags
        if args.notes:
            prompt_data['Notes'] = args.notes

        db.update_prompt(args.id, prompt_data)

    elif args.command == 'filter':
        filters = {}
        if args.category:
            filters['Category'] = args.category
        if args.subcategory:
            filters['Subcategory'] = args.subcategory
        if args.tool:
            filters['Primary Tool'] = args.tool
        if args.tags:
            filters['Tags'] = args.tags

        prompts = db.filter_prompts(filters)
        if prompts:
            for prompt in prompts:
                print(f"{prompt.get('Prompt ID')}: {prompt.get('Prompt Title')}")
        else:
            print("No prompts found matching the filters")

    elif args.command == 'analyze':
        prompt = db.get_prompt(args.id)
        if not prompt:
            sys.exit(1)

        prompt_text = prompt.get('Prompt Text', '')
        prompt_title = prompt.get('Prompt Title', 'Untitled')
        category = prompt.get('Category', '')
        subcategory = prompt.get('Subcategory', '')

        print(f"\n{'=' * 80}")
        print(f"ANALYZING PROMPT: {prompt_title} (ID: {args.id})")
        print(f"{'=' * 80}")

        # Skip OpenRouter and use local analysis directly
        print("\nPerforming local analysis...")

        # Perform a simple local analysis
        word_count = len(prompt_text.split())
        char_count = len(prompt_text)
        sentence_count = len([s for s in prompt_text.split('.') if s.strip()])

        # Calculate metrics
        avg_word_length = char_count / max(1, word_count)
        avg_sentence_length = word_count / max(1, sentence_count)

        # Calculate rating based on multiple factors
        length_score = min(5, max(1, word_count // 20))
        structure_score = 1
        if ":" in prompt_text:
            structure_score += 1
        if prompt_text.count("\n") > 2:
            structure_score += 1
        if any(marker in prompt_text for marker in ["1.", "2.", "•", "-", "*"]):
            structure_score += 1
        if "?" in prompt_text:
            structure_score += 1

        clarity_score = min(5, structure_score)
        rating = min(10, max(1, (length_score + clarity_score) // 1))

        # Print analysis metrics
        print(f"\n{'-' * 30} METRICS {'-' * 30}")
        print(f"Word count:             {word_count}")
        print(f"Character count:        {char_count}")
        print(f"Sentence count:         {sentence_count}")
        print(f"Avg word length:        {avg_word_length:.1f} characters")
        print(f"Avg sentence length:    {avg_sentence_length:.1f} words")
        print(f"Overall rating:         {rating}/10")

        # Simple suggestions based on prompt content
        suggestions = []

        # Basic suggestions
        if "[insert" in prompt_text or "[INSERT" in prompt_text:
            suggestions.append("Replace placeholder text with specific examples")
        if word_count < 50:
            suggestions.append("Add more detail to make the prompt more specific")
        if word_count > 300:
            suggestions.append("Consider breaking this into multiple smaller prompts")
        if "?" not in prompt_text:
            suggestions.append("Consider adding specific questions to guide the response")
        if prompt_text.count("\n") < 2:
            suggestions.append("Add more structure with line breaks and sections")
        if not any(marker in prompt_text for marker in ["1.", "2.", "•", "-", "*"]):
            suggestions.append("Use numbered lists or bullet points to organize instructions")

        # Category-specific suggestions
        if "linkedin" in prompt_text.lower() or "linkedin" in prompt_title.lower() or "linkedin" in subcategory.lower():
            suggestions.append("Specify the target audience more clearly")
            suggestions.append("Include examples of successful LinkedIn content in your niche")
            suggestions.append("Ask for metrics or KPIs to measure content success")

        if "writing" in category.lower() or "content" in category.lower():
            suggestions.append("Specify the desired tone and style (formal, conversational, etc.)")
            suggestions.append("Include word count or length guidelines")
            suggestions.append("Clarify the target audience for the content")

        if "coding" in category.lower() or "technical" in category.lower():
            suggestions.append("Specify the programming language or technology stack")
            suggestions.append("Include requirements for code comments and documentation")
            suggestions.append("Ask for explanations of the code's functionality")

        # Print improvement suggestions
        print(f"\n{'-' * 30} IMPROVEMENT SUGGESTIONS {'-' * 30}")
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i:2}. {suggestion}")
        else:
            print("No specific improvement suggestions.")

        # Create a simple analysis result
        local_analysis = {
            "Effectiveness Rating": str(rating),
            "Improvement Suggestions": "\n".join(suggestions) if suggestions else "No specific suggestions",
            "Notes": f"Word count: {word_count}. Character count: {char_count}. Sentence count: {sentence_count}. This is a local analysis."
        }

        # Update the prompt with the local analysis
        db.update_prompt(args.id, local_analysis)

        print(f"\n{'-' * 30} NEXT STEPS {'-' * 30}")
        print("1. Review the analysis and suggestions above")
        print("2. Improve the prompt using: python prompt_manager.py improve --id " + args.id)
        print("3. Generate variations for different models using: python prompt_manager.py variations --id " + args.id + " --models \"gpt-4,claude-3,gemini-pro\"")

        print(f"\n{'=' * 80}")
        print("Analysis complete and saved to the database.")
        print(f"{'=' * 80}")

    elif args.command == 'improve':
        prompt = db.get_prompt(args.id)
        if not prompt:
            sys.exit(1)

        target_model = args.model or prompt.get('Primary Tool') or "general"
        prompt_text = prompt.get('Prompt Text', '')
        prompt_title = prompt.get('Prompt Title', 'Untitled')
        category = prompt.get('Category', '')
        subcategory = prompt.get('Subcategory', '')

        print(f"\n{'=' * 80}")
        print(f"IMPROVING PROMPT: {prompt_title} (ID: {args.id})")
        print(f"Target Model: {target_model}")
        print(f"{'=' * 80}")

        # Skip OpenRouter and use local improvement
        print("\nApplying intelligent improvements...")

        # Get improvement suggestions
        suggestions = []
        if prompt.get('Improvement Suggestions'):
            suggestions = prompt.get('Improvement Suggestions').split('\n')

        # Track changes for reporting
        changes_made = []

        # Apply improvements based on suggestions
        improved_prompt = prompt_text

        # Replace placeholder text
        if "[insert" in prompt_text:
            if "marketing" in category.lower() or "linkedin" in subcategory.lower():
                replacement = "Digital Marketing Consultant"
                improved_prompt = improved_prompt.replace("[insert Your Category]", replacement)
                changes_made.append(f"Replaced placeholder '[insert Your Category]' with '{replacement}'")
            elif "writing" in category.lower():
                replacement = "Content Writer"
                improved_prompt = improved_prompt.replace("[insert Your Category]", replacement)
                changes_made.append(f"Replaced placeholder '[insert Your Category]' with '{replacement}'")
            elif "coding" in category.lower() or "tech" in category.lower():
                replacement = "Software Developer"
                improved_prompt = improved_prompt.replace("[insert Your Category]", replacement)
                changes_made.append(f"Replaced placeholder '[insert Your Category]' with '{replacement}'")
            else:
                replacement = "Professional"
                improved_prompt = improved_prompt.replace("[insert Your Category]", replacement)
                changes_made.append(f"Replaced placeholder '[insert Your Category]' with '{replacement}'")

        # Add specific audience
        if "linkedin" in prompt_text.lower() and "target audience" not in prompt_text.lower():
            audience_text = "\n\nMy target audience is business professionals aged 30-50 who are looking to improve their digital presence."
            improved_prompt += audience_text
            changes_made.append("Added target audience specification")

        # Add request for metrics
        if "metrics" not in prompt_text.lower() and "kpi" not in prompt_text.lower():
            metrics_text = "\n\nPlease also suggest 3-5 key metrics I should track to measure the success of this content strategy."
            improved_prompt += metrics_text
            changes_made.append("Added request for success metrics/KPIs")

        # Add examples request
        if "example" not in prompt_text.lower():
            examples_text = "\n\nFor each content pillar, please provide one detailed example post that demonstrates the format and approach."
            improved_prompt += examples_text
            changes_made.append("Added request for example content")

        # Add structure if needed
        if prompt_text.count("\n") < 2 and improved_prompt.count("\n") < 2:
            # Add basic structure with sections
            structured_prompt = "I need the following:\n\n"
            structured_prompt += improved_prompt
            improved_prompt = structured_prompt
            changes_made.append("Added structural formatting with sections")

        # Add model-specific optimizations
        if target_model.lower() in ["gpt-4", "gpt-3.5", "gpt"]:
            gpt_text = "\n\nPlease format your response using markdown with clear headings, bullet points, and numbered lists for better readability."
            improved_prompt += gpt_text
            changes_made.append(f"Added {target_model}-specific formatting instructions")
        elif target_model.lower() in ["claude", "claude-3", "anthropic"]:
            claude_text = "\n\nPlease organize your response with clear headings and structured sections. Feel free to use tables if appropriate."
            improved_prompt += claude_text
            changes_made.append(f"Added {target_model}-specific formatting instructions")

        # Print the changes made
        print(f"\n{'-' * 30} IMPROVEMENTS APPLIED {'-' * 30}")
        if changes_made:
            for i, change in enumerate(changes_made, 1):
                print(f"{i:2}. {change}")
        else:
            print("No improvements were needed or applied.")

        # Print before and after comparison
        print(f"\n{'-' * 30} BEFORE {'-' * 30}")
        formatted_original = db._format_text_for_display(prompt_text)
        print(formatted_original)

        print(f"\n{'-' * 30} AFTER {'-' * 30}")
        formatted_improved = db._format_text_for_display(improved_prompt)
        print(formatted_improved)

        # Update the prompt with the improved version
        improved_versions = prompt.get('Improved Versions', '')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if improved_versions:
            improved_versions += f"\n\n--- {target_model} (Improved on {timestamp}) ---\n{improved_prompt}"
        else:
            improved_versions = f"--- {target_model} (Improved on {timestamp}) ---\n{improved_prompt}"

        db.update_prompt(args.id, {'Improved Versions': improved_versions})

        print(f"\n{'-' * 30} NEXT STEPS {'-' * 30}")
        print("1. Review the improved prompt above")
        print("2. Generate variations for different models using: python prompt_manager.py variations --id " + args.id + " --models \"gpt-4,claude-3,gemini-pro\"")
        print("3. Test the improved prompt with your target model")

        print(f"\n{'=' * 80}")
        print("Improvement complete and saved to the database.")
        print(f"{'=' * 80}")

    elif args.command == 'variations':
        prompt = db.get_prompt(args.id)
        if not prompt:
            sys.exit(1)

        models = [model.strip() for model in args.models.split(',')]
        prompt_text = prompt.get('Prompt Text', '')
        prompt_title = prompt.get('Prompt Title', 'Untitled')
        category = prompt.get('Category', '')
        subcategory = prompt.get('Subcategory', '')

        print(f"\n{'=' * 80}")
        print(f"GENERATING VARIATIONS: {prompt_title} (ID: {args.id})")
        print(f"Target Models: {', '.join(models)}")
        print(f"{'=' * 80}")

        print("\nFinding best base prompt to use...")

        # Get the base improved prompt if it exists
        improved_versions = prompt.get('Improved Versions', '')
        base_improved_prompt = None
        base_source = "original"

        # Try to find an existing improved version to use as base
        if improved_versions:
            # Extract the content after the first model marker
            try:
                parts = improved_versions.split('---')
                if len(parts) >= 3:  # At least one model section
                    model_name = parts[1].strip()
                    content_start = improved_versions.find('---', improved_versions.find('---') + 3) + 3
                    content_end = improved_versions.find('---', content_start) if '---' in improved_versions[content_start:] else len(improved_versions)
                    base_improved_prompt = improved_versions[content_start:content_end].strip()
                    base_source = model_name
                    print(f"✓ Using existing improved prompt for {model_name} as base")
            except Exception as e:
                print(f"✗ Error extracting base prompt: {e}")
                base_improved_prompt = None

        # If no improved version exists, create one
        if not base_improved_prompt:
            base_improved_prompt = prompt_text
            print("✓ Using original prompt as base (no improved version found)")

            # Apply basic improvements to the base prompt
            changes_made = []

            # Replace placeholder text
            if "[insert" in base_improved_prompt:
                if "marketing" in category.lower() or "linkedin" in subcategory.lower():
                    base_improved_prompt = base_improved_prompt.replace("[insert Your Category]", "Digital Marketing Consultant")
                    changes_made.append("Replaced placeholder text")
                elif "writing" in category.lower():
                    base_improved_prompt = base_improved_prompt.replace("[insert Your Category]", "Content Writer")
                    changes_made.append("Replaced placeholder text")
                elif "coding" in category.lower() or "tech" in category.lower():
                    base_improved_prompt = base_improved_prompt.replace("[insert Your Category]", "Software Developer")
                    changes_made.append("Replaced placeholder text")
                else:
                    base_improved_prompt = base_improved_prompt.replace("[insert Your Category]", "Professional")
                    changes_made.append("Replaced placeholder text")

            # Add specific audience
            if "linkedin" in base_improved_prompt.lower() and "target audience" not in base_improved_prompt.lower():
                base_improved_prompt += "\n\nMy target audience is business professionals aged 30-50 who are looking to improve their digital presence."
                changes_made.append("Added target audience specification")

            # Add request for metrics
            if "metrics" not in base_improved_prompt.lower() and "kpi" not in base_improved_prompt.lower():
                base_improved_prompt += "\n\nPlease also suggest 3-5 key metrics I should track to measure the success of this content strategy."
                changes_made.append("Added request for metrics")

            if changes_made:
                print("✓ Applied basic improvements to the base prompt:")
                for change in changes_made:
                    print(f"  • {change}")

        print(f"\n{'-' * 30} GENERATING VARIATIONS {'-' * 30}")

        # Generate variations for each model
        variations = {}
        model_features = {
            "gpt": ["Markdown formatting", "System message compatibility", "Function calling"],
            "claude": ["XML tag processing", "Table formatting", "Code analysis"],
            "gemini": ["Step-by-step instructions", "Visual reasoning", "Detailed examples"],
            "mistral": ["Concise responses", "Efficient token usage", "Direct answers"],
            "llama": ["Open-source compatibility", "Straightforward instructions", "Efficient prompting"]
        }

        for model in models:
            print(f"\nGenerating variation for {model}...")

            # Start with the base improved prompt
            variation = base_improved_prompt

            # Identify model family
            model_family = next((family for family in model_features.keys() if family in model.lower()), "general")

            # Print model-specific features being optimized for
            if model_family in model_features:
                print(f"  Optimizing for {model_family.upper()} features:")
                for feature in model_features[model_family]:
                    print(f"  • {feature}")

            # Customize for specific models
            if "gpt" in model.lower():
                # Add GPT-specific instructions
                variation += f"\n\nPlease format your response in a way that's easy to read and implement. Use markdown formatting with headers, bullet points, and numbered lists."

                # Add system message hint
                if "system message" not in variation.lower():
                    variation = f"[For GPT models] I need a comprehensive response. {variation}"

            elif "claude" in model.lower():
                # Add Claude-specific instructions
                variation += f"\n\nPlease organize your response with clear headings and structured sections. Feel free to use tables if appropriate."

                # Add XML tags hint for Claude
                if "<tag>" not in variation.lower():
                    variation += "\n\nYou can use <thinking> tags to show your reasoning process if helpful."

            elif "gemini" in model.lower() or "palm" in model.lower():
                # Add Google model specific instructions
                variation += f"\n\nPlease provide a detailed, step-by-step strategy that I can implement immediately. Include specific examples for each recommendation."

            elif "mistral" in model.lower() or "llama" in model.lower():
                # Add open-source model specific instructions
                variation += f"\n\nPlease be concise and direct in your recommendations. Focus on practical, actionable advice."

            variations[model] = variation

        # Update the prompt with all variations
        new_improved_versions = ""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Clear existing variations if they exist
        if "Variation" in improved_versions:
            # Keep only the first improved version (non-variation)
            if "Improvement" in improved_versions or "Improved" in improved_versions:
                end_of_improvement = improved_versions.find("---", improved_versions.find("---") + 3)
                if end_of_improvement > 0:
                    improved_versions = improved_versions[:end_of_improvement]
                else:
                    improved_versions = ""
            else:
                improved_versions = ""

        # Add the variations
        for model, variation in variations.items():
            if new_improved_versions:
                new_improved_versions += f"\n\n--- {model} (Variation generated on {timestamp}) ---\n{variation}"
            else:
                new_improved_versions = f"--- {model} (Variation generated on {timestamp}) ---\n{variation}"

        # Preserve existing improved versions if they exist
        if improved_versions:
            if new_improved_versions:
                new_improved_versions = improved_versions + "\n\n" + new_improved_versions
            else:
                new_improved_versions = improved_versions

        db.update_prompt(args.id, {'Improved Versions': new_improved_versions})

        print(f"\n{'-' * 30} SUMMARY {'-' * 30}")
        print(f"• Base prompt source: {base_source}")
        print(f"• Generated variations for {len(models)} models: {', '.join(models)}")
        print(f"• Each variation is optimized for the specific model's capabilities")
        print(f"• All variations have been saved to the database")

        print(f"\n{'-' * 30} NEXT STEPS {'-' * 30}")
        print("1. Review the variations using: python prompt_manager.py get --id " + args.id)
        print("2. Test the variations with their respective models")
        print("3. Update the prompt with any additional improvements")

        print(f"\n{'=' * 80}")
        print("Variations generated and saved to the database.")
        print(f"{'=' * 80}")

    elif args.command == 'process-new':
        # Detect prompts that need processing
        new_prompts = db.detect_new_prompts()

        if not new_prompts:
            print("\nNo new prompts found that need processing.")
            sys.exit(0)

        print(f"\n{'=' * 80}")
        print(f"FOUND {len(new_prompts)} PROMPTS THAT NEED PROCESSING")
        print(f"{'=' * 80}")

        # Display the prompts that need processing
        print("\nPrompts to process:")
        for i, prompt in enumerate(new_prompts, 1):
            prompt_id = prompt.get('Prompt ID', 'Unknown')
            prompt_title = prompt.get('Prompt Title', 'Untitled')
            prompt_text = prompt.get('Prompt Text', '')

            # Truncate prompt text for display
            if len(prompt_text) > 100:
                prompt_text = prompt_text[:97] + "..."

            print(f"{i}. ID: {prompt_id} | Title: {prompt_title}")
            print(f"   Text: {prompt_text}")
            print()

        # Ask for confirmation unless auto-approve is specified
        if not args.auto_approve:
            confirm = input("Process these prompts? (y/n): ")
            if confirm.lower() != 'y':
                print("Operation cancelled.")
                sys.exit(0)

        # Process each prompt
        success_count = 0
        for i, prompt in enumerate(new_prompts):
            prompt_id = prompt.get('Prompt ID', '')
            if prompt_id:
                print(f"\nProcessing prompt {prompt_id} ({i+1}/{len(new_prompts)})...")
                if db.auto_process_prompt(prompt_id, openrouter):
                    success_count += 1

                # Add a delay between processing prompts to avoid quota limits
                if i < len(new_prompts) - 1:  # Don't delay after the last prompt
                    print(f"Waiting 5 seconds before processing next prompt to avoid quota limits...")
                    time.sleep(5)

        print(f"\n{'=' * 80}")
        print(f"Processing complete. Successfully processed {success_count} out of {len(new_prompts)} prompts.")
        print(f"{'=' * 80}")

    elif args.command == 'auto-fill':
        # Process a specific prompt
        prompt = db.get_prompt(args.id, silent=True)
        if not prompt:
            print(f"Prompt with ID {args.id} not found")
            sys.exit(1)

        # Check if the prompt has text
        if not prompt.get('Prompt Text', '').strip():
            print(f"Prompt with ID {args.id} has no text to process")
            sys.exit(1)

        # Process the prompt
        if db.auto_process_prompt(args.id, openrouter):
            print(f"\n{'=' * 80}")
            print(f"Successfully processed prompt {args.id}")
            print(f"{'=' * 80}")
        else:
            print(f"\n{'=' * 80}")
            print(f"Failed to process prompt {args.id}")
            print(f"{'=' * 80}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
