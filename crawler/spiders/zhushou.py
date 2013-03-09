import urlparse
import re
import json
import traceback

from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from crawler.items import *
from crawler.urls import geturls

class Spider(CrawlSpider):
    name = 'zhushou'
    start_urls = [
            'http://zhushou.360.cn/',
            'http://zhushou.360.cn/list/index/cid/1/size/all/lang/all/order/download/?page=1',
            'http://zhushou.360.cn/list/index/cid/2/size/all/lang/all/order/download/?page=1',
            ]
    def parse(self, response):
        items = []
        if re.match(ur'.*/\?page=1$',response.url):
            hxs = HtmlXPathSelector(response)
            lastpage=int(hxs.select("//script/text()").re("pg.pageCount.*\d+")[0][15::])
            for pagenum in range(lastpage):
                url = re.sub(r"\d+$",str(pagenum),response.url)
                yield Request(url, callback=self.parse)
        elif re.match(ur'.*/\?page=\d+$',response.url):
            items+=parse_rankpage(response)
        elif re.match(ur".*/detail/.*",response.url):
            items+=parse_content(response)
        elif re.match(ur"http://zhushou.360.cn/",response.url):
            items+=parse_index(response)
        else:
            pass
        for item in items:
            yield self.return_item(item)

    def return_item(self,item):
        return item
    def request_url(self,url):
        yield Request(url,callback=self.parse)

def parse_index(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = MarketItem()
        item['name'] = "zhushou"
        item['appsum'] = int(hxs.select("//input[@class=\"kwd\"]/@value").re("\d+")[0])
        items.append(item)
    except Exception as e :
        print e
    return items

def parse_content_links(response):
    items = []
    hxs = HtmlXPathSelector(response)
    for url in hxs.select("//a/@href").re(r"/detail/.*"):
        try:
            item = LinkItem()
            item ['url'] = "http://zhushou.360.cn"+url
            item ['md5'] = md5(item['url']).hexdigest()
            item ['market'] = "360"
            items.append(item)
        except Exception as e:
            print e
            pass
    return items

def parse_rankpage(response):
    items = []
    hxs = HtmlXPathSelector(response)
    applist = hxs.select("//ul[@id=\"iconList\"]/li")
    for app in applist:
        try:
            item = UpdateItem()
            item ['url'] = "http://zhushou.360.cn"+app.select("a/@href").re(r"/detail/.*")[0]
            item ['md5'] = md5(item['url']).hexdigest()
            item ['down'] = int(app.select("span/text()").re("\d+")[0])
            item ['market'] = "360"
            items.append(item)
        except Exception as e:
            print e
            pass
    return items

def parse_content(response):
    items = []
    hxs = HtmlXPathSelector(response)
    try:
        item = MetaItem()
        item['md5'] = md5(response.url).hexdigest()
        item['url'] = response.url
        item['market'] = "360"
        item['app_id'] = re.findall(r"\d+",response.url)[-1]
        item['name'] = hxs.select("//script[2]/text()").re("baike_name\":\"[^ \"]*")[0][13::]
        item['update_time'] = hxs.select("//dl[@class=\"clearfix\"]//dd[2]/p[3]/text()").re("[0-9-]+")[0]
        item['app_version'] = hxs.select("//div[@class=\"nstxt\"]/table/tr[1]/td[2]/text()").extract()[0][3::]
        item['package_url'] = hxs.select("//script[1]/text()").re(r"downurl':'[^']*")[0][10::]
        item['size'] = hxs.select("//script/text()").re(r"size':'[^']*")[0][7::]
        item['comment_url'] = "http://intf.baike.360.cn/index.php?c=message&a=getmessage&name="+item['name']
        item['icon'] = hxs.select("//dl[@class=\"clearfix\"]/dt/img/@src").extract()[0]
        item['images'] = hxs.select("//div[@class=\"overview\"]/img/@src").extract()
        item['description'] = hxs.select("//div[@class=\"alldesc\"]/text()").extract()[0]
        item['category_general'] = "app" #"game"
        item['category_detail'] = hxs.select("//div[@class=\"nstxt\"]/table/tr[2]/td[2]/text()").extract()[0][3::].split(".")[0]
        item['category'] = hxs.select("//div[@class=\"nstxt\"]/table/tr[2]/td[2]/text()").extract()[0][3::].replace(".","")
        item['developer'] = hxs.select("//div[@class=\"nstxt\"]/table/tr[2]/td[3]/text()").extract()[0][3::]
        item['email'] = None
        item['devpage'] = None
        item['level'] = hxs.select("//dl[@class=\"clearfix\"]/dd[2]/em/text()").extract()[0][0:-1:]
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

def parse_comment(response):
    items = []
    try :
        data = json.loads(response.body)
        for t in data['data']['messages']:
            item = CommentItem()
            item['md5'] = md5(response.url)
            item['content']=t['comment']
            item['date']=t['create_time']
            item['username'] = t['username']
            items.append(item)
    except Exception as e :
        print e
    return items
