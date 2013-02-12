from scrapy.contrib.spiders import XMLFeedSpider
from crawler.items import *

class RssSpider(XMLFeedSpider):
    name = 'rss'
    #allowed_domains = ['$domain']
    start_urls = ['http://www.$domain/feed.xml']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        i = RssItem()
        i['url'] = selector.select('url').extract()
        i['name'] = selector.select('name').extract()
        i['description'] = selector.select('description').extract()
        return i
