import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
import urllib.parse


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
        if extract_old_pdfs == 'TRUE':  # If checkbox is checked
            post_title = row['post_title']
            url = row['URL']
            print(f"Processing: {post_title}")
            
            # Create a new tab for the post_title
            new_sheet = create_new_tab(spreadsheet, post_title)
            
            # Add links to sheet
            old_pdf_links = get_old_pdfs(url)
            for old_link in old_pdf_links:
                new_sheet.append_row([old_link, get_new_link(old_link), 'Pending'])

# Find the PDF links with sites/default/files
def get_old_pdfs(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to get {url}")
        return[]
    
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = []

    # Find all the links
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Filter by sites/default/files
        if 'sites/default/files' in href and href.endswith('.pdf'):
            pdf_links.append(href)
    
    return pdf_links

def get_new_link(old_link):
        # Extract the components of the URL
    url_parts = old_link.split('/')

    # Extract the filename and the date portion
    old_filename = url_parts[-1]
    date_str = url_parts[-5]  # The "762426" part from the URL
    old_filename = urllib.parse.unquote(old_filename)  # Decode the URL-encoded file name
    
    # Assuming the date is in YYYY-MM format (example: "2015-05" is in '762426' format)
    year = date_str[:4]
    month = date_str[4:6]

    # Replace spaces (%20) with dashes in the filename
    new_filename = old_filename.replace("%20", "-")

    # Construct the new URL
    new_link = f"https://law.stanford.edu/wp-content/uploads/{year}/{month}/{new_filename}"
    return new_link

# Main execution
if __name__ == '__main__':
    client = authenticate_google_sheet()
    spreadsheet_name = 'Auto Old Link Updater'  # Replace with your spreadsheet name
    spreadsheet = open_spreadsheet(client, spreadsheet_name)
    process_rows(spreadsheet)
