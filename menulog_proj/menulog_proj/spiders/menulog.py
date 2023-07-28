import scrapy
from scrapy.cmdline import execute
import pymysql
import menulog_proj.db_config as db
from menulog_proj.items import MenulogProjItem


class MenulogSpider(scrapy.Spider):
    name = "menulog"
    allowed_domains = ["menulog.com.au"]
    start_urls = ["https://www.menulog.com.au/takeaway"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.menulog.com.au/takeaway"
        )
        self.con = pymysql.connect(
            host=db.host,
            user=db.user,
            passwd=db.password,
            db=db.database
        )
        self.cur = self.con.cursor()

    def parse(self, response, **kwargs):
        self.loc=response.xpath('//div//li[@class="link-item"]//a/text()').getall()
        for self.index,i in enumerate(response.xpath('//li[@class="link-item"]//a/@href').getall()):
            if i[0] == '/':
                j = 'https://www.menulog.com.au' + i
                yield scrapy.Request(url=j,callback=self.newpage)
            else:
                item = MenulogProjItem()
                item['link'] = i
                item['loc']= self.loc[self.index]
                yield item


    def newpage(self,response):
        for data_list in response.xpath('//div[@class="group-links-wrapper"]//li//a/@href').getall():
          item = MenulogProjItem()
          item['link'] = data_list
          item['loc']= self.loc[self.index]
          yield item



if __name__ == '__main__':
    execute('scrapy crawl menulog'.split())
