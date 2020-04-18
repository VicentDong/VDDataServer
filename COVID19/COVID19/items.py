# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Covid19Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = table = 'covid19'
    name = scrapy.Field()
    parent = scrapy.Field()
    position = scrapy.Field()
    new = scrapy.Field()
    now = scrapy.Field()
    total = scrapy.Field()
    cure = scrapy.Field()
    death = scrapy.Field()