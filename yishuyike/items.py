# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YishuyikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content_title = scrapy.Field()
    videoDuration = scrapy.Field()  # video id
    videoUrl = scrapy.Field()  # video url 参数
    author = scrapy.Field()  # 书作者
    contentId = scrapy.Field()  # 书 id
    userInfoVersion = scrapy.Field()  # 使用人版本id
