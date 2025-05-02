import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import argparse

# TODO: Add file from Secbank itself
parser = argparse.ArgumentParser(description="CC Analyzer")
parser.add_argument("--sheet-name", required=True, help="Name of the Google Sheet")
parser.add_argument("--billing-period", required=True, help="Name of the worksheet to create")
args = parser.parse_args()

sheet_name = args.sheet_name
billing_period = args.billing_period

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("src/credentials.json", scope)

client = gspread.authorize(creds)
sheet = client.open(sheet_name)

# Check if a worksheet with the same name already exists
existing_titles = [ws.title for ws in sheet.worksheets()]
if billing_period in existing_titles:
    raise ValueError(f"The following billing period already exists('{billing_period}')!")

new_worksheet = sheet.add_worksheet(title=billing_period, rows="100", cols="20")

# Reorder worksheets to make the new worksheet the leftmost (first)
worksheets = sheet.worksheets()
sheet.reorder_worksheets([new_worksheet] + [ws for ws in worksheets if ws != new_worksheet])

new_worksheet.append_row(["Transaction", "Post date", "Merchant", "Amount", "Notes", "Shoulder", "C", "S"])