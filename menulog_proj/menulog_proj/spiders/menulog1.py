import scrapy
import pymysql
from scrapy.cmdline import execute
import re
import menulog_proj.db_config as db
from menulog_proj.items import Menulog1ProjItem


class Menulog1Spider(scrapy.Spider):
    name = "menulog1"
    allowed_domains = ["menulog.com.au"]
    start_urls = ["https://menulog.com.au"]


    def start_requests(self):
        self.con = pymysql.connect(
            host=db.host,
            user=db.user,
            passwd=db.password,
            db=db.database
        )
        self.cur = self.con.cursor()
        qry = f"select id, first_link,location  from {db.takeaway_link} where status = 'pending';"
        self.cur.execute(qry)

        for i in self.cur.fetchall():
            yield scrapy.Request(url=i[1],cb_kwargs={"id": i[0],'location':i[2]})

    def parse(self, response,**kwargs):
        code=response.body
        with open('text.html','wb+') as file :
            file.write(code.decode('unicode_escape').encode('UTF-8'))
        with open('text.html', 'r', encoding='UTF-8') as file:
            html_f = file.read()
        c = re.findall('\"uniqueName\"\:\"[\S]{1,}\"{1}', html_f)
        list_main = []
        for count, i in enumerate(c):
            Bc = str(i).split(",")
            dictionaty = dict()
            for j in Bc:
                k = j.split(":")
                dictionaty[k[0]] = k[1]
                list_main.append(dictionaty)
                try:
                    uniquename = re.findall('[a-zA-z\-]{1,}', dictionaty['"uniqueName"'])[0]
                    link=f'https://www.menulog.com.au/restaurants-{uniquename}/menu'
                    item=Menulog1ProjItem()
                    item['p_link']=link
                    item['id'] = kwargs["id"]
                    item['location']=kwargs['location']
                    yield item
                except:
                    continue


if __name__ == '__main__':
    execute('scrapy crawl menulog1'.split())
