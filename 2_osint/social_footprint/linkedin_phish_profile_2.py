import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os
import openai

# OpenAI API Configuration
openai.api_key = os.getenv('OPENAI_API_KEY')

# Read URLs from a file
def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

# Log in to LinkedIn
def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    
    sign_in_button = driver.find_element(By.XPATH, "//button[@aria-label='Sign in']")
    sign_in_button.click()
    
    time.sleep(5)

def extract_visible_text(driver):
    elements = driver.find_elements(By.XPATH, "//*[not(self::script or self::style)]") # Exclude script and style tags
    
    visible_texts = []
    for element in elements:
        if element.is_displayed():
            text = element.text.strip()
            if text:
                visible_texts.append(text)
    
    return "\n".join(visible_texts)

def truncate_text_to_500_words(text):
    words = text.split()
    if len(words) > 500:
        words = words[:500]  # Truncate to 500 words
    return " ".join(words)

def generate_profile_from_text(text, model="gpt-4o"):
    try:
        prompt = (
            "Create a personal profile that could be used in a phishing simulation. "
            "The profile should contain details such as the person's job title, work history, "
            "education, and any other relevant information. Use the following information:\n\n"
            f"{text}"
        )
        truncated_text = truncate_text_to_500_words(prompt)
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert, pretending to be an adversary."},
                {"role": "user", "content": truncated_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

def generate_filename_from_url(url):
    filename = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")
    return f"{filename}.txt"

def open_urls_in_browser(urls, username, password):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    linkedin_login(driver, username, password)
    
    for url in urls:
        driver.get(url)
        time.sleep(2)
        visible_text = extract_visible_text(driver)
        
        # Generate phishing profile
        profile = generate_profile_from_text(visible_text)
        filename = generate_filename_from_url(url)
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(profile)
        
        print(f"Profile written to {filename}")
    
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_url_file> <linkedin_username> <linkedin_password>")
        sys.exit(1)

    url_file_path = sys.argv[1]
    linkedin_username = os.getenv('LINKEDIN_USERNAME')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    
    urls = read_urls(url_file_path)
    open_urls_in_browser(urls, linkedin_username, linkedin_password)
