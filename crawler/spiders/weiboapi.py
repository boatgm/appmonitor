#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import urlparse
from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy.http import Request,FormRequest
from crawler.items import *
from crawler.urls import tokens
from crawler.spiders import itunes,zhushou,waptw,anzhi,hiapk,google

class Spider(CrawlSpider):
    name = 'weiboapi'
    start_urls =[
            'http://localhost/',
            ]
    is_start = True
    def parse(self,response):
        if self.is_start :
            self.is_start = False
            for t in tokens():
                yield WeiboRequest()
                yield Request(url,callback=self.parse)

        for item in items:
            yield self.return_item(item)

    def parse_weibo_list(self,response):
        pass


    def return_item(self,item):
        return item

def WeiboRequest(token,plotform):
    if plotform is "sina":
        pass
    if plotform is "tencent":
        pass
    if plotform is "twitter":
        pass

def InfoRequest(token,plotform):
    return Request()
