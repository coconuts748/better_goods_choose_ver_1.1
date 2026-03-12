# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BetterGoodsChoosePipeline:
    def process_item(self, item, spider):
        item  = dict(item)
        with open('goods_messages.txt', 'a',encoding='utf-8') as f:
            f.write(str(item) + '\n' + '\n')

        return item
