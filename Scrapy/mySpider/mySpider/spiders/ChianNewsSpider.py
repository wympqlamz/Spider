# -*- utf-8 -*-

import scrapy
from mySpider.items import ChinaNewsItem

class ChinaNewsSpider(scrapy.Spider):

    #spider name
    name = "ChinaNewsSpider"

    #Allow scope of spider
    allowd_domains = ["http://www.chinanews.com/"]

    #True url for spider
    start_urls = ["http://channel.chinanews.com/cns/cl/gn-gcdt.shtml?pager=0"]

    def parse(self, response):

        #Title
        titles = response.xpath("//td/a/text()").extract()
        #Content
        contents = response.xpath("//td/font/text()").extract()
        #newsURL
        newsURLs = response.xpath("//tr[3]/td/text()").extract()
        
        newsItems = []
        for title, content, newsURL in zip(titles, contents, newsURLs):
            #newsList = {"Title:" : title, "Content:" : content, "newsURL:" : newsURL}
            item = ChinaNewsItem()

            item["title"] = title.strip()
            item["content"] = content.strip()
            item["newsURL"] = newsURL.strip()
            
            newsItems.append(item)

        return newsItems
