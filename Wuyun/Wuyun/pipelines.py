# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from pymongo import *
from scrapy.conf import settings

class WuyunPipeline(object):

    def __init__(self):
        #self.client = MongoClient("mongodb://wuyun:wuyun@localhost:27017/Wuyun")        
        self.client = MongoClient("mongodb://%s:%s@%s:%s/%s"%(
                                settings["MONGODB_USERNAME"], 
                                settings["MONGODB_PASSWORD"],
                                settings["MONGODB_HOST"],
                                settings["MONGODB_PORT"],
                                settings["MONGODB_DBNAME"]
                            )
                        )        
        #self.client = pymongo.MongoClient(host=settings["MONGODB_HOST"], port=settings["MONGODB_port"])
        #self.client.admin.authenticate(settings["MONGDB_USERNAME"], settings["MONGDB_PASSWORD"])
        
        #Pey attention to below, use self.client[dbName] instead of self.client.wuyun
        self.mydb = self.client[settings["MONGODB_DBNAME"]]

        self.post = self.mydb[settings["MONGODB_SHEETNAME"]]

    def process_item(self, item, spider):
        text = dict(item) 
        
        print("*"*50)
        
        print(text)
        print("*"*50)
        self.post.insert(text)
       
        return item

