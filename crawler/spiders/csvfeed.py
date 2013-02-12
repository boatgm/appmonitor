from scrapy.contrib.spiders import CSVFeedSpider
from crawler.items import *

class CsvSpider(CSVFeedSpider):
    name = 'csv'
    #allowed_domains = ['$domain']
    start_urls = [
            'http://www.www/feed.csv',
            ]
    headers = ['id', 'name', 'description', 'image_link']
    delimiter = '\t'

    # Do any adaptations you need here
    def adapt_response(self, response):
        return response

    def parse_row(self, response, row):
        i = CsvItem()
        i['url'] = row['url']
        i['name'] = row['name']
        i['description'] = row['description']
        return i
