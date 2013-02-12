#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#========================================================================
#   FileName: datastatus.py
#     Author: gongming
#      Email: gongming@umeng.com
#   HomePage: http://umeng.com
# LastChange: 2013-01-18 12:06:27
#========================================================================
import pymongo
import time
#from crawl import settings
#from scrapy.conf import settings

class datastatus():
    HOST="localhost"
    PORT=27017
    NAME="test"
    db = None
    @classmethod
    def open(cls):
        if cls.db is None:
            cls.db = pymongo.Connection(cls.HOST,cls.PORT)[cls.NAME]
    @classmethod
    def content(cls):
        cls.open()
        content = {}
        content['360']=cls.db.appmeta.find({"market":"360"}).count()
        content['itunes'] =cls.db.appmeta.find({"market": "itunes"}).count()
        return content
    def comment(cls):
        cls.open()
        comment = {}
        cls.db.appmeta.find().count()
        pass
    def package(cls):
        cls.open()
        package = {}
        cls.db.appmeta.find().count()
        pass
    def market(clas):
        cls.open()
        market = {}
        cls.db.appmeta.find().count()
        pass

if __name__ == '__main__':
    s = datastatus()
    print "OK"
    while True :
        print s.content()
        #time.sleep(1)

    print "OK"
        
