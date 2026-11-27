"""Starter program: read and add rows in a Google Sheet.

Setup:  pip install gspread
Put your OAuth client file (Desktop app) next to this file as
credentials.json, then paste your spreadsheet ID below. The first run
opens your browser so you can sign in.
"""

from pathlib import Path

import gspread

CREDENTIALS_FILE = Path(__file__).with_name("credentials.json")
TOKEN_FILE = Path(__file__).with_name("authorized_user.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets_MOEW"]
SPREADSHEET_ID = "1A9sH8WMptPrmC7Eo07X08JwgijW_MOOOOEEEWWWW-5Xg"


def connect():
    """Return the first tab of the spreadsheet."""
    client = gspread.oauth(
        scopes=SCOPES,
        credentials_filename=CREDENTIALS_FILE,
        authorized_user_filename=TOKEN_FILE,
    )
    return client.open_by_key(SPREADSHEET_ID).sheet1


def show_rows(sheet):
    rows = sheet.get_all_values()
    if not any(rows):
        print("The sheet is empty.")
        return
    for number, row in enumerate(rows, start=1):
        print(f"{number}: " + " | ".join(row))


def add_row(sheet):
    text = input("Enter values separated by commas: ")
    values = [value.strip() for value in text.split(",")]
    if not any(values):
        print("Nothing to add.")
        return
    sheet.append_row(values)
    print("Row added.")


def color(red, green, blue):
    """Turn normal 0-255 color numbers into the 0-1 scale Google uses."""
    return {"red": red / 255, "green": green / 255, "blue": blue / 255}


def make_colorful(sheet):
    headings = ["Item", "Quantity", "Price"]
    if sheet.row_values(1) != headings:
        sheet.insert_row(headings, index=1)  # existing rows move down

    formats = [
        {
            "range": "A1:C1",
            "format": {
                "backgroundColor": color(214, 51, 132),
                "horizontalAlignment": "CENTER",
                "textFormat": {
                    "bold": True,
                    "fontSize": 12,
                    "foregroundColor": color(255, 255, 255),
                },
            },
        }
    ]
    for row in range(2, 31):
        shade = color(255, 228, 240) if row % 2 == 0 else color(230, 240, 255)
        formats.append(
            {"range": f"A{row}:C{row}", "format": {"backgroundColor": shade}}
        )

    sheet.batch_format(formats)
    sheet.freeze(rows=1)
    print("Your sheet is now colorful!")


def main():
    if not CREDENTIALS_FILE.exists():
        print(f"Missing file: {CREDENTIALS_FILE}")
        return

    try:
        sheet = connect()
    except gspread.exceptions.SpreadsheetNotFound:
        print("Spreadsheet not found. Check the ID.")
        return
    except PermissionError:
        print("Access denied. Sign in with an account that can edit the sheet,")
        print("and check that the Google Sheets API is enabled.")
        return

    while True:
        choice = input("\n1) Show rows  2) Add row  3) Make it colorful  4) Quit: ").strip()
        if choice == "1":
            show_rows(sheet)
        elif choice == "2":
            add_row(sheet)
        elif choice == "3":
            make_colorful(sheet)
        elif choice == "4":
            break
        else:
            print("Choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
