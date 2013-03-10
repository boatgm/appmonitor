#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import urlparse
import traceback
from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy.http import Request
from crawler.items import *

class Spider(CrawlSpider):
    name = 'itunes'
    start_urls = [
        #'https://itunes.apple.com/cn/genre/ios-gong-ju/id6002?mt=8',
        #'https://itunes.apple.com/cn/genre/ios-you-xi/id6014?mt=8',
        #'https://itunes.apple.com/cn/genre/ios/id36?mt=8',
        #'https://itunes.apple.com/cn/genre/ios-productivity/id6007?l=cn&mt=8',
        'https://itunes.apple.com/cn/app/id428750296?mt=8'
            ]

    def parse(self,response):
        items = []
        items+=parse_content_links(response)
        if re.match(ur'.*/cn/app/id\d+.*mt=8',response.url):
            items+=parse_content(response)

        if re.match(ur".*/cn/genre/ios-.*",response.url):
            hxs = HtmlXPathSelector(response)
            for url in list(set(hxs.select("//a/@href").re(r"https://.*/cn/genre/ios-.*"))):
                url = re.sub(r"&letter=.","",url)
                yield Request(url,callback=self.parse)

        for item in items:
            yield self.return_item(item)

    def return_item(self,item):
        return item
    def request_url(self,url):
        yield Request(url,callback=self.parse)

def parse_content_links(response):
    items = []
    hxs = HtmlXPathSelector(response)
    for url in list(set(hxs.select("//a/@href").re(r"/cn/app/.*/id\d+"))):
        try:
            item = LinkItem()
            item['url'] = "https://itunes.apple.com/cn/app/"+re.findall(r"id\d+",url)[-1]
            item['md5'] = md5(response.url).hexdigest()
            item['market'] = "itunes"
            items.append(item)
        except Exception as e :
            error = ErrorItem()
            error['market'] = "itunes"
            error['itemtype'] = "link" 
            error['md5'] = item['md5'] 
            error['info'] = str(e)
            error['traceback'] = traceback.format_exc()
            items.append(error)
    return items

def parse_update(response):
    items = []
    return items

def parse_content(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = MetaItem()
        item['md5'] = md5(response.url).hexdigest()
        item['url'] = response.url
        item['app_id'] = re.findall(r"\d+",response.url)[-1]
        item['name'] = hxs.select("//div[@class=\"left\"]/h1/text()").extract()[0]
        item['update_time'] = hxs.select("//li[@class=\"release-date\"]/text()").extract()[0]
        item['app_version'] = hxs.select("//div[@id=\"left-stack\"]//li[4]/text()").extract()[0]
        item['language'] = hxs.select("//li[@class=\"language\"]/text()").extract()[0]
        item['package_url'] = None
        item['package_name'] = None
        item['size'] = hxs.select("//ul[@class=\"list\"]/li[5]/text()").extract()[0]
        item['comment_url'] = None
        item['icon'] = hxs.select("//div[@class=\"artwork\"]/img/@src").extract()[0]
        item['market'] = "itunes"
        item['images'] = hxs.select("//img[@class=\"portrait\"]/@src").extract()
        item['description'] = hxs.select("//div[@class=\"product-review\"]/p").extract()[0]
        item['category'] = hxs.select("//ul[@class=\"list\"]/li[@class=\"genre\"]/a/text()").extract()[0]
        item['developer'] = hxs.select("//ul[@class=\"list\"]/li[7]/text()").extract()[0]
        item['email'] = None
        item['devpage'] = hxs.select("//div[@class=\"app-links\"]/a/@href").extract()[0]
        item['level'] = None
        item['price'] = hxs.select("//div[@class=\"price\"]/text()").extract()[0]
        items.append(item)
    except Exception as e :
        error = ErrorItem()
        error['market'] = "itunes"
        error['md5'] = item['md5'] 
        error['info'] = str(e)
        error['itemtype'] = "meta" 
        error['traceback'] = traceback.format_exc()
        items.append(error)
    return items
