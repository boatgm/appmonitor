import urlparse
import re
import json
import requests
from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,FormRequest
from scrapy.conf import settings
from crawler.items import *

class Spider(CrawlSpider):
    name = 'searchengine'
    start_urls = ['http://www.baidu.com']
    is_start = True

    def parse(self,response):
        items = []
        if re.match(ur".*\.baidu\.com.*",response.url):
            items+=parse_baidu(response)
            if re.match(ur".*page=1.*",response.url):
                for pagenum in range(6):
                    url="http://www.baidu.com/?kw="+k
                    yield Request(url,callback=self.parse)

        elif re.match(ur".*\.google\..*",response.url):
            items+=parse_google(response)
            if re.match(ur".*page=1.*",response.url):
                for pagenum in range(6):
                    url="http://www.baidu.com/?kw="+k
                    yield Request(url,callback=self.parse)

        elif re.match(ur".*\.weibo\..*",response.url):
            items+=parse_google(response)
            if re.match(ur".*page=1.*",response.url):
                for pagenum in range(6):
                    url="http://www.baidu.com/?kw="+k
                    yield Request(url,callback=self.parse)

        if self.is_start:
            self.is_start = False
            for k in keywords:
                url="http://www.baidu.com/?kw="+k
                yield Request(url,callback=self.parse)
                url="http://www.google.hk/?kw="+k
                yield Request(url,callback=self.parse)
                url="http://s.weibo.cn/?kw="+k
                yield Request(url,callback=self.parse)

    def return_item(self,item):
        return item

def parse_google(response):
    items = []
    hxs=HtmlXPathSelector(response)
    return items

def parse_baidu(response):
    items = []
    hxs=HtmlXPathSelector(response)
    return items

def parse_weibo(response):
    items = []
    hxs=HtmlXPathSelector(response)
    return items
