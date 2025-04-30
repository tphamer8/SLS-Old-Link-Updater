import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

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

# Configure Selenium WebDriver for downloading files
def create_selenium_driver(download_dir):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Set Chrome preferences to auto-download files to a specific directory
    prefs = {
        "download.default_directory": download_dir,  # Path to the directory to save downloaded files
        "download.prompt_for_download": False,  # Disable download prompt
        "directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def create_selenium_driver(download_dir):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Set Chrome preferences to auto-download files to a specific directory
    prefs = {
        "download.default_directory": download_dir,  # Path to the directory to save downloaded files
        "download.prompt_for_download": False,  # Disable download prompt
        "directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def download_file_selenium(url, download_dir):
    driver = create_selenium_driver(download_dir)
    driver.get(url)
    time.sleep(5)
    driver.quit()

# Process rows and add data to "Old files" sheet
def process_rows(spreadsheet):
    old_files = spreadsheet.worksheet('Old Files')  # Access "Old Files" sheet
    rows = old_files.get_all_records()  # Fetch all rows

    download_dir = '/Users/tpham/Documents/Stanford Webmaster Files/File Reuploads/Automated Downloads'

    for row_idx, row in enumerate(rows, start=2):  # start=2 because Google Sheets is 1-indexed
        if row['Type'] == 'PDF' and row['Status'] == 'Pending' :  # check if pdf has been downloaded
            url = row['URL']
            file_name = url.split("/")[-1]
            print(f"Downloading: {url}")
            
            # Update the "Status" column
            old_files.update_cell(row_idx, 5, 'Downloaded')

            # Specify where to save the downloaded file
            save_path = os.path.join(download_dir, file_name)

            # Download the file
            download_file_selenium(url, download_dir)

# Main execution
if __name__ == '__main__':
    client = authenticate_google_sheet()
    spreadsheet_name = 'Auto Old Link Updater'  # Replace with your spreadsheet name
    spreadsheet = open_spreadsheet(client, spreadsheet_name)
    process_rows(spreadsheet)