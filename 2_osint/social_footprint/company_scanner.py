from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Setup Chrome options
options = Options()
# Uncomment these options if you want to run the browser headlessly
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the Chrome WebDriver using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Google
driver.get("https://www.google.com")

# Allow the page to load
time.sleep(2)

# Find the search box element by ID
search_box = driver.find_element(By.ID, 'APjFqb')

# Google Dork query
google_dork = 'site:linkedin.com "current company" "JPMorgan"'

# Enter the query into the search box
search_box.send_keys(google_dork)

# Simulate pressing the Enter key
search_box.send_keys(Keys.RETURN)

# Allow the search results to load
time.sleep(3)

# (Optional) Capture screenshot of the results
driver.save_screenshot('google_dork_results.png')

# Keep the browser open for a while before closing it
time.sleep(10)

# Close the browser
driver.quit()