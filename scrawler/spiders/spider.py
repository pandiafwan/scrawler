import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse
from scrapy.conf import settings
import tldextract
import pymongo

class MySpider(CrawlSpider):
    name = 'spider'

    rules = (
        Rule(LinkExtractor(), callback='parse_item'),
    )

    def __init__(self, url=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        extracted = tldextract.extract(url)
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]


    def parse_item(self, response):
        extracted = tldextract.extract(self.start_urls[0])
        domain_start = "{}.{}".format(extracted.domain, extracted.suffix)
        extracted = tldextract.extract(response.url)
        domain_response = "{}.{}".format(extracted.domain, extracted.suffix)
        if domain_response == domain_start:
            check_dedup = self.collection.find({"url" : response.url}).count()
            if check_dedup == 0:
                self.collection.insert({"url" : response.url})