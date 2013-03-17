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
from crawler.spiders import waptw,zhushou,anzhi,google

class Spider(CrawlSpider):
    name = 'marketrank'
    start_urls = [
            'http://www.waptw.com/sonyericsson/x11/new/0/1',
            'http://www.waptw.com/sonyericsson/x11/rank/week/0/1',
            'http://www.waptw.com/sonyericsson/x11/rank/month/0/1',
            'http://www.waptw.com/sonyericsson/x11/rank/all/0/1',
            'http://zhushou.360.cn/list/index/cid/1?page=1',
            'https://play.google.com/store/apps/category/APPLICATION/collection/topselling_free?start=0&num=24',
            ]

    def parse(self, response):
        maxpage=5 
        items = []
        hxs = HtmlXPathSelector(response)
        if re.match(".*waptw\.com.*",response.url):
            for pagenum in range(maxpage,1,-1):
                url = re.sub(r"\d+$",str(pagenum),response.url)
                yield Request(url, callback=self.parse_rankpage)
        if re.match(".*zhushou\.360\.cn.*",response.url):
            for pagenum in range(5):
                url = re.sub(r"\d+$",str(pagenum),response.url)
                yield Request(url, callback=self.parse_rankpage)
        if re.match(".*play\.google\.com.*",response.url):
            for pagenum in range(480,0,-24):
                url = re.sub(r"start=\d+","start="+str(pagenum),response.url)
                yield Request(url, callback=self.parse_rankpage)

    def parse_rankpage(self, response):
        items = []
        if re.match(".*waptw\.com.*",response.url):
            items += waptw.parse_content_links(response)
            #items+=waptw.parse_rankpage(response)
        if re.match(".*zhushou\.360\.cn.*",response.url):
            items += zhushou.parse_rankpage(response)
        if re.match(".*play\.google\.com.*",response.url):
            items += google.parse_content_links(response)
        return items
