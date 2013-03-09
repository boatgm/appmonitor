#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import urlparse
from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy.http import Request,FormRequest
from crawler.items import *
from crawler.urls import geturls

class Spider(CrawlSpider):
    name = 'hiapk'
    start_urls = [
            'http://apk.hiapk.com/App.aspx?action=FindAppSoftList',#POST categoryId:0,currentHash:2_1_0_0_0_0_0  3_1_0_0_0_0_0
            'http://apk.hiapk.com/Game.aspx?action=FindGameSoftList',
            #'http://apk.hiapk.com/html/2012/12/1030082.html',
            #'http://apk.hiapk.com/html/2012/12/1084607.html',
            ]
    def parse(self, response):
        items = []
        items+=parse_content_links(response)
        if re.match(r".*/html/\d{4}/\d{2}/\d+\.html",response.url):
            items+=parse_content(response)
        elif re.match(ur"http://.*SoftList",response.url):
            lastpage = 10
            for pagenum in range(lastpage):
                formdata={"currentHash":str(pagenum)+"_1_0_0_0_0_0"}
                yield FormRequest(response.url,formdata=formdata)

        for item in items:
            yield self.return_item(item)
    def return_item(self,item):
        return item

def parse_content_links(response):
    items = []
    hxs = HtmlXPathSelector(response)
    for url in list(set(hxs.select("//a/@href").re(r"/html/\d{4}/\d{2}/\d+\.html"))):
        item = LinkItem()
        item['url'] = "http://apk.hiapk.com"+url
        item['md5'] = md5(item['url']).hexdigest()
        item['market'] = "hiapk"
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
        item['name'] = hxs.select("//label[@id=\"ctl00_AndroidMaster_Content_Apk_SoftName\"]/text()").extract()[0]
        item['update_time'] = hxs.select("//label[@id=\"ctl00_AndroidMaster_Content_Apk_SoftPublishTime\"]/text()").extract()[0]
        item['app_version'] = hxs.select("//label[@id=\"ctl00_AndroidMaster_Content_Apk_SoftVersionName\"]/text()").extract()[0]
        item['language'] = hxs.select("//label[@id=\"ctl00_AndroidMaster_Content_Apk_SoftLanguage\"]/text()").extract()[0]
        item['package_url'] = "http://apk.hiapk.com/Download.aspx?aid="+item['app_id']
        item['package_name'] = None
        item['size'] = hxs.select("//label[@id=\"ctl00_AndroidMaster_Content_Apk_SoftSize\"]/text()").extract()[0]
        item['market'] = "hiapk"
        item['images'] = hxs.select("//div[@class=\"screenimg\"]/ul/li/a/img/@src").extract()
        item['description'] = hxs.select("//label[@id=\"ctl00_AndroidMaster_Content_Apk_Description\"]/text()").extract()[0]
        item['category'] = hxs.select("//label[@id=\"ctl00_AndroidMaster_Content_Apk_SoftCategory\"]/text()").extract()[0]
        item['level'] = hxs.select("//div[@class=\"star_num\"]/text()").extract()[0]
        items.append(item)
    except Exception as e :
        print e

    return items

def parse_update(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = UpdateItem()
        item['md5'] = md5(response.url).hexdigest()
        item['url'] = response.url
        item['down'] = int(hxs.select("//label[@id=\"ctl00_AndroidMaster_Content_Apk_Download\"]/text()").extract()[0])
        item['market'] = "hiapk"
        items.append(item)
    except Exception as e :
        print e
    return items

