# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewItem(scrapy.Item):
    # define the fields for your item here like:
    store_name = scrapy.Field()
    text = scrapy.Field(),
    address = scrapy.Field(),
    phone_no = scrapy.Field(),
    opening_hour = scrapy.Field(),
    direction = scrapy.Field()