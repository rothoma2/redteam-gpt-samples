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

def setup_driver():
    options = Options()
    # Uncomment these options if you want to run the browser headlessly (not recommended for avoiding detection)
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def human_typing(element, text):
    """Types text into an element with a delay between each keystroke."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

def random_sleep(min_time, max_time):
    """Sleep for a random time between min_time and max_time seconds."""
    time.sleep(random.uniform(min_time, max_time))

def random_scroll(driver):
    """Randomly scrolls the page to mimic human behavior."""
    scroll_height = random.randint(100, 1000)
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")
    random_sleep(1, 3)

def random_mouse_movement(driver):
    """Simulates random mouse movements."""
    actions = ActionChains(driver)
    for _ in range(random.randint(1, 10)):
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        actions.move_by_offset(x_offset, y_offset)
        actions.perform()
        random_sleep(0.5, 1.5)

def extract_linkedin_links(driver):
    """Extracts LinkedIn links from the page source excluding certain patterns."""
    page_source = driver.page_source
    all_links = re.findall(r'href="(https://[^\s"]*linkedin\.com/in/[^\s"]*)"', page_source)
    linkedin_links = [
        link for link in all_links 
        if not link.startswith("https://translate.google.com/translate?") 
        and not link.startswith("https://accounts.google.com")
        and not link.startswith("https://maps.google.com")      
    ]
    for link in linkedin_links:
        print(link)
    return linkedin_links

def search_google(driver, query):
    """Performs a Google search for the given query."""
    driver.get("https://www.google.com")
    random_sleep(2, 4)
    search_box = driver.find_element(By.NAME, 'q')
    human_typing(search_box, query)
    search_box.send_keys(Keys.RETURN)
    random_sleep(3, 5)

def navigate_and_extract_links(driver, max_pages=10):
    """Navigates through Google search result pages and extracts LinkedIn links."""
    all_links = extract_linkedin_links(driver)
    for page in range(2, max_pages + 1):
        try:
            random_scroll(driver)
            next_button = driver.find_element(By.ID, 'pnnext')
            ActionChains(driver).move_to_element(next_button).click().perform()
            random_sleep(3, 5)
            all_links.extend(extract_linkedin_links(driver))
            save_links_to_file(all_links)
        except Exception as e:
            print(f"Failed to go to page {page}: {e}")
            break
    return all_links

def save_links_to_file(links, filename='linkedin_links.txt'):
    """Saves extracted links to a file."""
    with open(filename, 'w') as file:
        for link in links:
            file.write(link + '\n')

def main():
    driver = setup_driver()
    google_dork = 'site:linkedin.com/in/ AND "JPMorgan"'
    search_google(driver, google_dork)
    all_links = navigate_and_extract_links(driver)
    save_links_to_file(all_links)
    driver.quit()

if __name__ == "__main__":
    main()
