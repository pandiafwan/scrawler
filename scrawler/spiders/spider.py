import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse
import tldextract

class MySpider(CrawlSpider):
    name = 'spider'

    rules = (
        Rule(LinkExtractor(), callback='parse_item'),
    )

    def __init__(self, url=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        extracted = tldextract.extract(url)

    def parse_item(self, response):
        extracted = tldextract.extract(self.start_urls[0])
        domain_start = "{}.{}".format(extracted.domain, extracted.suffix)
        extracted = tldextract.extract(response.url)
        domain_response = "{}.{}".format(extracted.domain, extracted.suffix)
        if domain_response == domain_start:
            file = open("crawldb/urls.list","a")
            file.write(response.url+"\n")
            file.close()