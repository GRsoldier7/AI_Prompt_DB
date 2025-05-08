#!/usr/bin/env python3
"""
Prompt Database Manager

This script provides functionality to manage a database of prompts stored in a Google Sheet.
It allows for adding, editing, retrieving, and improving prompts.
"""

import os
import sys
import json
import datetime
from typing import List, Dict, Any, Optional, Union
import argparse
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'n8n-integrations-452015-811dc210bea2.json'
SPREADSHEET_ID = '1gBM_HxkjCrlBhmHT7i0CZoEpdKRkJa9ZGjd2xX3755M'
SHEET_NAME = 'Prompts'

# Column definitions
COLUMNS = [
    'Prompt ID', 'Prompt Title', 'Prompt Text', 'Category', 'Subcategory',
    'Primary Tool', 'Compatible Tools', 'Effectiveness Rating', 'Tags',
    'Creation Date', 'Last Modified', 'Notes', 'Improvement Suggestions'
]

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
                    range=f"{self.sheet_name}!A1:M1",
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
                
                # Add data validation for categories
                self._add_data_validation()
                
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
    
    def _add_data_validation(self):
        """Add data validation for category and subcategory columns."""
        # This would be expanded in a real implementation to add dropdown lists
        # for categories, subcategories, and tools
        pass
    
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
                range=f"{self.sheet_name}!A:M"
            ).execute()
            
            values = result.get('values', [])
            
            if not values or len(values) <= 1:
                return []
            
            # Convert to list of dictionaries
            headers = values[0]
            data = []
            
            for row in values[1:]:
                # Pad row if it's shorter than headers
                padded_row = row + [''] * (len(headers) - len(row))
                data.append(dict(zip(headers, padded_row)))
            
            return data
        
        except HttpError as error:
            print(f"Error retrieving prompts: {error}")
            return []
    
    def add_prompt(self, prompt_data: Dict[str, Any]) -> bool:
        """Add a new prompt to the database."""
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
                prompt_data.get('Improvement Suggestions', '')
            ]
            
            # Append to sheet
            self.sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A:M",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={
                    "values": [row_data]
                }
            ).execute()
            
            print(f"Added new prompt with ID: {prompt_id}")
            return True
        
        except HttpError as error:
            print(f"Error adding prompt: {error}")
            return False
    
    def update_prompt(self, prompt_id: str, prompt_data: Dict[str, Any]) -> bool:
        """Update an existing prompt."""
        try:
            # Get all prompts
            prompts = self.get_all_prompts()
            
            # Find the prompt with the given ID
            row_index = None
            for i, prompt in enumerate(prompts):
                if prompt.get('Prompt ID') == prompt_id:
                    row_index = i + 2  # +2 because of 0-indexing and header row
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
                prompt_data.get('Prompt Title', prompts[row_index-2].get('Prompt Title', '')),
                prompt_data.get('Prompt Text', prompts[row_index-2].get('Prompt Text', '')),
                prompt_data.get('Category', prompts[row_index-2].get('Category', '')),
                prompt_data.get('Subcategory', prompts[row_index-2].get('Subcategory', '')),
                prompt_data.get('Primary Tool', prompts[row_index-2].get('Primary Tool', '')),
                prompt_data.get('Compatible Tools', prompts[row_index-2].get('Compatible Tools', '')),
                prompt_data.get('Effectiveness Rating', prompts[row_index-2].get('Effectiveness Rating', '')),
                prompt_data.get('Tags', prompts[row_index-2].get('Tags', '')),
                prompts[row_index-2].get('Creation Date', ''),  # Keep original creation date
                current_date,  # Update last modified
                prompt_data.get('Notes', prompts[row_index-2].get('Notes', '')),
                prompt_data.get('Improvement Suggestions', prompts[row_index-2].get('Improvement Suggestions', ''))
            ]
            
            # Update the row
            self.sheet.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A{row_index}:M{row_index}",
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
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt from the database."""
        try:
            # Get all prompts
            prompts = self.get_all_prompts()
            
            # Find the prompt with the given ID
            row_index = None
            for i, prompt in enumerate(prompts):
                if prompt.get('Prompt ID') == prompt_id:
                    row_index = i + 2  # +2 because of 0-indexing and header row
                    break
            
            if row_index is None:
                print(f"Prompt with ID {prompt_id} not found")
                return False
            
            # Delete the row
            request = {
                "deleteDimension": {
                    "range": {
                        "sheetId": self._get_sheet_id(),
                        "dimension": "ROWS",
                        "startIndex": row_index - 1,  # 0-indexed
                        "endIndex": row_index  # exclusive
                    }
                }
            }
            
            self.sheet.batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={'requests': [request]}
            ).execute()
            
            print(f"Deleted prompt with ID: {prompt_id}")
            return True
        
        except HttpError as error:
            print(f"Error deleting prompt: {error}")
            return False
    
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
    
    def export_to_csv(self, filename: str) -> bool:
        """Export the prompt database to a CSV file."""
        try:
            prompts = self.get_all_prompts()
            df = pd.DataFrame(prompts)
            df.to_csv(filename, index=False)
            print(f"Exported prompts to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def import_from_csv(self, filename: str) -> bool:
        """Import prompts from a CSV file."""
        try:
            df = pd.read_csv(filename)
            
            # Convert DataFrame to list of dictionaries
            prompts = df.to_dict('records')
            
            # Clear existing data (except header)
            self.sheet.values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A2:M"
            ).execute()
            
            # Prepare data for batch update
            values = []
            for prompt in prompts:
                row = [
                    prompt.get('Prompt ID', ''),
                    prompt.get('Prompt Title', ''),
                    prompt.get('Prompt Text', ''),
                    prompt.get('Category', ''),
                    prompt.get('Subcategory', ''),
                    prompt.get('Primary Tool', ''),
                    prompt.get('Compatible Tools', ''),
                    prompt.get('Effectiveness Rating', ''),
                    prompt.get('Tags', ''),
                    prompt.get('Creation Date', ''),
                    prompt.get('Last Modified', ''),
                    prompt.get('Notes', ''),
                    prompt.get('Improvement Suggestions', '')
                ]
                values.append(row)
            
            # Update sheet
            self.sheet.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A2",
                valueInputOption="RAW",
                body={
                    "values": values
                }
            ).execute()
            
            print(f"Imported {len(prompts)} prompts from {filename}")
            return True
        
        except Exception as e:
            print(f"Error importing from CSV: {e}")
            return False

def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(description='Prompt Database Manager')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List all prompts
    list_parser = subparsers.add_parser('list', help='List all prompts')
    
    # Add a new prompt
    add_parser = subparsers.add_parser('add', help='Add a new prompt')
    add_parser.add_argument('--title', required=True, help='Prompt title')
    add_parser.add_argument('--text', required=True, help='Prompt text')
    add_parser.add_argument('--category', required=True, help='Category')
    add_parser.add_argument('--subcategory', help='Subcategory')
    add_parser.add_argument('--tool', help='Primary tool')
    add_parser.add_argument('--compatible', help='Compatible tools (comma-separated)')
    add_parser.add_argument('--rating', help='Effectiveness rating (1-10)')
    add_parser.add_argument('--tags', help='Tags (comma-separated)')
    add_parser.add_argument('--notes', help='Additional notes')
    add_parser.add_argument('--suggestions', help='Improvement suggestions')
    
    # Update an existing prompt
    update_parser = subparsers.add_parser('update', help='Update an existing prompt')
    update_parser.add_argument('--id', required=True, help='Prompt ID')
    update_parser.add_argument('--title', help='Prompt title')
    update_parser.add_argument('--text', help='Prompt text')
    update_parser.add_argument('--category', help='Category')
    update_parser.add_argument('--subcategory', help='Subcategory')
    update_parser.add_argument('--tool', help='Primary tool')
    update_parser.add_argument('--compatible', help='Compatible tools (comma-separated)')
    update_parser.add_argument('--rating', help='Effectiveness rating (1-10)')
    update_parser.add_argument('--tags', help='Tags (comma-separated)')
    update_parser.add_argument('--notes', help='Additional notes')
    update_parser.add_argument('--suggestions', help='Improvement suggestions')
    
    # Delete a prompt
    delete_parser = subparsers.add_parser('delete', help='Delete a prompt')
    delete_parser.add_argument('--id', required=True, help='Prompt ID')
    
    # Filter prompts
    filter_parser = subparsers.add_parser('filter', help='Filter prompts')
    filter_parser.add_argument('--category', help='Filter by category')
    filter_parser.add_argument('--subcategory', help='Filter by subcategory')
    filter_parser.add_argument('--tool', help='Filter by primary tool')
    filter_parser.add_argument('--tags', help='Filter by tags (comma-separated)')
    
    # Export to CSV
    export_parser = subparsers.add_parser('export', help='Export prompts to CSV')
    export_parser.add_argument('--file', required=True, help='Output CSV file')
    
    # Import from CSV
    import_parser = subparsers.add_parser('import', help='Import prompts from CSV')
    import_parser.add_argument('--file', required=True, help='Input CSV file')
    
    args = parser.parse_args()
    
    # Initialize the PromptDB
    db = PromptDB()
    
    if args.command == 'list':
        prompts = db.get_all_prompts()
        if prompts:
            for prompt in prompts:
                print(f"{prompt.get('Prompt ID')}: {prompt.get('Prompt Title')}")
        else:
            print("No prompts found")
    
    elif args.command == 'add':
        prompt_data = {
            'Prompt Title': args.title,
            'Prompt Text': args.text,
            'Category': args.category,
            'Subcategory': args.subcategory or '',
            'Primary Tool': args.tool or '',
            'Compatible Tools': args.compatible or '',
            'Effectiveness Rating': args.rating or '',
            'Tags': args.tags or '',
            'Notes': args.notes or '',
            'Improvement Suggestions': args.suggestions or ''
        }
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
        if args.rating:
            prompt_data['Effectiveness Rating'] = args.rating
        if args.tags:
            prompt_data['Tags'] = args.tags
        if args.notes:
            prompt_data['Notes'] = args.notes
        if args.suggestions:
            prompt_data['Improvement Suggestions'] = args.suggestions
        
        db.update_prompt(args.id, prompt_data)
    
    elif args.command == 'delete':
        db.delete_prompt(args.id)
    
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
    
    elif args.command == 'export':
        db.export_to_csv(args.file)
    
    elif args.command == 'import':
        db.import_from_csv(args.file)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
