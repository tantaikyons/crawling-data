
import requests
from ..domain.crawl import ICrawlService
from bs4 import BeautifulSoup

class CrawlService(ICrawlService):
    def __init__(self):
        print("fad")

    def crawl_website(base_url):
    # List to store all page data
        all_pages = []
        # Set to store all unique URLs
        all_urls = set()
        def crawl_page(url):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text from the page
            body_text = soup.get_text(strip=False)
            body_text = body_text.replace('\n', ' ')
            print("body_text: ", body_text)
            # Add page data to the list
            if "404 Không tìm thấy trang" not in soup.title.string:
                all_pages.append({
                    "url": url,
                    "title": soup.title.string if soup.title else "",
                    "body": body_text
                })
                # Find all links on the page
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('/') or href.startswith(base_url):
                        full_url = base_url + href if href.startswith('/') else href
                        if full_url not in all_urls:
                            all_urls.add(full_url)
                            crawl_page(full_url)

        # Start crawling from the base URL
        crawl_page(base_url)
    
        return all_pages


    


    
