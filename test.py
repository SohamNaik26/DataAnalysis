from scrapy import Spider

import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://example.com']

    def parse(self, response):
        # Your parsing logic here
        pass
