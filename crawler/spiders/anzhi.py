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
from crawler.urls import geturls
class Spider(CrawlSpider):
    name = 'anzhi'
    #start_urls = geturls("anzhi","content")
    start_urls = [
        'http://www.anzhi.com/soft_505956.html',
        'http://www.anzhi.com/soft_573085.html',
        'http://www.anzhi.com/soft_585612.html',
        'http://www.anzhi.com/sort_1_1_hot.html',
        'http://www.anzhi.com/sort_2_1_hot.html',
            ]
    def parse(self, response):
        items = []
        items += parse_content_links(response)
        if re.match(ur'.*/soft_\d+\.html',response.url):
            parse_content(response)
        elif re.match('http://www.anzhi.com/sort_\d_1_hot.html',response.url):
            hxs = HtmlXPathSelector(response)
            lastpage=50
            #int(hxs.select("//li[@class=\"pages\"]/a[@class=\"selected\"]/text()").extract()[0])
            for pagenum in range(lastpage,0,-1):
                url = re.sub(r"\d+_hot.html",str(pagenum)+"_hot.html",response.url)
                yield Request(url, callback=self.parse)
        else:
            pass
        for item in items:
            yield self.return_item(item)

    def return_item(self,item):
        return item

def parse_content_links(response):
    items = []
    hxs = HtmlXPathSelector(response)
    for url in list(set(hxs.select("//a/@href").re(r"/soft_\d+\.html"))):
        item = LinkItem()
        item['market'] = "anzhi"
        item['url'] = "http://www.anzhi.com"+url
        item['md5'] = md5(item['url']).hexdigest()
        items.append(item)
    return items

def parse_content(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = MetaItem()
        item['market'] = "anzhi"
        item['md5'] = md5(response.url).hexdigest()
        item['url'] = response.url
        item['app_id'] = re.findall(r"\d+",response.url)[-1]
        item['name'] = hxs.select("//div[@class=\"titleline\"][1]/h1/text()").extract()[0]
        item['update_time'] = hxs.select("//div[@class=\"titleline\"][2]/span[3]/text()").extract()[0][3::]
        item['app_version'] = hxs.select("//div[@class=\"titleline\"][1]/text()").re(r"[0-9.]+")[0]
        item['package_url'] = hxs.select("//div[@id=\"op_left\"]/a[1]/@href").extract()[0]
        item['package_name'] = None
        item['size'] = hxs.select("//div[@class=\"titleline\"][3]/span[2]/text()").extract()[0][3::]
        item['comment_url'] = "http://www.anzhi.com"+ hxs.select("//script[3]/text()").re("/comment.*\"")[0][0:-7:]
        item['icon'] = hxs.select("//div[@class=\"d_img l\"]/img/@src").extract()[0]
        item['images'] = hxs.select("//div[@class=\"imgoutbox\"]/ul/li/img/@src").extract()
        item['description'] = hxs.select("//div[@class=\"des\"]/p").extract()[0]
        item['category'] = hxs.select("//div[@class=\"titleline\"][2]/span[2]/text()").extract()[0][3::]
        item['developer'] = hxs.select("//div[@class=\"titleline\"][2]/span[1]/text()").extract()[0][3::]
        item['email'] = None
        item['devpage'] = None
        item['level'] = None
        item['price'] = None
        items.append(item)
    except Exception as e :
        Error = ErrorItem()
        Error['md5'] = item['md5']
        Error['market'] = item['market']
        Error['itemtype'] = 'meta'
        Error['info'] = str(e)
        Error['traceback'] = traceback.format_exc()
        items.append(Error)
    return items

def parse_rankpage(self, response):
    items = []
    hxs = HtmlXPathSelector(response)
    applist = hxs.select("//div[@class=\"top\"]")
    for app in applist:
        try:
            item = UpdateItem()
            item ['url'] = "http://www.anzhi.com"+app.select("span/a/@href").extract()[0]
            item ['md5'] = md5(item['url']).hexdigest()
            down = app.select("span/text()").re(r"\d+.*")[-1]
            down = re.sub(u"\u4e07","0000",down)
            down = re.sub(u"\u5343","000",down)
            down = re.findall(r"\d+",down)[0]
            item ['down'] = int(down)
            item ['market'] = "anzhi"
            items.append(item)
        except Exception as e:
            Error = ErrorItem()
            Error['md5'] = item['md5']
            Error['market'] = item['market']
            Error['itemtype'] = 'updeta'
            Error['info'] = str(e)
            Error['traceback'] = traceback.format_exc()
            items.append(Error)
    return items
