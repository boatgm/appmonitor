#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import urlparse
from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings
from crawler.items import *

class Spider(CrawlSpider):
    name = 'appchina'
    start_urls = [
        'http://www.appchina.com/app/com.tencent.mobileqq/',
        'http://www.appchina.com/app/com.mygame_spjiguikda/',
        'http://www.appchina.com/app/com.adwhirl.dixiacheng/',
        'http://www.appchina.com/app/cn.com.fetion/',
            ]
    def parse(self, response):
        items = []
        items += parse_content_links(response)
        if re.match(ur'.*/app/[0-9a-z.]+/',response.url):
            items += parse_content(response)
        return items

def parse_content_links(response):
    items = []
    hxs = HtmlXPathSelector(response)
    for url in list(set(hxs.select("//a/@href").re(r"/app/[0-9a-z.]+/"))):
        item = LinkItem()
        item['url'] = "http://www.appchina.com"+url
        item['md5'] = md5(item['url']).hexdigest()
        item['market'] = "appchina"
        items.append(item)
    return items

def parse_content(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = MetaItem()
        item['md5'] = md5(response.url).hexdigest()
        item['url'] = response.url
        item['app_id'] = re.findall(r"/[0-9a-z.]+/",response.url)[-1][1:-1:]
        item['name'] = hxs.select("//h1[@class=\"cname\"]/text()").extract()[0]
        item['update_time'] = hxs.select("//div[@class=\"detail cf\"]/div[@class=\"disc cutoff\"][2]/text()").re(r"[0-9-]+")[0]
        item['app_version'] = hxs.select("//div[@class=\"detail cf\"]/div[@class=\"disc cutoff\"][1]/text()").re(r"[0-9.]+")[0]
        item['language'] = "cn"
        item['package_url'] = hxs.select("//div[@class=\"download cf\"]/ul/li/a[@class=\"free\"]/@href").re("http://.*\?")[0][0:-1:]
        item['package_name'] = re.findall(r"[^/]+",item['package_url'])[-1]
        item['size'] = hxs.select("//div[@class=\"detail cf\"]/div[@class=\"disc bold cutoff\"][2]/@title").extract()[0]
        item['comment_url'] = item['url'] + hxs.select("//a[@class=\"linkmore\"]/@href").extract()[0]
        item['icon'] = hxs.select("//img[@class=\"pic\"]/@src").extract()[0]
        item['market'] = "appchina"
        item['images'] = hxs.select("//ul[@class=\"screenshoot\"]/li/a/img/@src").extract()
        item['description'] = hxs.select("//p[@id=\"sorh\"]").extract()[0]
        item['category'] = hxs.select("//div[@class=\"detail cf\"]/div[@class=\"disc bold cutoff\"][3]/@title").extract()[0]
        item['developer'] = hxs.select("//div[@class=\"about-author cf\"]/a/text()").extract()[0]
        item['email'] = None
        item['devpage'] = None
        item['level'] = hxs.select("//div[@class=\"result-mark\"]/p/text()").re("[0-9.]+")[0]
        item['price'] = None
        items.append(item)
        pass
    except Exception as e :
        print e
        pass
    return items
