import pymongo
from datetime import datetime
from scrapy.exceptions import DropItem
from scrapy import log
from crawler.settings import MONGODB
from crawler.dicts import UMDict
from crawler.db import mongo

class mongo_storage(object):
    def __init__(self):
        self.db = mongo.get_db()
        self.date = datetime.now().strftime("%Y-%m-%d")
                                     
    def process_item(self, item, spider):
        if 'MetaItem' == item.__class__.__name__:
            self.process_meta_item(item)
        elif 'CommentItem' == item.__class__.__name__:
            self.process_comment_item(item)
        elif 'UpdateItem' == item.__class__.__name__:
            self.process_update_item(item)
        elif 'LinkItem' == item.__class__.__name__:
            self.process_link_item(item)
        elif 'ApkItem' == item.__class__.__name__:
            self.process_apk_item(item)
        elif 'MarketItem' == item.__class__.__name__:
            self.process_market_item(item)
        elif 'ErrorItem' == item.__class__.__name__:
            self.process_error_item(item)
        else:
            raise DropItem("Unknown Item Type !!!")
        return item

    def process_error_item(self,item):
        self.db.exceptions.update({"market":item['market'],"date":self.date,"itemtype":item['itemtype']},
                {"$inc":{"num":1},"$set":{item['md5']:{item['info']:item['traceback']}}},True)
        self.db.appmeta.update({"md5":item['md5']},{"$set":{"avaiable":3}})

    def process_meta_item(self,item):
        utf8_name = item['name']
        if len(utf8_name.encode('utf-8'))-len(utf8_name)>0:
            item["language"] = "ch"
        else:
            item["language"] = "en"
        item['description'] = "".join(item['description'].split())

        self.db.category.update({"category":item['category']},{"$inc":{"total":1}},True)

        self.db.appmeta.update({'md5':item['md5']},
                {"$set":dict(item)},True)

        self.db.appmeta.update({'md5':item['md5']},
                {"$set":{"avaiable":1}},True)

        self.db.market.update({'market':item['market']},
                {"$inc":{"content."+self.date : 1}},True)

    def process_comment_item(self,item):
        self.db.appmeta.update({'md5':item['md5']},
                {"$addToSet":{comment:{
                    "datetime":item['date'],
                    "content" :item['content'],
                    "username":item['username']
                    }}},
                True)

    def process_link_item(self,item):
        if not self.db.appmeta.find_one({'md5':item['md5']}):
            self.db.appmeta.insert(dict(item))
            self.db.market.update({'market':item['market']},
                    {"$inc":{"LinkItem."+self.date : 1}},True)

    def process_update_item(self,item):
        self.db.appmeta.update({'md5':item['md5']},
            {"$set":{'download.' + self.date : item['down']}})

    def process_apk_item(self,item):
        self.db.appmeta.update({'md5':item['md5']},
            {"$set":{"package_name":item['package_name']}})

    def process_market_item(self,item):
        self.db.market.update({"market":item['name']},
                {"$set":{"appsum."+self.date:item['appsum']}},
                True)
