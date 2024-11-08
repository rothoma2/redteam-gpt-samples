import random
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options
options = Options()
# Uncomment these options if you want to run the browser headlessly (not recommended for avoiding detection)
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Set a realistic user-agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the Chrome WebDriver using webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def human_typing(element, text):
    """Types text into an element with a delay between each keystroke."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

def random_sleep(min_time, max_time):
    """Sleep for a random time between min_time and max_time seconds."""
    time.sleep(random.uniform(min_time, max_time))

def random_scroll():
    """Randomly scrolls the page to mimic human behavior."""
    scroll_height = random.randint(100, 1000)
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
    random_sleep(1, 3)

def random_mouse_movement():
    """Simulates random mouse movements."""
    actions = ActionChains(driver)
    for _ in range(random.randint(1, 10)):
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        actions.move_by_offset(x_offset, y_offset)
        actions.perform()
        random_sleep(0.5, 1.5)

# Open Google
driver.get("https://www.google.com")

# Allow the page to load
random_sleep(2, 4)

# Find the search box element by ID
search_box = driver.find_element(By.ID, 'APjFqb')

# Google Dork query for finding JPMorgan emails
google_dork = 'intext:"@jpmorgan.com"'

# Enter the query into the search box using human_typing
human_typing(search_box, google_dork)

# Simulate pressing the Enter key
search_box.send_keys(Keys.RETURN)

# Allow the search results to load
random_sleep(3, 5)

def parse_emails():
    emails = set()  # Using a set to avoid duplicates
    search_results = driver.find_elements(By.XPATH, '//div[@class="g"]')  # Finding all results divs
    for result in search_results:
        result_text = result.text
        found_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@jpmorgan\.com\b', result_text)
        for email in found_emails:
            if email not in emails:
                print(email)  # Print the email to the console
                emails.add(email)
    return emails

# Gather emails from the first page
all_emails = parse_emails()

# Iterate over the next pages up to page 10
for page in range(2, 11):
    try:
        # Random scrolling and mouse movements to mimic human behavior
        random_scroll()
        #random_mouse_movement()

        # Find and click the 'Next' button to go to the next page of results
        next_button = driver.find_element(By.ID, 'pnnext')
        # Move to the next button and click it
        ActionChains(driver).move_to_element(next_button).click().perform()

        # Allow the new page to load
        random_sleep(3, 5)

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
