# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BollywoodMovieItem(scrapy.Item):
    item_type = scrapy.Field()
    url = scrapy.Field()
    movie_name = scrapy.Field()
    directed_by = scrapy.Field()
    produced_by = scrapy.Field()
    written_by = scrapy.Field()
    release_date = scrapy.Field()
    casts = scrapy.Field()

class BollywoodPersonItem(scrapy.Item):
    item_type = scrapy.Field()
    url = scrapy.Field()
    actor_name = scrapy.Field()
    gender = scrapy.Field()
    birth_date = scrapy.Field()
    birth_place = scrapy.Field()
    nationality = scrapy.Field()
    occupation = scrapy.Field()
    
