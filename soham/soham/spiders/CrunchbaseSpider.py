import scrapy


class CrunchbasespiderSpider(scrapy.Spider):
    name = "CrunchbaseSpider"
    allowed_domains = ["domain.com"]
    start_urls = ["https://domain.com"]

    def parse(self, response):
        pass
