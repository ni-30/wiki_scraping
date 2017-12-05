# -*- coding: utf-8 -*-

# Scrapy settings for my_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wiki_scrapy'

SPIDER_MODULES = ['wiki_scrapy.spiders']
NEWSPIDER_MODULE = 'wiki_scrapy.spiders'

ROBOTSTXT_OBEY = True