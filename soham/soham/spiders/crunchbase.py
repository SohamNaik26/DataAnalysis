import scrapy


class CrunchbaseSpider(scrapy.Spider):
    name = "crunchbase"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
