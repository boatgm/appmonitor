#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import urlparse
from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy.http import Request
from crawler.items import ApkItem,MetaItem,CommentItem,LinkItem
from crawler.urls import updateurls
from crawler.spiders import itunes,zhushou,waptw,anzhi,hiapk,google

class Spider(CrawlSpider):
    name = 'marketupdate'
    start_urls =[
            'http://www.baidu.com/',
            ]
    is_start = True
    def parse(self,response):
        items = []
        if re.match(ur".*itunes\.apple\.com.*",response.url):
            items += itunes.parse_update(response)
        if re.match(ur".*zhushou\.360\.cn.*",response.url):
            items += zhushou.parse_update(response)
        elif re.match(ur".*waptw\.com.*",response.url):
            items += waptw.parse_update(response)
        elif re.match(ur".*google\.com.*",response.url):
            items += google.parse_update(response)
        
        if self.is_start :
            self.is_start = False
            for url in updateurls():
                yield Request(url,callback=self.parse)
        for item in items:
            yield self.return_item(item)

    def return_item(self,item):
        return item

