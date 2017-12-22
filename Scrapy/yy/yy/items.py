# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()

    #imageURL
    thumb2 = scrapy.Field()

    #stroeURL path
    #imagePath = scrapy.Field()

