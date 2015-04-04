# -*- coding: utf-8 -*-
import scrapy

class HetznerItem(scrapy.Item):
    id = scrapy.Field()
    cpu = scrapy.Field()
    cpu_b = scrapy.Field()
    ram = scrapy.Field()
    hdd = scrapy.Field()
    price = scrapy.Field()
    reduction = scrapy.Field()
