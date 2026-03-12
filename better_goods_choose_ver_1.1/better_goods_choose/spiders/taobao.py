import scrapy

taobao_net = {}

class TaobaoSpider(scrapy.Spider):
    name = "taobao"
    allowed_domains = ["www.taobao.com"]
    start_urls = ["https://www.taobao.com"]

    def parse(self, response):
        pass
