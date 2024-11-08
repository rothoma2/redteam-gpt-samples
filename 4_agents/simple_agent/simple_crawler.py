from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlparse
import chromedriver_autoinstaller
import time

# Install the correct version of ChromeDriver
chromedriver_autoinstaller.install()

# Set to avoid revisiting the same links
visited_links = set()

def is_internal_link(base_url, link):
    """
    Check if the link is internal to the base_url domain.
    """
    base_domain = urlparse(base_url).netloc
    link_domain = urlparse(link).netloc
    return base_domain == link_domain or link.startswith('/')

def crawl_links(url, depth=2):
    """
    Crawls links recursively from the given URL up to the specified depth.

    :param url: URL to start crawling from.
    :param depth: Depth level to control recursion.
    """
    if url in visited_links or depth == 0:
        return
    visited_links.add(url)

    # Set up headless Chrome options
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Start the browser
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(2)  # Allow time for JavaScript to execute

        # Extract all anchor tags and find href attributes
        links = [urljoin(url, link.get_attribute("href")) for link in driver.find_elements(By.TAG_NAME, "a")]
        
        # Filter only internal links to stay within the target site
        internal_links = [link for link in links if is_internal_link(url, link)]

        print(f"Crawling: {url}")
        for link in internal_links:
            if link not in visited_links:
                time.sleep(1)  # Delay to prevent overloading the server
                crawl_links(link, depth - 1)  # Recursively crawl the link

    except Exception as e:
        print(f"Failed to crawl {url}: {e}")
    finally:
        driver.quit()  # Ensure the browser is closed

# Starting URL (change this to your VulnVM URL)
start_url = "http://192.168.2.155:3000"
crawl_links(start_url, depth=2)
