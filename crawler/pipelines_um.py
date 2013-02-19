import pymongo
from datetime import datetime
from scrapy.exceptions import DropItem
from scrapy import log
from crawler.settings import MONGODB
from crawler.dicts import UMDict

class mongo_storage(object):
    def __init__(self):
        connection = pymongo.Connection(MONGODB['host'],MONGODB['port'])
        self.db = connection[MONGODB['name']]
        self.date = datetime.now().strftime("%Y-%m-%d")
    def create_index(self):
        db.appmeta.ensure_index({"md5":1},name="appmeta_key")
        db.marketmeta.ensure_index({"marketmeta":1},name="appmeta_key")
                                     
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
        """ process content meta, conten meta update immediately. """
        utf8_name = item['name']
        if len(utf8_name.encode('utf-8'))-len(utf8_name)>0:
            item["language"] = "ch"
        else:
            item["language"] = "en"
        try:
            item['category_detail'] = UMDict[item['categroy']]
        except Exception as e:
            db.exceptions.update({"market":item['market'],"date":self.date},
                    {"$addToSet":{"unknown_catagory":item['category']}},True)

        self.db.appmeta.update({'md5':item['md5']},
                {"$set":dict(item).update({"avaiable":1})},True)

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

    def process_update_item(self,item):
        """ update item`s download number"""
        if self.db.appmeta.find({'md5':item['md5']},{"package_name":1,"app_id":1}):
            self.db.appmeta.update({'md5':item['md5']},
                {"$set":{"download."+self.date:item['down']}},True)
        else:
            self.db.appmeta.update({'md5':item['md5']},{
                'md5':item['md5'],
                'url':item['url'],
                'market':item['market'],
                'download':{self.date:item['down']}
                },True)

    def process_apk_item(self,item):
        self.db.appmeta.update({'md5':item['md5']},
            {"$set":{"package_name":item['package_name']}},True)

    def process_market_item(self,item):
        self.db.market.update({"market":item['name']},
                {"$set":{"appsum."+self.date:item['appsum']}},
                True)
