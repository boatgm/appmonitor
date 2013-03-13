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
from crawler.items import *
from crawler.urls import contenturls
from crawler.spiders import itunes,zhushou,waptw,anzhi,hiapk,google,nduoa,appchina

class Spider(CrawlSpider):
    name = 'marketcontent'
    start_urls =[
            #'https://itunes.apple.com/cn/app/id553749400',
            #'http://zhushou.360.cn/detail/index/soft_id/199152',
            'http://www.baidu.com/',
            #'http://www.waptw.com/soft/33627.html',
            ]
    #start_urls = []
    is_start = True

    def parse(self,response):
        items = []
        if re.match(ur".*itunes\.apple\.com.*",response.url):
            items+=itunes.parse_content_links(response)
            items+=itunes.parse_content(response)
        if re.match(ur".*zhushou\.360\.cn.*",response.url):
            items+=zhushou.parse_content_links(response)
            items+=zhushou.parse_content(response)
        elif re.match(ur".*waptw\.com.*",response.url):
            items+=waptw.parse_content_links(response)
            items+=waptw.parse_content(response)
        #elif re.match(ur".*anzhi\.com.*",response.url):
        #    items+=anzhi.parse_content_links(response)
        #    items+=anzhi.parse_content(response)
        elif re.match(ur".*google\.com.*",response.url):
            items+=google.parse_content_links(response)
            items+=google.parse_content(response)
        elif re.match(ur".*nduoa\.com.*",response.url):
            items+=nduoa.parse_content_links(response)
            items+=nduoa.parse_content(response)
        #elif re.match(ur".*hiapk\.com.*",response.url):
        #    items+=hiapk.parse_content_links(response)
        #    items+=hiapk.parse_content(response)
        #elif re.match(ur".*appchina\.com.*",response.url):
        #    items+=appchina.parse_content_links(response)
        #    items+=appchina.parse_content(response)

        if self.is_start :
            self.is_start = False
            for url in contenturls():
                yield Request(url,callback=self.parse)
        for item in items:
            yield self.return_item(item)

    def return_item(self,item):
        return item

