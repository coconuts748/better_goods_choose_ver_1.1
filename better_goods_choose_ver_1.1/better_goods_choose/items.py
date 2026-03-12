# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BetterGoodsChooseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    details = scrapy.Field()
    price = scrapy.Field()
    href = scrapy.Field()


if __name__ == '__main__':
    item = BetterGoodsChooseItem()
    item['name'] = '<NAME>'
    item['price'] = 100
    item['href'] = 'https://www.bettergoods.com/'
    print(item)
