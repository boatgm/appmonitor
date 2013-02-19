#coding:utf-8
from scrapy.item import Item, Field

class CrawlerItem(Item):
    pass

class MarketItem(Item):
    date = Field()
    name = Field()
    category = Field()
    appsum = Field()

    def __str__(self):
        return ("MarketItem:%s"%(self['name']))

class MetaItem(Item):
    md5 = Field()
    url = Field()
    package_url = Field()
    comment_url = Field()
    market = Field()
    app_id = Field() 
    app_version = Field()
    package_name = Field()
    update_time = Field()
    
    name = Field()
    description = Field()
    images = Field()
    icon = Field()

    language = Field()
    size = Field()

    category = Field()
    category_general = Field()
    category_detail = Field()

    email = Field()
    developer = Field()
    devpage = Field()

    down = Field()
    rate = Field()
    price = Field()
    level = Field()

    def __str__(self):
        return ("MetaItem:%s\t%s"%(self['md5'],self['name']))

class ApkItem(Item):
    md5 = Field()
    package_name = Field()
    package_info = Field()
    usespermission = Field()
    usesfeature = Field()
    label = Field()
    version = Field()
    size = Field()
    sdk = Field()
    apk_store_path = Field()
    def __str__(self):
        return ("ApkItem:%s"%(self['package_name']))

class CommentItem(Item):
    md5 = Field()
    comment = Field()
    username = Field()
    date = Field()
    
    def __str__(self):
        return ("CommentItem")
    
class LinkItem(Item):
    md5 = Field()
    url = Field()
    tag = Field() #1:
    recommend = Field()#1:ture;0:false
    rank = Field()#in rank inc 1
    avaiable = Field()#1:ture;0:false
    market = Field()
    
    def __str__(self):
        return ("LinkItem")
    
class UpdateItem(Item):
    md5 = Field()
    url = Field()
    down = Field()
    rate = Field()
    date = Field()
    market=Field()

    def __str__(self):
        return ("UpdateItem")

class ErrorItem(Item):
    md5 = Field()
    market = Field()
    itemtype = Field()
    info = Field()
    traceback = Field()

    def __str__(self):
        return ("ErrorItem: %s,%s"%(self['market'],self['info']))
