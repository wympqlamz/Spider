# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ChinaNewsPipeline(object):
    def __init__(self):
        self.fileContent = open("temp1.json", "w")

    def process_item(self, item, spider):
        jsonText = json.dumps(dict(item), ensure_ascii = False) + "\n"*2
        self.fileContent.write(jsonText)

        return item

    def close_spider(self, spider):
        self.fileContent.close()
