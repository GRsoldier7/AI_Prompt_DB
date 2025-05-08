#!/usr/bin/env python3
"""
Google Sheet Cleanup Script

This script cleans up and reformats the prompt database Google Sheet.
It preserves existing data while organizing it into a clean, consistent format.
"""

import os
import sys
import json
import datetime
from typing import List, Dict, Any
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

# Define the proper column headers
COLUMNS = [
    'Prompt ID', 'Prompt Title', 'Prompt Text', 'Category', 'Subcategory',
    'Primary Tool', 'Compatible Tools', 'Effectiveness Rating', 'Tags',
    'Creation Date', 'Last Modified', 'Notes', 'Improvement Suggestions',
    'Improved Versions'
]

def get_sheet_service():
    """Authenticate and get the Google Sheets service."""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        return service.spreadsheets()
    except Exception as e:
        print(f"Error authenticating with Google Sheets: {e}")
        sys.exit(1)

def get_sheet_data(sheet):
    """Get all data from the sheet."""
    try:
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:Z"  # Get all columns to ensure we don't miss any data
        ).execute()

        return result.get('values', [])
    except HttpError as error:
        print(f"Error retrieving sheet data: {error}")
        return []

def get_sheet_id(sheet):
    """Get the sheet ID for the current sheet."""
    try:
        sheet_metadata = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', [])

        print(f"Available sheets in spreadsheet:")
        for s in sheets:
            sheet_title = s['properties']['title']
            sheet_id = s['properties']['sheetId']
            print(f"  - {sheet_title} (ID: {sheet_id})")

            # Case-insensitive comparison to be safe
            if sheet_title.lower() == SHEET_NAME.lower():
                print(f"Found sheet: {sheet_title} with ID: {sheet_id}")
                return sheet_id

        print(f"Sheet {SHEET_NAME} not found in the available sheets")
        # If we can't find the exact sheet, use the first one as a fallback
        if sheets:
            first_sheet = sheets[0]['properties']
            print(f"Using first available sheet as fallback: {first_sheet['title']} (ID: {first_sheet['sheetId']})")
            return first_sheet['sheetId']
        return None
    except HttpError as error:
        print(f"Error getting sheet ID: {error}")
        return None

def clear_sheet(sheet):
    """Clear all content from the sheet."""
    try:
        sheet.values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:Z"
        ).execute()
        print(f"Cleared all content from {SHEET_NAME}")
        return True
    except HttpError as error:
        print(f"Error clearing sheet: {error}")
        return False

def extract_prompt_data(values):
    """Extract prompt data from the sheet values."""
    if not values:
        return []

    # Try to identify the columns based on the headers
    headers = values[0]
    header_map = {}

    # Map existing headers to our expected columns
    for i, header in enumerate(headers):
        header_lower = header.lower() if header else ""

        # Direct matches
        if header in COLUMNS:
            header_map[i] = COLUMNS.index(header)
        # Prompt ID
        elif "id" in header_lower or "prompt id" in header_lower:
            header_map[i] = 0
        # Prompt Title
        elif "title" in header_lower or "name" in header_lower:
            header_map[i] = 1
        # Prompt Text
        elif "text" in header_lower or "content" in header_lower or "prompt" in header_lower:
            header_map[i] = 2
        # Category
        elif "category" in header_lower and "sub" not in header_lower:
            header_map[i] = 3
        # Subcategory
        elif "subcategory" in header_lower or "sub-category" in header_lower or "sub category" in header_lower:
            header_map[i] = 4
        # Primary Tool
        elif ("tool" in header_lower and "primary" in header_lower) or "model" in header_lower:
            header_map[i] = 5
        # Compatible Tools
        elif "compatible" in header_lower or ("tool" in header_lower and "other" in header_lower):
            header_map[i] = 6
        # Effectiveness Rating
        elif "rating" in header_lower or "effectiveness" in header_lower or "score" in header_lower:
            header_map[i] = 7
        # Tags
        elif "tag" in header_lower or "keyword" in header_lower:
            header_map[i] = 8
        # Creation Date
        elif ("create" in header_lower and "date" in header_lower) or "created" in header_lower:
            header_map[i] = 9
        # Last Modified
        elif "modified" in header_lower or "updated" in header_lower or "last edit" in header_lower:
            header_map[i] = 10
        # Notes
        elif "note" in header_lower or "comment" in header_lower:
            header_map[i] = 11
        # Improvement Suggestions
        elif "suggestion" in header_lower or "improve" in header_lower:
            header_map[i] = 12
        # Improved Versions
        elif "version" in header_lower or "variation" in header_lower:
            header_map[i] = 13

    # Extract data from rows
    prompts = []
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    for i, row in enumerate(values[1:], 1):  # Skip header row
        # Initialize a new prompt with empty values
        prompt = [""] * len(COLUMNS)

        # Map data from the row using the header map
        for col_idx, value in enumerate(row):
            if col_idx in header_map:
                mapped_idx = header_map[col_idx]
                prompt[mapped_idx] = value

        # Ensure Prompt ID exists
        if not prompt[0]:
            prompt[0] = f"P{i:03d}"

        # Ensure dates exist
        if not prompt[9]:  # Creation Date
            prompt[9] = current_date
        if not prompt[10]:  # Last Modified
            prompt[10] = current_date

        prompts.append(prompt)

    return prompts

