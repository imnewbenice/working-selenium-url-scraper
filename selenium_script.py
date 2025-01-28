from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import hashlib
import json
import time

# Paths to ChromeDriver and Chrome binary
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
CHROME_BINARY_PATH = "/usr/bin/google-chrome"

# Configure Selenium
options = Options()
options.binary_location = CHROME_BINARY_PATH
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Function to calculate content hash
def calculate_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

# Function to scrape a single URL
def scrape_url(url):
    driver.get(url)
    time.sleep(2)  # Allow time for the page to load

    try:
        # Extract title (h1) and content (p)
        title = driver.find_element(By.TAG_NAME, 'h1').text
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        content = "\n".join([p.text for p in paragraphs if p.text.strip()])

        # Calculate hash of the content
        content_hash = calculate_hash(content)

        return {
            "url": url,
            "title": title,
            "content": content,
            "hash": content_hash
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Function to process a chapter
def process_chapter(chapter_name, urls):
    results = []
    for url in urls:
        print(f"Scraping URL: {url}")
        data = scrape_url(url)
        if data:
            results.append(data)

    # Save results to a JSON file named after the chapter
    output_file = f"{chapter_name}_hashed.json"
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)
    print(f"Chapter {chapter_name} scraping complete. Data saved to {output_file}.")

# Load chapter URLs from JSON file
with open('chapters.json', 'r') as file:
    chapters = json.load(file)

# Process each chapter
for chapter_name, urls in chapters.items():
    print(f"Processing {chapter_name} with {len(urls)} URLs...")
    process_chapter(chapter_name, urls)

driver.quit()
