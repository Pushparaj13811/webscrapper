import json
import csv
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from fake_useragent import UserAgent
import urllib.parse
from webdriver_manager.chrome import ChromeDriverManager

class WebScraper:
    def __init__(self):
        """Initialize the WebScraper with necessary attributes."""
        self.user_agent = UserAgent()
        self.options = webdriver.ChromeOptions()
        self.driver = None
        self.initialize_driver()

    def initialize_driver(self):
        """Initialize or reinitialize the Chrome WebDriver."""
        if self.driver:
            self.driver.quit()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.options
        )

    def set_user_agent_and_proxy(self):
        """Set a random user agent and reinitialize the driver."""
        self.options.add_argument(f"user-agent={self.user_agent.random}")
        self.initialize_driver()

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present on the page."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"Element with {by} = {value} not found within {timeout} seconds.")

    def get_element_safely(self, element):
        """Safely get element properties with retry mechanism for stale elements."""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                return {
                    "tag_name": element.tag_name,
                    "text": element.text,
                    "attributes": {
                        attr["name"]: attr["value"]
                        for attr in element.get_property("attributes")
                    } if element.get_property("attributes") else {}
                }
            except StaleElementReferenceException:
                print(f"Stale element encountered, retry {retry_count + 1}/{max_retries}")
                retry_count += 1
                time.sleep(1) 
                if retry_count == max_retries:
                    return {
                        "tag_name": "unknown",
                        "text": "",
                        "attributes": {}
                    }
            except Exception as e:
                print(f"Error processing element: {str(e)}")
                return {
                    "tag_name": "error",
                    "text": str(e),
                    "attributes": {}
                }

    def scrape_page(self, url):
        """Scrape all elements from a given URL with improved error handling."""
        try:
            self.set_user_agent_and_proxy()
            self.driver.get(url)
            
            self.wait_for_element(By.TAG_NAME, "body")
            time.sleep(5)
            
            max_retries = 3
            retry_count = 0
            page_data = []
            
            while retry_count < max_retries:
                try:
                    elements = self.driver.find_elements(By.XPATH, "//*")
                    
                    for element in elements:
                        element_data = self.get_element_safely(element)
                        if element_data:
                            page_data.append(element_data)
                    
                    break
                except Exception as e:
                    print(f"Error during scraping, retry {retry_count + 1}/{max_retries}: {str(e)}")
                    retry_count += 1
                    time.sleep(2)
            time.sleep(random.randint(5, 15))
            return page_data
            
        except Exception as e:
            print(f"Error scraping page {url}: {str(e)}")
            return []

    def save_data(self, data, page_name, website_name):
        """Save scraped data to JSON file."""
        try:
            os.makedirs("data", exist_ok=True)
            website_folder = os.path.join("data", website_name)
            os.makedirs(website_folder, exist_ok=True)
            page_folder = os.path.join(website_folder, page_name)
            os.makedirs(page_folder, exist_ok=True)
            
            json_filename = os.path.join(page_folder, f"{page_name}.json")
            
            with open(json_filename, "w", encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
            
            print(f"Data saved for page '{page_name}' inside {json_filename}")
        except Exception as e:
            print(f"Error saving data: {str(e)}")

    def compile_master_file(self, page_names, website_name):
        """Compile all page data into a master JSON file."""
        try:
            all_data = []
            website_folder = os.path.join("data", website_name)
            file_name = os.path.join(website_folder, f"{website_name}_all_data.json")
            
            for page_name in page_names:
                try:
                    page_folder = os.path.join(website_folder, page_name)
                    json_filename = os.path.join(page_folder, f"{page_name}.json")
                    
                    with open(json_filename, "r", encoding='utf-8') as json_file:
                        page_data = json.load(json_file)
                        all_data.append({"page_name": page_name, "data": page_data})
                except Exception as e:
                    print(f"Error processing page {page_name}: {str(e)}")
                    
            with open(file_name, "w", encoding='utf-8') as master_json:
                json.dump(all_data, master_json, indent=4, ensure_ascii=False)
            
            print(f"Master JSON file created as '{file_name}'")
        except Exception as e:
            print(f"Error compiling master file: {str(e)}")

    @staticmethod
    def read_urls_from_csv(file_name):
        """Read URLs from a CSV file."""
        try:
            urls = []
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row and row[0].strip():
                        urls.append(row[0].strip())
            return urls
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return []

    def process_urls(self, urls):
        """Process multiple URLs and create master file."""
        if not urls:
            print("No valid URLs found to process")
            return
            
        page_names = []
        website_name = urllib.parse.urlparse(urls[0]).netloc.split('.')[0]
        if website_name.startswith("www"):
            website_name = urllib.parse.urlparse(urls[0]).netloc.split('.')[1]
        
        for url in urls:
            try:
                page_name = url.split("/")[-1] or website_name + "_Homepage"
                page_name = page_name.replace(" ", "_").replace("-", "_")
                
                print(f"Processing URL: {url}")
                page_data = self.scrape_page(url)
                
                if page_data:
                    self.save_data(page_data, page_name, website_name)
                    page_names.append(page_name)
                else:
                    print(f"No data retrieved for {url}")
                    
            except Exception as e:
                print(f"Error processing URL {url}: {str(e)}")
        
        if page_names:
            self.compile_master_file(page_names, website_name)
        else:
            print("No pages were successfully scraped")

    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()

def main():
    """Main function to run the scraper."""
    scraper = WebScraper()
    try:
        csv_file = input("Enter the relative location of the CSV file: ")
        urls = scraper.read_urls_from_csv(csv_file)
        if urls:
            scraper.process_urls(urls)
        else:
            print("No URLs found in the CSV file")
    except Exception as e:
        print(f"An error occurred in main: {str(e)}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()