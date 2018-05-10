# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    link = scrapy.Field()
    job_name = scrapy.Field()
    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    job_require = scrapy.Field()
    address = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    company_name = scrapy.Field()
    company_size = scrapy.Field()
    job_require_keyword = scrapy.Field()
    job_require_skill = scrapy.Field()
    pass
