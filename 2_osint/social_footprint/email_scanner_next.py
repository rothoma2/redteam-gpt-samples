from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

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

# Google Dork query for finding JPMorgan emails
google_dork = 'intext:"@jpmorgan.com"'

# Enter the query into the search box
search_box.send_keys(google_dork)

# Simulate pressing the Enter key
search_box.send_keys(Keys.RETURN)

# Allow the search results to load
time.sleep(3)

# Function to parse emails from the search results
def parse_emails():
    emails = set()  # Using a set to avoid duplicates
    search_results = driver.find_elements(By.XPATH, '//div[@class="g"]')  # Finding all results divs
    for result in search_results:
        result_text = result.text
        found_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@jpmorgan\.com\b', result_text)
        emails.update(found_emails)
    return emails

# Gather emails from the first page
all_emails = parse_emails()

# Iterate over the next pages up to page 10
for page in range(2, 11):
    try:
        # Find and click the 'Next' button to go to the next page of results
        next_button = driver.find_element(By.ID, 'pnnext')
        next_button.click()
        # Allow the new page to load
        time.sleep(3)
        # Parse emails from the new page
        all_emails.update(parse_emails())
    except Exception as e:
        print(f"Failed to go to page {page}: {e}")
        break

# Write the found emails to a .txt file
with open('jpmorgan_emails.txt', 'w') as file:
    for email in all_emails:
        file.write(email + '\n')

# Close the browser
driver.quit()
