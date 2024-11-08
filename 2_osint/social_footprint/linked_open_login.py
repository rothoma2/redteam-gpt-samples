import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Read URLs from a file
def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

# Log in to LinkedIn
def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)  # Wait for the login page to load
    
    # Find and fill the username field
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    
    # Find and fill the password field
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    
    # Find and click the sign-in button
    sign_in_button = driver.find_element(By.XPATH, "//button[@aria-label='Sign in']")
    sign_in_button.click()
    
    time.sleep(5) 

# Open URLs in a web browser
def open_urls_in_browser(urls, username, password):
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Log in to LinkedIn
    linkedin_login(driver, username, password)
    
    for url in urls:
        driver.get(url)
        time.sleep(5)  # Wait for 5 seconds to allow the page to load
    
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py <path_to_url_file> <linkedin_username> <linkedin_password>")
        sys.exit(1)

    url_file_path = sys.argv[1]  # Get filename from command-line arguments
    linkedin_username = sys.argv[2]  # Get LinkedIn username from command-line arguments
    linkedin_password = sys.argv[3]  # Get LinkedIn password from command-line arguments
    
    urls = read_urls(url_file_path)
    open_urls_in_browser(urls, linkedin_username, linkedin_password)
