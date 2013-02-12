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
            #'https://itunes.apple.com/cn/app/id553749400',
            #'http://zhushou.360.cn/detail/index/soft_id/199152',
            #'http://zhushou.360.cn/',
            'http://www.waptw.com/',
            #'http://zhushou.360.cn/list/index/cid/2?page=1',
            #'http://zhushou.360.cn/list/index/cid/1?page=1',
            #'http://www.waptw.com/soft/33627.html',
            ]
    is_start = True
    def parse(self,response):
        items = []
        #if re.match(ur".*itunes\.apple\.com.*",response.url):
            #items+=itunes.parse_content_links(response)
        #    items+=itunes.parse_content(response)
        if re.match(ur".*zhushou\.360\.cn.*",response.url):
            #items+=zhushou.parse_content_links(response)
            items+=zhushou.parse_rankpage(response)
            if re.match(ur'.*page=1$',response.url):
                hxs = HtmlXPathSelector(response)
                lastpage=int(hxs.select("//script/text()").re("pg.pageCount.*\d+")[0][15::])
                for pagenum in range(lastpage,2,-1):
                    url = re.sub(r"\d+$",str(pagenum),response.url)
                    yield Request(url, callback=self.parse)
        elif re.match(ur".*waptw\.com.*",response.url):
            #items+=waptw.parse_content_links(response)
            items+=waptw.parse_update(response)
        #elif re.match(ur".*anzhi\.com.*",response.url):
            #items+=anzhi.parse_content_links(response)
        #    items+=anzhi.parse_content(response)
        #elif re.match(ur".*google\.com.*",response.url):
            #items+=google.parse_content_links(response)
        #    items+=google.parse_content(response)
        
        if self.is_start :
            self.is_start = False
            for url in updateurls():
                yield Request(url,callback=self.parse)
        for item in items:
            yield self.return_item(item)

    def return_item(self,item):
        return item

