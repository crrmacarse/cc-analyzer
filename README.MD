# CC Analyzer

Bored and tried to build a CC analysis tool to streamline my monthly validation process of my CC bills.

## Python Implementation (Recommended)

### Prerequisites

- Head over to `python` folder
- Enable Google Sheets and Google Drive API in Google Cloud Console
- Share targeted Google sheet file to Service account email as "Editor"
- Add Service Account's JSON file as `credentials.json` under `src` folder
- Download PDF file of your CC bill

### Install Dependencies

```
pip install -r requirements.txt
```

### Running the app

```
python3 src/main.py --sheet-name "NAME_OF_GOOGLE_SHEET" --billing-period "MMMM YYYYY" --pdf-path "pdf/path" --pdf-password "pdf_password" 
```

> Supported Credit Card: Security Bank

## Node Implementation (DEPRECATED)

```
npm run start -- --bank <bank> --card <card> --table <string of table>

#example
npm run start -- --card World --date "March 2025" --table <table string>
```

> It is important to add `--` to allow usage of args. Only applicable on CLI