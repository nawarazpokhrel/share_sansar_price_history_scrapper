# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class ShareSansarItem(scrapy.Item):
    s_no = scrapy.Field()
    symbol = scrapy.Field()
    confidence = scrapy.Field()
    open_price = scrapy.Field()
    high_price = scrapy.Field()
    low_price = scrapy.Field()
    close_price = scrapy.Field()
    vwap = scrapy.Field()
    volume = scrapy.Field()
    prev_close = scrapy.Field()
    turnover = scrapy.Field()
    transactions = scrapy.Field()
    diff = scrapy.Field()
    diff_percentage = scrapy.Field()
    date = scrapy.Field()




class ShareSansarIndexItem(scrapy.Item):
    index_name = scrapy.Field()
    current_value = scrapy.Field()
    point_change = scrapy.Field()
    percent_change = scrapy.Field()
    turnover = scrapy.Field()
    date = scrapy.Field()

