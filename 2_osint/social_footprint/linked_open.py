import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Read URLs from a file
def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

# Open URLs in a web browser
def open_urls_in_browser(urls):
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    for url in urls:
        driver.get(url)
        time.sleep(5)  # Wait for 5 seconds to allow the page to load
    
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_url_file>")
        sys.exit(1)

    url_file_path = sys.argv[1]  # Get filename from command-line arguments
    urls = read_urls(url_file_path)
    open_urls_in_browser(urls)
