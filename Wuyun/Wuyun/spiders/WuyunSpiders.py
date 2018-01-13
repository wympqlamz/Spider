from Wuyun.items import WuyunItem
import scrapy

class WuyunSpider(scrapy.Spider):
    
    name = "wuyun"
    allowed_domians = ["anquan.us"]
    
    offSet = 1
    url = "http://www.anquan.us/search?keywords=&&page="
    start_urls = [url + str(offSet)]
    
    subURL = "http://www.anquan.us/"

    def parse(self, response):
        for each in response.xpath("//div[@class='col-md-10']//tr/td[2]/a/@href").extract():
            fullURL = self.subURL + each
            yield scrapy.Request(fullURL, callback=self.parseItem)

        if self.offSet < 2015:
            self.offSet += 1
            yield scrapy.Request(self.url + str(self.offSet), callback=self.parse)
    

    def parseItem(self, response):
        
        item = WuyunItem()
        item["title"] = response.xpath(r"//div[@class='content']/h3[@class='wybug_title']/text()").extract()[0].split("：")[-1].strip("\n\t\r").strip()

        item["factory"] = response.xpath(r"//div[@class='content']/h3[@class='wybug_corp']/a/text()").extract()[0].strip("\n\t").strip()

        item["issueTime"] = response.xpath(r"//div[@class='content']/h3[@class='wybug_date']/text()").extract()[0].split("：")[-1].strip()

        item["severity"] = response.xpath(r"//div[@class='content']/h3[@class='wybug_level']/text()").extract()[0].split("：")[-1].strip()

        yield item



