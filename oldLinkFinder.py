import os
import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

# Create a Selenium WebDriver with headless options
def create_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Download the file using Selenium
def download_file_selenium(url, save_path):
    driver = create_selenium_driver()
    
    # Navigate to the URL
    driver.get(url)
    
    # Wait for the page to load (adjust the wait time or conditions as necessary)
    time.sleep(3)
    
    # If there's a button or a link to trigger the download, find and click it
    # Example: If there's a download button on the page
    try:
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="download_button_id"]'))  # Modify this with the correct XPATH
        )
        download_button.click()
        
        # Wait for the file to download (You can adjust this for specific timing or events)
        time.sleep(5)  # Wait for download to complete
        
    except Exception as e:
        print(f"Error while downloading the file: {e}")
    
    driver.quit()  # Close the browser after download

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

        # Download the file using Selenium
        download_file_selenium(url, save_path)

# Main execution
if __name__ == '__main__':
    client = authenticate_google_sheet()
    spreadsheet_name = 'Auto Old Link Updater'  # Replace with your spreadsheet name
    spreadsheet = open_spreadsheet(client, spreadsheet_name)
    process_and_download_files(spreadsheet)
