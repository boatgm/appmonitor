#coding:utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CrawlerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass
class MarketItem(Item):
    date = Field()
    name = Field()
    app_category = Field()
    game_category = Field()
    appsum = Field()
    app_num = Field()
    game_num = Field()

    def __str__(self):
        return ("MarketItem:%s"%(self['name']))

class MetaItem(Item):
    md5 = Field()
    #应用在平台上的ID标识
    app_id = Field() 
    #应用名称 不含版本号
    name = Field()
    #应用信息更新时间
    update_time = Field()
    #应用版本 格式：数字和点号组合
    app_version = Field()
    #开发者名称
    developer = Field()
    #语言,cn/en/jp 遵照django国际化标准设定
    language = Field()
    #APP包链接
    package_url = Field()
    package_md5 = Field()
    #App下载爬虫负责填充
    size = Field()
    #APP评论链接
    comment_url = Field()
    #APP ICON标志url
    icon = Field()
    #内容页规范化url
    url = Field()
    #市场标志 使用字典规范 采用核心域名 小写
    market = Field()
    #APP 描述性信息
    description = Field()
    #APP 应用截图
    images = Field()
    #APP 主分类 app or game
    category = Field()
    category_general = Field()
    #APP 具体分类 使用函数进行标准化
    category_detail = Field()
    #包名 交给APP spider处理
    package_name = Field()
    #开发者联系方式 不存在则设为""
    email = Field()
    #APP 等级
    level = Field()
    #开发者的页面
    devpage = Field()
    #评分 未获取设为 0
    rate = Field()
    #APP 价格
    price = Field()
    def __str__(self):
        return ("MetaItem:%s\t%s"%(self['md5'],self['name']))

class ApkItem(Item):
    md5 = Field()
    package_name = Field()
    size = Field()
    sdk = Field()
    apk_store_path = Field()
    def __str__(self):
        return ("ApkItem")

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
