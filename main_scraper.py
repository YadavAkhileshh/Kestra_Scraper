import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import logging
import os
from fake_useragent import UserAgent
from retry import retry

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, urls=None):
        self.ua = UserAgent()
        env_urls = os.getenv('SCRAPER_URLS')
        if env_urls:
            self.urls = [url.strip() for url in env_urls.split(',')]
        else:
            self.urls = [urls] if isinstance(urls, str) else urls or ["https://quotes.toscrape.com/"]
        
        self.output_dir = '/tmp/scraper/output'
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.stats = {
            'start_time': datetime.now(),
            'end_time': None,
            'total_items': 0,
            'successful': 0,
            'failed': 0,
            'urls_processed': 0
        }

    @retry(tries=3, delay=2)
    def fetch_page(self, url):
        """Fetch page with retry logic and rotating user agents"""
        logger.info(f"Fetching URL: {url}")
        headers = {'User-Agent': self.ua.random}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            self.stats['failed'] += 1
            raise

    def process_content(self, html, url):
        """Process HTML content and extract data"""
        soup = BeautifulSoup(html, 'html.parser')
        items = []

        for quote in soup.find_all('div', class_='quote'):
            try:
                text = quote.find('span', class_='text').get_text()
                author = quote.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]

                items.append({
                    'url': url,
                    'content': text,
                    'author': author,
                    'tags': tags,
                    'scrape_time': datetime.now().isoformat()
                })
                self.stats['successful'] += 1
                
            except Exception as e:
                logger.error(f"Error processing item: {str(e)}")
                self.stats['failed'] += 1

        return items

    def run(self):
        """Main execution method"""
        logger.info("Starting web scraping process...")
        all_items = []
        
        for url in self.urls:
            try:
                html = self.fetch_page(url)
                items = self.process_content(html, url)
                all_items.extend(items)
                self.stats['urls_processed'] += 1
                self.stats['total_items'] += len(items)
                
            except Exception as e:
                logger.error(f"Error processing URL {url}: {str(e)}")
                continue

        self.stats['end_time'] = datetime.now()
        
        data_file = os.path.join(self.output_dir, 'scraped_data.json')
        stats_file = os.path.join(self.output_dir, 'scraping_stats.json')
 
        with open(data_file, 'w') as f:
            json.dump(all_items, f, indent=2)
        logger.info(f"Saved scraped data to: {data_file}")
            
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, default=str, indent=2)
        logger.info(f"Saved stats to: {stats_file}")
        
        return data_file

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.run()