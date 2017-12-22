# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import scrapy
import os

from scrapy.utils.project import get_project_settings as gps
from scrapy.pipelines.images import ImagesPipeline

class YyImagesPipeline(ImagesPipeline):
    
#    def process_item(self, item, spider):
#        fileName = item["name"]
#        image = json.dumps(dict(item), ensure_ascii=False)
#        self.writeImage(text, fileName)
#        return item
#
#    def writeImage(self, text, fileName):
#        filePath = "./images/" + fileName + ".jpg"
#
#        with open(filePath, "wb") as f:
#            f.write(text)
    
    IMAGES_STORE = gps().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        imgURL = item["thumb2"]

        yield scrapy.Request(imgURL)
    
    
    def item_completed(self, results, item, info):
    
        
        h = [x for ok, x in results if ok]
        
        print("*"*60)
        print(h)
        print("*"*60)
        
        imgPath = [x["path"] for ok, x in results if ok]
        print("*"*60)
        print(imgPath)
        print("*"*60)
        
        os.rename(self.IMAGES_STORE + "/" + imgPath[0], self.IMAGES_STORE + "/" + item["name"] + ".jpg")

        
