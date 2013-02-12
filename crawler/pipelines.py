# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import pymongo
from datetime import datetime

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

class UMMongoDBStorage(object):
    def __init__(self):
        """ Initiate a MongoDB connection, a create the settings['MONGODB_COLLECTION'] collection. """
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.appmeta = db['appmeta']
        self.market = db['market']
    def create_index(self):
        if not db.system.index.find({"name":"appmeta"}):
            db.system.index.insert({})
        if not db.system.index.find({"name":"marketmeta"}):
            db.system.index.insert({})
        pass

                                     
    def process_item(self, item, spider):
        """ This method is called each time an item is scraped from a webpage.
        If the item validates, we store it in the MongoDB collection. If not,
        we drop it.
        """
        if 'MetaItem' == item.__class__.__name__:
            """ process meta item """
            self.process_meta_item(item)
            pass
        elif 'CommentItem' == item.__class__.__name__:
            """ process comment item """
            self.process_comment_item(item)
            pass
        elif 'UpdateItem' == item.__class__.__name__:
            """ process update item """
            self.process_update_item(item)
            pass
        elif 'LinkItem' == item.__class__.__name__:
            """ process Link item """
            self.process_link_item(item)
            pass
        elif 'ApkItem' == item.__class__.__name__:
            """ process apk item """
            self.process_apk_item(item)
            pass
        elif 'MarketItem' == item.__class__.__name__:
            """ process market item """
            self.process_market_item(item)
            pass
        else:
            raise DropItem("Unknown Item Type !!!")
            pass
        #log.msg("Item wrote to MongoDB database ", level=log.DEBUG, spider=spider) 
        return item

    def process_meta_item(self,item):
        res = self.appmeta.update({'md5':item['md5']},
                dict(item),True)
        pass

    def process_comment_item(self,item):
        self.appmeta.update({'comment_md5':item['md5']},
                {"$addToSet":{comment:{"date":item['date'],"content":item['content'],"username":item['username']}}},True)
        pass

    def process_link_item(self,item):
        self.appmeta.update({'md5':item['md5']},
                {"$set":dict(item)},True)
        pass

    def process_update_item(self,item):
        item['date']=datetime.now().strftime("%Y-%m-%d")
        if self.appmeta.find_one({'md5':item['md5']}):
            self.appmeta.update({'md5':item['md5']},
                {"$set":{"download."+item['date']:item['down']}},True)
        else:
            self.appmeta.insert({'md5':item['md5'],'url':item['url'],'market':item['market'],'download':{item['date']:item['down']}})
        pass

    def process_apk_item(self,item):
        self.appmeta.update({'package_md5':item['md5']},
                {},True)
        pass
    def process_market_item(self,item):
        item['date']=datetime.now().strftime("%Y-%m-%d")
        self.market.update({"market":item['name']},{"$set":{"appsum."+item['date']:item['appsum']}},True)
        pass


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlDBStorage(object):
    def process_item(self, item, spider):
        return item

