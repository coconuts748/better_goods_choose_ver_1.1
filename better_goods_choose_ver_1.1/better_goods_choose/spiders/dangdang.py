import json

import scrapy
from loguru import logger
from bs4 import BeautifulSoup
from better_goods_choose.items import BetterGoodsChooseItem


class DangdangSpider(scrapy.Spider):
    name = "dangdang"
    allowed_domains = ["www.dangdang.com"]
    start_urls = ["https://www.dangdang.com"]

    def start_requests(self):
        with open(r'E:\python_projects\better_goods_choose\better_goods_choose\spiders\search_history.json','r') as read:
            data = json.load(read)
            get_real_url = data['dang_dang_net']
            yield scrapy.Request(
                url=get_real_url,
                callback=self.parse,
                dont_filter=True)

    def parse(self, response):
        logger.error(response.url)
        soup = BeautifulSoup(response.body, 'lxml')
        # logger.debug(soup.prettify())

        try:
            # logger.debug(soup.prettify())
            goods_areas = soup.find('div',id='search_nature_rg')
            logger.info(goods_areas)
            inner_goods_areas = goods_areas.find('ul')
            inner_goods_areas = inner_goods_areas.find_all('li')
            # logger.debug(len(inner_goods_areas))
            if len(inner_goods_areas) > 0:
                for i in inner_goods_areas:
                    logger.debug(i)
                    limited_items = BetterGoodsChooseItem()
                    goods_name = i.find('p',class_='name').text
                    good_detail = i.find('p',class_='detail').text
                    goods_price = i.find('p',class_='price').text
                    goods_href = i.find('a')['href']
                    limited_items['name'] = goods_name
                    limited_items['details'] = good_detail
                    limited_items['price'] = goods_price
                    limited_items['href'] = f"https:{goods_href}"
                    # logger.debug(limited_items)
                    yield limited_items
        #
        except Exception as a:
            logger.debug(a)