# Required libraries for scraping, file handling and URL parsing
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse
from pathlib import Path

# Define a Spider class for scraping HTML content
class HtmlScraperSpider(scrapy.Spider):
    # Name of the spider
    name = 'html_scraper'

    # Initialization method
    def __init__(self, body_tag=None, *args, **kwargs):
        super(HtmlScraperSpider, self).__init__(*args, **kwargs)
        # Set start URLs and failed URLs lists
        self.start_urls = self.get_start_urls()
        self.failed_urls = []
        self.body_tag = body_tag

    # Method to get the start URLs from a file
    def get_start_urls(self):
        url_file_path = '/workspaces/explorebot/explorebot/myproject/urls.txt'
        try:
            with open(url_file_path, 'r') as f:
                urls = f.read().split('\n')
            if not urls:
                print("The URL file is empty.")
                return []
            return urls
        except FileNotFoundError:
            print("The URL file is not found.")
            return []

    # Method to start making requests to the URLs
    def start_requests(self):
        for url in self.start_urls:
            try:
                result = urlparse(url)
                if all([result.scheme, result.netloc]):
                    self.log(f'Starting to scrape: {url}')
                    yield scrapy.Request(url)
                else:
                    self.failed_urls.append(url)
                    self.log(f'Invalid URL format: {url}')
            except Exception as e:
                self.failed_urls.append(url)
                self.log(f'Error making request to {url}: {e}')

    # Method to parse the response from the scraped website
    def parse(self, response):
        try:
            self.log(f'Response received - Status: {response.status}, URL: {response.url}')
            filename = response.url.split('/')[-1]
            filepath = Path('html_downloads') / f'{filename}.html'
            
            if self.body_tag:
                content = response.css(self.body_tag).get()
            else:
                content = response.body
                
            if content:
                os.makedirs('html_downloads', exist_ok=True)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content.decode('utf-8'))
        except Exception as e:
            self.failed_urls.append(response.url)
            self.log(f'Error processing response from {response.url}: {e}')

    # Method executed when spider closes
    def closed(self, reason):
        if self.failed_urls:
            print("List of unsuccessfully scraped URLs:")
            print('\n'.join(self.failed_urls))

# Instantiate the Spider
spider = HtmlScraperSpider()

# Check if there are any start URLs and then start the crawl process
if spider.start_urls:
    process = CrawlerProcess()
    process.crawl(HtmlScraperSpider)
    process.start()
else:
    print("The initial URL file is empty.")
