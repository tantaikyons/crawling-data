
from domain.crawl import ICrawlUrl,ICrawlResult

class CrawlUrl:
    def __init__(self, url, body, title):
        self.url = url
        self.body = body
        self.title = title

    def to_json(self):
        return {"url": self.url, "body": self.body, "title": self.title}

class CrawlResult:
    def __init__(self, urls:list[CrawlUrl],total):
        self.urls = urls
        self.total = total
        
    def to_json(self):
        return {"urls": [url.to_json() for url in self.urls], "total": self.total}