import pymongo
import sys
from crawler.db import mongo as DBUtil
from crawler.settings import LIMIT

start_urls=[
        'http://zhushou.360.cn/',
        'htpp://www.waptw.com/',
        ]

category_url=[
        'http://zhushou.360.cn/list/index/cid/2?page=1',
        'http://zhushou.360.cn/list/index/cid/1?page=1',
        'http://www.waptw.com/sonyericsson/x11/new/0/1',
        'http://www.waptw.com/sonyericsson/x11/rank/week/0/1',
        ]

def contenturls():
    urls = []
    db = DBUtil.get_db()
    res = db.appmeta.find({"$or":[{"market":'360'},{"market":'waptw'}],"name":None,"avaiable":None},{"url":1,"md5":1,"_id":0},limit=LIMIT)
    for row in res:
        urls.append(row['url'])
        db.appmeta.update({"md5":row['md5']},{"$set":{"avaiable":0}})
    return urls

def updateurls():
    urls = []
    db = DBUtil.get_db()
    res = db.appmeta.find({"$or":[{"market":'waptw'}],"avaiable":1},{"url":1,"md5":1,"_id":0},limit=LIMIT)
    for row in res:
        urls.append(row['url'])
        #db.appmeta.update({"md5":row['md5']},{"$inc":{"lock":2}})
    return urls

def commenturls():
    urls = []
    db = DBUtil.get_db()
    res = db.appmeta.find({"$or":[{"market":'waptw'}],"name":None,"ulock":None},{"comment_url":1,"md5":1,"_id":0},limit=10000)
    for row in res:
        urls.append(row['comment_url'])
        #db.appmeta.update({"md5":row['md5']},{"$inc":{"lock":4}})
    return urls

def packages():
    urls = []
    db = DBUtil.get_db()
    res = db.appmeta.find({"$or":[{"market":'waptw'}],"package_url":{"$exists":True},"ulock":None},{"category_general":1,"app_id":1,"app_version":1,"market":1,"package_url":1,"md5":1,"_id":0},limit=10)
    for row in res:
        print row['package_url']
        url = {}
        url['package_url'] = row['package_url']
        url['app_id'] = row['app_id']
        url['app_version'] = row['app_version']
        url['market'] = row['market']
        url['md5'] = row['md5']
        url['category_general'] = row['category_general']
        urls.append(url)
    #    urls.append(row['comment_url'])
    #    #db.appmeta.update({"md5":row['md5']},{"$inc":{"lock":4}})
    return urls

def unlock():
    db = DBUtil.get_db()
    db.appmeta.update({"lock":1},{"$set":{"lock":None}})

def geturls(market,category):
    urls = []
    return urls

class urls():
    """
    url proccess class. 
    support get ,check, decorate urls.
    """
    @classmethod
    def geturls(cls,key,urlclass):
        """ get urls to spiders from mongodb """
        LIMIT=100
        fields = {urlclass:1,"md5":1,"_id":0}
        urls = []
        DBUtil.get_db()
        #res = DBUtil.db.appmeta.find(key, {"url":1,"md5":1,"_id":0},limit=LIMIT)
        #for row in res:
        #    urls.append(row[urlclass])
        #    cls.lock(row['md5'])
        return urls
    
    @classmethod
    def check(cls, md5):
        #return True if DBUtil.count("appmeta", {"md5":md5}) else False
        pass

    @classmethod
    def lock(cls, md5):
        #DBUtil.update("appmeta", {"md5":md5}, {"lock":1})
        pass

    @classmethod
    def unlock(cls, md5):
        #DBUtil.update("appmeta", {"md5":md5}, {"lock":0})
        pass

    @classmethod
    def decorate(cls, url):
        return url
