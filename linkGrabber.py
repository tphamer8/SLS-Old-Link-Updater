from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Set up the Selenium WebDriver with WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# The URL of the WordPress page you want to access
url = 'https://law.stanford.edu/?p=59093'

# Navigate to the URL
driver.get(url)

# Wait for a few seconds to let the page load (adjust time if necessary)
time.sleep(3)

# Get the page source (HTML)
html = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Print the HTML content (or you can manipulate it as needed)
print(soup.prettify())  # This formats the HTML for better readability