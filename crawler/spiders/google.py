#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import urlparse
import traceback
from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings
from crawler.items import *
from crawler.urls import geturls

class Spider(CrawlSpider):
    name = 'google'
    #use proxy
    start_urls = [
            'https://play.google.com/store/apps/details?id=com.tencent.mobileqq',
            'https://play.google.com/store/apps/details?id=com.droidappsolutions.fingerprintscanner',
            #'https://play.google.com/store/apps/category/CASUAL?feature=category-nav',
            #'https://play.google.com/store/apps/category/GAME_WALLPAPER/collection/topselling_free?start=24&num=24',
            #'https://play.google.com/store/apps/category/CASUAL/collection/topselling_free?start=24&num=24',
            #'https://play.google.com/store/apps/category/APPLICATION/collection/topselling_free?start=0&num=24',
            #'https://play.google.com/store/apps/category/GAME/collection/topselling_free?start=0&num=24',
            ]
    def parse(self, response):
        items = []
        hxs = HtmlXPathSelector(response)
        items += parse_content_links(response)
        if re.match(ur".*/store/apps/details.*",response.url):
            items+=parse_content(response)
        elif re.match(ur".*/store/apps/category/.*start=\d+&num=24",response.url):
            lastpage=480
            for pagenum in range(480,0,-24):
                url = re.sub(r"\d+$",str(pagenum),response.url)
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
    for url in list(set(hxs.select("//a/@href").re(r"/store/apps/details\?id=[^&]*"))):
        item = LinkItem()
        item['url'] = "https://play.google.com"+url
        item['md5'] = md5(item['url']).hexdigest()
        item['market'] = "google"
        items.append(item)
    return items

def parse_content(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = MetaItem()
        item['market'] = "google"
        item['md5'] = md5(response.url).hexdigest()
        item['url'] = response.url
        item['app_id'] = re.findall(r"[^=?&]+",response.url)[-1]
        item['name'] = hxs.select("//h1[@class=\"doc-banner-title\"]/text()").extract()[0]
        item['update_time'] = hxs.select("//time[@itemprop=\"datePublished\"]/text()").extract()[0]
        item['app_version'] = hxs.select("//dd[@itemprop=\"softwareVersion\"]/text()").extract()[0]
        item['language'] = None
        item['package_url'] = None
        item['package_name'] = item['app_id']
        item['size'] = hxs.select("//dd[@itemprop=\"fileSize\"]/text()").extract()[0]
        item['comment_url'] = None
        item['icon'] = hxs.select("//div[@class=\"doc-banner-icon\"]/img/@src").extract()[0]
        item['images'] = hxs.select("//img[@class=\"doc-screenshot-img\"]/@src").extract()
        item['description'] = hxs.select("//div[@id=\"doc-original-text\"]").extract()[0][51:-6:]
        item['category'] = hxs.select("//dl[@class=\"doc-metadata-list\"]/dd[5]/a/text()").extract()[0]
        item['developer'] = hxs.select("//td[@class=\"doc-banner-title-container\"]/a/text()").extract()[0]
        item['email'] = None
        item['devpage'] = "https://play.google.com"+hxs.select("//td[@class=\"doc-banner-title-container\"]/a/@href").extract()[0]
        item['level'] = hxs.select("//div[@class=\"ratings goog-inline-block\"]/@content").extract()[0]
        item['price'] = hxs.select("//dd[@itemprop=\"offers\"]/text()").extract()[0]
        items.append(item)
    except Exception as e :
        error = ErrorItem()
        error['market'] = item['market']
        error['md5'] = item['md5'] 
        error['info'] = str(e)
        error['itemtype'] = "meta" 
        error['traceback'] = traceback.format_exc()
        items.append(error)
    return items


def parse_update(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try :
        item = UpdateItem()
        item['market'] = "google"
        item['url'] = response.url
        item['md5'] = md5(response.url).hexdigest()
        item['down'] = hxs.select("//dd[@itemprop=\"numDownloads\"]/text()").extract()[0]
        items.append(item)
    except Exception as e :
        Error = ErrorItem()
        Error['md5'] = item['md5']
        Error['market'] = item['market']
        Error['itemtype'] = 'update'
        Error['info'] = str(e)
        Error['traceback'] = traceback.format_exc()
        items.append(Error)
    return items
