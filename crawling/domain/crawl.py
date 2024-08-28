
from abc import abstractmethod, ABC


class ICrawlUrl:
    def __init__(self,url:str,body:str,title:str) -> None:
        self.url = url
        self.body = body
        self.title = title

class ICrawlResult:
    def __init__(self,urls:list[ICrawlUrl],total:int) -> None:
        self.urls = urls
        self.total = total
        
class ICrawlService(ABC):
    @abstractmethod
    def crawl(self,url:str) -> ICrawlResult: pass
