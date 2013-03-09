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
from crawler.urls import geturls
class Spider(CrawlSpider):
    """ General configuration of the Crawl Spider """
    name = 'waptw'
    start_urls = [ 
            'http://www.waptw.com/sonyericsson/x11/rank/week/0/1',
            'http://www.waptw.com/sonyericsson/x11/rank/week/0/1',
            'http://www.waptw.com/sonyericsson/x11/new/0/1',
            'http://www.waptw.com/soft/27701.html',
            'http://www.waptw.com/soft/22687.html',
            'http://www.waptw.com/soft/22687.html',
            ]

    def parse(self, response):
        items = []
        items += parse_content_links(response)
        if re.match(ur'.*/soft/\d+.html',response.url):
            parse_content(response)
            pass
        if re.match(ur'.*/new/0/1',response.url):
            lastpage = 100
            for pagenum in range(100):
                url = re.sub(ur"\d+$",str(pagenum),response.url)
                yield Request(url,callback=self.parse)
        for item in items:
            yield self.return_item(item)

    def return_item(self,item):
        return item


def parse_content_links(response):
    items = []
    hxs = HtmlXPathSelector(response)
    for url in list(set(hxs.select("//a/@href").re(r"/soft/\d+.html"))):
        item = LinkItem()
        item['url'] = "http://www.waptw.com"+url
        item['md5'] = md5(item['url']).hexdigest()
        item['market'] = "waptw"
        items.append(item)
    return items

def parse_content(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = MetaItem()
        item['md5'] = md5(response.url).hexdigest()
        item['url'] = response.url
        item['app_id'] = re.findall(r"\d+",response.url)[-1]
        item['name'] = hxs.select("//title/text()").re(r"^.*V")[0][0:-1:]
        item['update_time'] = hxs.select("//table[@class=\"summary\"]/tr[1]/td[1]/text()").re("[0-9-]+")[0]
        item['app_version'] = hxs.select("//title/text()").re(r"V[0-9.]*")[0][1::]
        item['language'] = "cn"
        item['package_url'] = hxs.select("//div[@class=\"down-btns\"]/a[1]/@href").re(r"^[^?]*apk")[0]
        item['package_name'] = re.findall(r"[^/]*\.apk",item['package_url'])[0]
        item['size'] = hxs.select("//table[@class=\"summary\"]/tr[1]/td[2]/text()").extract()[0]
        item['comment_url'] = "http://www.waptw.com/sonyericsson/x11/comment/"+item['app_id']
        item['icon'] = hxs.select("//div[@class=\"imgbox\"]/img/@src").extract()[0]
        item['market'] = "waptw"
        item['images'] = hxs.select("//div[@class=\"imgbox\"]/img/@src").extract()
        item['description'] = hxs.select("//div[@class=\"G-panel\"]/p").extract()[0]
        item['category'] = hxs.select("//div[@class=\"crumbs\"]/a[2]/text()").extract()[0]
        item['developer'] = None
        item['email'] = None
        item['devpage'] = None
        item['level'] = None
        item['price'] = hxs.select("//table[@class=\"summary\"]/tr[4]/td[1]/p/text()").extract()[0]
        items.append(item)
    except Exception as e :
        print e
    return items


def parse_index(response):
    items = []
    hxs = HtmlXPathSelector(response)
    item = MarketItem()
    item ['name'] = "waptw"
    item ['appsum'] = int(hxs.select("//li[@class=\"total\"]/em/text()").extract()[0])

    items.append(item)
    return items


def parse_update(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = UpdateItem()
        item['md5'] = md5(response.url).hexdigest()
        item['url'] = response.url
        item['down'] = int(hxs.select("//table[@class=\"summary\"]/tr[2]/td[1]/text()").extract()[0])
        item['market'] = "waptw"
        items.append(item)
    except Exception as e :
        print e
    return items