def format_sheet(sheet, sheet_id):
    """Apply formatting to the sheet."""
    try:
        # Define column widths for better readability
        column_widths = [
            100,  # Prompt ID
            200,  # Prompt Title
            400,  # Prompt Text
            150,  # Category
            150,  # Subcategory
            150,  # Primary Tool
            200,  # Compatible Tools
            150,  # Effectiveness Rating
            200,  # Tags
            120,  # Creation Date
            120,  # Last Modified
            300,  # Notes
            400,  # Improvement Suggestions
            400   # Improved Versions
        ]

        # Define column colors for better visual organization
        header_colors = {
            "metadata": {"red": 0.8, "green": 0.9, "blue": 1.0},  # Light blue for metadata
            "content": {"red": 0.9, "green": 1.0, "blue": 0.9},   # Light green for content
            "analysis": {"red": 1.0, "green": 0.9, "blue": 0.9}   # Light red for analysis
        }

        # Map columns to color categories
        column_color_map = [
            "metadata",  # Prompt ID
            "metadata",  # Prompt Title
            "content",   # Prompt Text
            "metadata",  # Category
            "metadata",  # Subcategory
            "metadata",  # Primary Tool
            "metadata",  # Compatible Tools
            "analysis",  # Effectiveness Rating
            "metadata",  # Tags
            "metadata",  # Creation Date
            "metadata",  # Last Modified
            "analysis",  # Notes
            "analysis",  # Improvement Suggestions
            "content"    # Improved Versions
        ]

        # Format header row (bold, freeze, colors)
        requests = [
            # Bold header row with background color
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {"bold": True},
                            "backgroundColor": {
                                "red": 0.2,
                                "green": 0.2,
                                "blue": 0.2
                            },
                            "horizontalAlignment": "CENTER",
                            "textFormat": {
                                "foregroundColor": {
                                    "red": 1.0,
                                    "green": 1.0,
                                    "blue": 1.0
                                },
                                "bold": True,
                                "fontSize": 11
                            }
                        }
                    },
                    "fields": "userEnteredFormat(textFormat,backgroundColor,horizontalAlignment)"
                }
            },
            # Freeze header row
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "gridProperties": {
                            "frozenRowCount": 1
                        }
                    },
                    "fields": "gridProperties.frozenRowCount"
                }
            }
        ]

        # Set column widths
        for i, width in enumerate(column_widths):
            requests.append({
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": i,
                        "endIndex": i + 1
                    },
                    "properties": {
                        "pixelSize": width
                    },
                    "fields": "pixelSize"
                }
            })

        # Color code the columns
        for i, color_category in enumerate(column_color_map):
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,  # Skip header row
                        "startColumnIndex": i,
                        "endColumnIndex": i + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": header_colors[color_category]
                        }
                    },
                    "fields": "userEnteredFormat.backgroundColor"
                }
            })

        # Add alternating row colors for better readability
        requests.append({
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{
                        "sheetId": sheet_id,
                        "startRowIndex": 1  # Skip header row
                    }],
                    "booleanRule": {
                        "condition": {
                            "type": "CUSTOM_FORMULA",
                            "values": [{
                                "userEnteredValue": "=MOD(ROW(),2)=0"
                            }]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 0.95,
                                "green": 0.95,
                                "blue": 0.95
                            }
                        }
                    }
                },
                "index": 0
            }
        })

        # Add borders to cells
        requests.append({
            "updateBorders": {
                "range": {
                    "sheetId": sheet_id
                },
                "top": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0.7,
                        "green": 0.7,
                        "blue": 0.7
                    }
                },
                "bottom": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0.7,
                        "green": 0.7,
                        "blue": 0.7
                    }
                },
                "left": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0.7,
                        "green": 0.7,
                        "blue": 0.7
                    }
                },
                "right": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0.7,
                        "green": 0.7,
                        "blue": 0.7
                    }
                },
                "innerHorizontal": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0.7,
                        "green": 0.7,
                        "blue": 0.7
                    }
                },
                "innerVertical": {
                    "style": "SOLID",
                    "width": 1,
                    "color": {
                        "red": 0.7,
                        "green": 0.7,
                        "blue": 0.7
                    }
                }
            }
        })

        # Apply text wrapping to content columns
        for i in [2, 11, 12, 13]:  # Prompt Text, Notes, Improvement Suggestions, Improved Versions
            requests.append({
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,  # Skip header row
                        "startColumnIndex": i,
                        "endColumnIndex": i + 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "wrapStrategy": "WRAP"
                        }
                    },
                    "fields": "userEnteredFormat.wrapStrategy"
                }
            })

        # Apply formatting
        sheet.batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": requests}
        ).execute()

        print("Applied enhanced formatting to the sheet")
        return True
    except HttpError as error:
        print(f"Error formatting sheet: {error}")
        return False

