# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutoRiaComItem(scrapy.Item):
    _id = scrapy.Field()
    image_urls = scrapy.Field()
    # file_urls = scrapy.Field()
    # files = scrapy.Field()
    images = scrapy.Field()
    manufacture = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
