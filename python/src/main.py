import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="CC Analyzer")
parser.add_argument("--sheet-name", required=True, help="Name of the Google Sheet")
args = parser.parse_args()

sheet_name = args.sheet_name

sheet_name = sys.argv[1]  # Get the sheet name from the command-line arguments

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("src/credentials.json", scope)

client = gspread.authorize(creds)
sheet = client.open(sheet_name)

# TODO: Depending on passed param
current_month_year = datetime.now().strftime("%B %Y")
new_worksheet = sheet.add_worksheet(title=current_month_year, rows="100", cols="20")

# Reorder worksheets to make the new worksheet the leftmost (first)
worksheets = sheet.worksheets()
sheet.reorder_worksheets([new_worksheet] + [ws for ws in worksheets if ws != new_worksheet])

new_worksheet.append_row(["Transaction", "Post date", "Merchant", "Amount", "Notes", "Shoulder", "C", "S"])