def rebuild_sheet():
    """Rebuild the sheet with clean, organized data."""
    print(f"Starting cleanup of Google Sheet: {SPREADSHEET_ID}, Sheet: {SHEET_NAME}")

    # Get the sheet service
    sheet = get_sheet_service()

    # Get the sheet ID
    sheet_id = get_sheet_id(sheet)
    if sheet_id is None:  # Only check for None, not for falsy values like 0
        print("Could not find the sheet. Please check the sheet name and spreadsheet ID.")
        return False

    print(f"Proceeding with sheet ID: {sheet_id}")

    # Get existing data
    print("Retrieving existing data...")
    values = get_sheet_data(sheet)

    if not values:
        print("No data found in the sheet.")
        # Create a new sheet with headers
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A1",
            valueInputOption="RAW",
            body={"values": [COLUMNS]}
        ).execute()
        print(f"Created new sheet with headers: {', '.join(COLUMNS)}")
        format_sheet(sheet, sheet_id)
        return True

    # Extract prompt data
    print("Extracting and organizing prompt data...")
    prompts = extract_prompt_data(values)

    # Clear the sheet
    clear_sheet(sheet)

    # Add headers
    print("Adding headers...")
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A1",
        valueInputOption="RAW",
        body={"values": [COLUMNS]}
    ).execute()

    # Add prompt data
    if prompts:
        print(f"Adding {len(prompts)} prompts...")
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A2",
            valueInputOption="RAW",
            body={"values": prompts}
        ).execute()

    # Format the sheet
    format_sheet(sheet, sheet_id)

    print("Sheet cleanup complete!")
    return True

if __name__ == "__main__":
    rebuild_sheet()
