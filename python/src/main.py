import gspread
from oauth2client.service_account import ServiceAccountCredentials
import argparse
from PyPDF2 import PdfReader
import re

# parse passed params
parser = argparse.ArgumentParser(description="CC Analyzer")
parser.add_argument("--sheet-name", required=True, help="Name of the Google Sheet")
parser.add_argument("--billing-period", required=True, help="Name of the worksheet to create")
parser.add_argument("--pdf-path", required=True, help="Path to the PDF file")
parser.add_argument("--pdf-password", required=True, help="Password for the PDF file")

args = parser.parse_args()

# load passed params to variables
sheet_name = args.sheet_name
billing_period = args.billing_period
pdf_path = args.pdf_path
pdf_password = args.pdf_password

# read PDF file
reader = PdfReader(pdf_path)

# decrypt PDF password
if reader.is_encrypted:
    reader.decrypt(pdf_password)

# TODO: remove CR and Payments
pdf_data = []

for page in reader.pages:
    text = page.extract_text()

    # Define a regular expression to match rows in the table
    table_pattern = re.compile(r"(\d{2}/\d{2}/\d{2})\s+(\d{2}/\d{2}/\d{2})\s+(.+?)\s+([\d,]+\.\d{2})")
    matches = table_pattern.findall(text)

    # Print the extracted rows
    for match in matches:
        tran_date, post_date, description, amount = match
        pdf_data.append([tran_date, post_date, description, amount, "", "", "", ""])

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("src/credentials.json", scope)

client = gspread.authorize(creds)
sheet = client.open(sheet_name)

# check if a worksheet with the same name already exists
existing_titles = [ws.title for ws in sheet.worksheets()]
if billing_period in existing_titles:
    raise ValueError(f"The following billing period already exists('{billing_period}')!")

# length of data + 10 extra row
row_length = str(len(pdf_data) + 10)

# create new worksheet
new_worksheet = sheet.add_worksheet(title=billing_period, rows=row_length, cols="20")

# TODO: doesn't work
# reorder worksheets to put the new worksheet at the left
worksheets = sheet.worksheets()
sheet.reorder_worksheets([new_worksheet] + [ws for ws in worksheets if ws != new_worksheet])

# header columns
header_cell_format = gspread.format.CellFormat(textFormat={"bold": True})
new_worksheet.append_row(["Transaction", "Post date", "Merchant", "Amount", "Notes", "Shoulder", "C", "S"])
new_worksheet.format("A1:H1", header_cell_format)

# TODO: Add summary

# load pulled pdf data to worksheet
new_worksheet.append_rows(pdf_data, value_input_option="USER_ENTERED")

sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet.id}"
print("Success", sheet_url)