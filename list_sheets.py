#!/usr/bin/env python3
"""
List all sheets in a Google Spreadsheet
"""

import os
import sys
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

def list_sheets():
    """List all sheets in the spreadsheet."""
    try:
        # Authenticate with Google Sheets API
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # Get spreadsheet metadata
        spreadsheet = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
        
        print(f"Spreadsheet: {spreadsheet.get('properties', {}).get('title', 'Unknown')}")
        print(f"Spreadsheet ID: {SPREADSHEET_ID}")
        print("\nSheets:")
        
        # List all sheets
        for s in spreadsheet.get('sheets', []):
            properties = s.get('properties', {})
            sheet_id = properties.get('sheetId', 'Unknown')
            title = properties.get('title', 'Unknown')
            index = properties.get('index', 'Unknown')
            
            print(f"  - {title} (ID: {sheet_id}, Index: {index})")
        
        return True
    except HttpError as error:
        print(f"Error accessing spreadsheet: {error}")
        return False

if __name__ == "__main__":
    list_sheets()
