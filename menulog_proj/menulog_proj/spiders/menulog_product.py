import scrapy
import pymysql
import re
from scrapy.cmdline import execute
import menulog_proj.db_config as db
import json
from menulog_proj.items import Menulog_productProjItem


class MenulogProductSpider(scrapy.Spider):
    name = "menulog_product"
    allowed_domains = ["menulog.com.au","aus.api.just-eat.io"]
    # start_urls = ["https://www.menulog.com.au/restaurants-dominos-burnie/menu"]

    def start_requests(self):
        self.con = pymysql.connect(
            host=db.host,
            user=db.user,
            passwd=db.password,
            db=db.database
        )
        self.cur = self.con.cursor()
        qry=f"select number ,menulog_linkcol ,location from {db.menu_link} where status = 'pending';"
        self.cur.execute(qry)
        for i in self.cur.fetchall():
            yield scrapy.Request(url=i[1], cb_kwargs={"id": i[0], "location": i[2]})

    def parse(self, response,**kwargs):
        new = response.xpath('//script[@data-vmid="structured-data-restaurant"]/text()').get('')
        newdata = json.loads(new)
        Full_Address = response.xpath('//div/p[@class="l-centered c-restaurantHeader-address"]/span/text()').get().strip()
        Delivery_hours = response.xpath('//div[@class="c-orderStatus-row"][1]/p/span/text()').get().strip()
        city = response.xpath('//div/p[@class="l-centered c-restaurantHeader-address"]/span/text()').get().split(',')[-2].strip()
        addressLocality = response.xpath('//div/p[@class="l-centered c-restaurantHeader-address"]/span/text()').get().split(',')[-2].strip()
        name = response.xpath('//div[@class="c-mediaElement-content"]/h1/text()').get().strip()
        rating = newdata['aggregateRating']['ratingValue']
        review = newdata['aggregateRating']['ratingCount']
        postalcode = newdata['address']['postalCode']
        Cusines = newdata['servesCuisine']
        cus=''
        if len(Cusines)>1:
            cus=f"{Cusines[0]} {Cusines[1]}"
        else:
            cus = f"{Cusines[0]}"

        street_Address = newdata['address']['streetAddress']

        j = response.xpath('//script[contains(text(), window.__INITIAL_STATE__)]').getall()
        data5 = re.findall(r'<script>window\.__INITIAL_STATE__=(.*?)<\/script>', j[8])
        json_data = json.loads(data5[0])

        Delivery_time = "|".join(newdata['openingHours'])
        description = json_data['state']['restaurantInfo']['description']
        phone_number = json_data['state']['restaurantInfo']['allergenPhoneNumber']
        latitude = json_data['state']['restaurantInfo']['location']['latitude']
        longitude = json_data['state']['restaurantInfo']['location']['longitude']
        l1=list()
        item=Menulog_productProjItem()

        item['URL']=response.url
        item['Location']=kwargs['location']
        item['longitude']=longitude
        item['latitude']=latitude
        item['Phone']=phone_number
        item['About_us']=description
        item['Delivery_time']=Delivery_time
        item['street_Address']=street_Address
        item['Cusines']=cus
        item['postalCode']=postalcode
        item['Review']=review
        item['Rating']=rating
        item['Name']=name
        item['addressLocality']=addressLocality
        item['City']=city
        item['Delivery_hours']=Delivery_hours
        item['Full_Address']=Full_Address
        item['id']=kwargs['id']
        l1.append(item)

        data = response.xpath('//script[@data-vmid="load-fonts"]/following-sibling::script[contains(text(),window.__INITIAL_STATE__)][1]/text()').get()
        data_json = json.loads(data[25:])
        self.restaurant_id = data_json['state']['restaurantId']

        another_link = f"https://aus.api.just-eat.io/consumeroffers/notifications/au?restaurantIds={self.restaurant_id}&optionalProperties=offerMenuItems"
        yield scrapy.Request(url=another_link, callback=self.newpage2,cb_kwargs={"data":l1})

    def newpage2(self,response, **kwargs):
        l1=kwargs["data"]
        data1=response.text
        data=json.loads(data1)
        item = Menulog_productProjItem()
        stamp=" "
        if len(data['offerNotifications']) > 1:
            if data['offerNotifications'][1]['offerType']=="StampCard":
             stamp="StampCard"
        elif len(data['offerNotifications']) == 1:
            if "StampCard"==data['offerNotifications'][0]['offerType']:
             stamp="StampCard"
        else:
            stamp=" "
        if len(data['offerNotifications'])>0:
         offer = data['offerNotifications'][0]['description']
        else:
            offer=" "
        item['Offers']=offer
        item['Stampcard'] = stamp
        if len(item['Offers'])==0:
         l1[0]['Offers']=" "
        else:
            l1[0]['Offers'] = item['Offers'][0:]

        if len(item['Stampcard'])==0:
            l1[0]['Stampcard']=[]
        else:
         l1[0]['Stampcard']=item['Stampcard'][0:]
        link = f'https://aus.api.just-eat.io/restaurant/au/{self.restaurant_id}/menu/dynamic?orderTime=2023-07-20T08:09:30.4217772%2B00:00&ratingsOutOfFive=true'
        yield scrapy.Request(url=link, callback=self.newpage,cb_kwargs={"data":l1})

    def newpage(self,response,**kwargs):
        l1 = kwargs["data"]
        data1=response.text
        data=json.loads(data1)
        l=" "
        try:
            if (data['DeliveryFees']['Bands'])!=None:

                    if len(data['DeliveryFees']['Bands']) > 1:
                        ma = (data['DeliveryFees']['Bands'][0]['Fee']) / 100
                        mi = (data['DeliveryFees']['Bands'][1]['Fee']) / 100
                        l=f"${mi}-{ma}"
                    else:
                        j= (data['DeliveryFees']['Bands'][0]['Fee']) / 100
                        l=f"${j}"
        except Exception:
            pass
        item = Menulog_productProjItem()

        item['Delivery_fee']=l
        min_order="$0"
        try:
         min_order=f"${(data['DeliveryFees']['MinimumOrderValue'])/100}"
        except Exception:
            pass
        item['Min_Order'] =min_order
        l1[0]['Delivery_fee']=item['Delivery_fee']
        l1[0]['Min_Order']=item['Min_Order']
        i=l1[0]

        yield i


if __name__ == '__main__':
    execute('scrapy crawl menulog_product'.split())

