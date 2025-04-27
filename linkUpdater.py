import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Sheets
def authenticate_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Open the spreadsheet
def open_spreadsheet(client, spreadsheet_name):
    spreadsheet = client.open(spreadsheet_name)
    return spreadsheet

# Create new tab and initialize columns
def create_new_tab(spreadsheet, post_title):
    spreadsheet.add_worksheet(title=post_title, rows="100", cols="3")
    new_sheet = spreadsheet.worksheet(post_title)
    new_sheet.append_row(['Old Link', 'New Link', 'Status'])
    return new_sheet

# Process rows and create tabs
def process_rows(spreadsheet):
    sheet = spreadsheet.get_worksheet(0)  # Access the first sheet
    rows = sheet.get_all_records()  # Fetch all rows

    for row in rows:
        extract_old_pdfs = row['Extract Old PDFs']  # Get checkbox value
        if extract_old_pdfs:  # If checkbox is checked
            post_title = row['post_title']
            print(f"Processing: {post_title}")
            
            # Create a new tab for the post_title
            new_sheet = create_new_tab(spreadsheet, post_title)
            
            # Add placeholder data (Replace this with actual old/new link extraction)
            new_sheet.append_row(['https://old-link.com', 'https://new-link.com', 'Pending'])

# Main execution
if __name__ == '__main__':
    client = authenticate_google_sheet()
    spreadsheet_name = 'Auto Old Link Updater'  # Replace with your spreadsheet name
    spreadsheet = open_spreadsheet(client, spreadsheet_name)
    process_rows(spreadsheet)
