from data.crawl_model import CrawlResult # type: ignore


def toView(crawlResult: CrawlResult):
    return crawlResult.to_json()