#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import urlparse
from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from crawler.items import ApkItem,MetaItem,CommentItem,LinkItem

class Spider(CrawlSpider):
    """ General configuration of the Crawl Spider """
    name = 'nduoa'
    start_urls = [
            'http://www.nduoa.com/apk/detail/476588',
            'http://www.nduoa.com/apk/detail/472053',
            'http://www.nduoa.com/apk/detail/473183',
            'http://www.nduoa.com/apk/detail/476495',
            ]
    def parse(self, response):
        items = []
        items+=parse_content_links(response)
        if re.match(ur'.*/apk/detail/\d+',response.url):
            items+=parse_content(response)
        return items

def parse_content_links(response):
    items = []
    hxs = HtmlXPathSelector(response)
    for url in list(set(hxs.select("//a/@href").re(r"/apk/detail/\d+"))):
        item = LinkItem()
        item['url'] = "http://www.nduoa.com"+url
        item['md5'] = md5(item['url']).hexdigest()
        item['market'] = "nduoa"
        items.append(item)
    return items

def parse_content(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = MetaItem()
        item['market'] = "nduoa"
        item['md5'] = md5(response.url).hexdigest()
        item['url'] = response.url
        item['app_id'] = re.findall(r"\d+",response.url)[-1]
        item['name'] = hxs.select("//div[@class=\"name\"]/span[@class=\"title\"]/text()").extract()[0]
        item['update_time'] = hxs.select("//div[@class=\"updateTime row\"]/em/text()").extract()[0]
        item['app_version'] = hxs.select("//div[@class=\"name\"]/span[@class=\"version\"]/text()").re(r"[0-9.]+")[0]
        item['package_url'] = "http://www.nduoa.com"+hxs.select("//a[@class=\"d_pc_normal\"]/@href").extract()[0]
        item['package_name'] = None
        item['size'] = hxs.select("//div[@class=\"size row\"]/text()").extract()[0][3::]
        item['comment_url'] = None
        item['icon'] = hxs.select("//div[@class=\"icon\"]/img/@src").extract()[0]
        item['images'] = hxs.select("//ul[@class=\"shotbox\"]/li/img/@src").extract()
        item['description'] =  "".join(hxs.select("//div[@class=\"inner\"]/p").extract())
        item['category'] = hxs.select("//div[@id=\"breadcrumbs\"]/span[3]/a/text()").extract()[0]
        item['developer'] = hxs.select("//div[@class=\"author row\"]/span/a/text()").extract()[0]
        item['email'] = None
        item['devpage'] = None
        item['level'] = hxs.select("//span[@class=\"level\"]/text()").re("\d+")[0]
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
