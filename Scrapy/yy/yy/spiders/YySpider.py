import scrapy
import json
import random
import time

from yy.items import YyItem

class YySpider(scrapy.Spider):

    name = "yy"
    def __init__(self):
        
        
        self.allowed_domains = ["yy.com"]

        self.offSet = 1

        self.url = "http://www.yy.com/more/page.action?biz=sing&subBiz=dance&moduleId=678&page="

        self.start_urls = [self.url + str(self.offSet)]
        
        self.sleepTime = [i for i in range(3,15)]

    def parse(self, response):
        item = YyItem()

        for each in json.loads( response.text)["data"]["data"]:
           
            item["name"] = each["name"]

            item["thumb2"] = each["thumb2"]
            
            time.sleep(random.choice(self.sleepTime))

            yield item
        
        if self.offSet < 5:
            self.offSet += 1

        yield scrapy.Request(self.url + str(self.offSet), callback=self.parse)

