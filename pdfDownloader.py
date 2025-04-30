import os
import requests
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

# Download the file from the given URL
def download_file(url, save_path):
    response = requests.get(url)
    
    # Ensure the request was successful
    if response.status_code == 200:
        # Write the content to a local file
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

# Process rows and download files
def process_and_download_files(spreadsheet):
    old_files = spreadsheet.worksheet('Old Files')  # Access "Old Files" sheet
    rows = old_files.get_all_records()  # Fetch all rows

    for row in rows:
        url = row['URL']  # Get the file URL from the "Old Files" sheet
        file_name = url.split("/")[-1]  # Get the file name from the URL (assuming it's the last part of the URL)
        
        # Specify where to save the downloaded file
        save_path = os.path.join('downloads', file_name)

        # Ensure the 'downloads' directory exists
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        # Download the file
        download_file(url, save_path)

# Main execution
if __name__ == '__main__':
    client = authenticate_google_sheet()
    spreadsheet_name = 'Auto Old Link Updater'  # Replace with your spreadsheet name
    spreadsheet = open_spreadsheet(client, spreadsheet_name)
    process_and_download_files(spreadsheet)
