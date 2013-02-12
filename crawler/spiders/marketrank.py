import urlparse
import re
import requests
from md5 import md5
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,Response,TextResponse
from scrapy.conf import settings
from crawler.items import *
from crawler.spiders import waptw,zhushou,anzhi
from crawler.urls import geturls

class Spider(CrawlSpider):
    name = 'marketrank'
    start_urls = [
            'http://www.waptw.com/sonyericsson/x11/new/0/1',
            'http://www.waptw.com/sonyericsson/x11/rank/week/0/1',
            'http://www.waptw.com/sonyericsson/x11/rank/month/0/1',
            'http://www.waptw.com/sonyericsson/x11/rank/all/0/1',
            'http://zhushou.360.cn/list/index/cid/2?page=1',
            'http://zhushou.360.cn/list/index/cid/1?page=1',
            ]

    def parse(self, response):
        items = []
        hxs = HtmlXPathSelector(response)
        if re.match(".*waptw\.com.*",response.url):
            #lastpage=int(hxs.select("//span[@class=\"pages\"]/text()").re("/\d+")[0][1::])
            maxpage=5 
            for pagenum in range(maxpage,1,-1):
                url = re.sub(r"\d+$",str(pagenum),response.url)
                yield Request(url, callback=self.parse_rankpage)
        if re.match(".*anzhi\.com.*",response.url):
            lastpage=5
            #    yield Request(url, callback=self.parse_rankpage)
            pass
        if re.match(".*zhushou\.360\.cn.*",response.url):
            #    yield Request(url, callback=self.parse_rankpage)
            pass
        if re.match(".*play\.google\.com.*",response.url):
            #    yield Request(url, callback=self.parse_rankpage)
            pass
        #return items

    def parse_rankpage(self, response):
        items = []
        if re.match(".*waptw\.com.*",response.url):
            #items+=waptw.parse_rankpage(response)
            items+=waptw.parse_content_links(response)
        if re.match(".*zhushou\.360\.cn.*",response.url):
            items+=zhushou.parse_rankpage(response)
        if re.match(".*play\.google\.com.*",response.url):
            items+=google.parse_rankpage(response)
        return items
