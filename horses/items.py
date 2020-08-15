# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HorsesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    base_info = scrapy.Field()
    result_columns = scrapy.Field()
    race_result = scrapy.Field()

