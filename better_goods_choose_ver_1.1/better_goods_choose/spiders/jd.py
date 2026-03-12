import scrapy

jd_net = {}

class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["re.jd.com"]
    start_urls = ["https://re.jd.com"]

    def parse(self, response):
        pass
