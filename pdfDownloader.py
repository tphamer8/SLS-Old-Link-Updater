import os
import requests

# Set your download directory
download_dir = "/Users/tpham/Documents/Stanford Webmaster Files/File Reuploads/Automated Downloads"
os.makedirs(download_dir, exist_ok=True)

# Example PDF URL from Stanford Law
url = "https://law.stanford.edu/wp-content/uploads/sites/default/files/child-page/762426/doc/slspublic/SPLS%202015%20-%20Final%20Schedule.pdf"

# Set a filename (you can extract from URL or set a custom one)
filename = os.path.join(download_dir, "SPLS_2015_Final_Schedule.pdf")

# Try to fetch the file with proper headers
try:
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }, stream=True)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

except Exception as e:
    print(f"Error downloading: {e}")
