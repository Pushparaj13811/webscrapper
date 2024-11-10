# Web Scraper

A robust and flexible web scraping tool built with Python and Selenium that handles multiple URLs, manages data storage, and includes features like random user agent rotation and error handling. some

## Features

- **Automated Web Scraping**: Scrapes web pages using Selenium WebDriver
- **User Agent Rotation**: Implements random user agent rotation to avoid detection
- **Robust Error Handling**: Contains comprehensive error handling and retry mechanisms
- **Flexible Data Storage**: Organizes scraped data in a structured JSON format
- **Batch Processing**: Processes multiple URLs from a CSV file
- **Master File Compilation**: Creates consolidated data files for easy analysis

## Prerequisites

Before running the scraper, make sure you have the following installed:

- Python 3.x
- Chrome browser
- ChromeDriver (automatically managed by webdriver_manager)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/pushparaj13811/webscrapper.git
cd webscrapper
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Required Python Packages

- selenium
- webdriver_manager
- fake-useragent
- urllib3

## Usage

1. Create a CSV file containing the URLs you want to scrape (one URL per line)

2. Run the script:

```bash
python dataScraper.py
```

3. When prompted, enter the relative path to your CSV file

The scraper will:

- Process each URL in the CSV file
- Create a structured directory for data storage
- Save individual JSON files for each page
- Compile a master JSON file with all scraped data

## Data Storage Structure

```
data/
└── website_name/
    ├── website_name_all_data.json
    └── page_name/
        └── page_name.json
```

## Key Components

- `WebScraper`: Main class that handles the scraping operations
- `initialize_driver()`: Sets up the Chrome WebDriver
- `set_user_agent_and_proxy()`: Rotates user agents
- `scrape_page()`: Extracts data from individual pages
- `save_data()`: Manages data storage
- `compile_master_file()`: Creates consolidated data files

## Error Handling

The scraper includes comprehensive error handling for:

- Stale elements
- Timeout exceptions
- Network issues
- File operations
- Invalid URLs

## Best Practices

1. Add appropriate delays between requests (already implemented)
2. Respect robots.txt
3. Implement rate limiting if necessary
4. Verify site's terms of service before scraping

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Be sure to check and comply with the target website's robots.txt file and terms of service before scraping any data.
