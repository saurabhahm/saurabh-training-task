# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MenulogProjItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    loc=scrapy.Field()

class Menulog1ProjItem(scrapy.Item):
    p_link=scrapy.Field()
    id=scrapy.Field()
    location=scrapy.Field()
class Menulog_productProjItem(scrapy.Item):
    id=scrapy.Field()
    Min_Order =scrapy.Field()
    Delivery_fee =scrapy.Field()
    Full_Address =scrapy.Field()
    About_us =scrapy.Field()
    Delivery_hours =scrapy.Field()
    Offers  =scrapy.Field()
    latitude   =scrapy.Field()
    longitude  =scrapy.Field()
    Stampcard =scrapy.Field()
    Phone  =scrapy.Field()
    postalCode =scrapy.Field()
    addressLocality =scrapy.Field()
    street_Address=scrapy.Field()
    Delivery_time=scrapy.Field()
    URL =scrapy.Field()
    Location  =scrapy.Field()
    City =scrapy.Field()
    Name=scrapy.Field()
    Cusines=scrapy.Field()
    Rating=scrapy.Field()
    Review=scrapy.Field()


