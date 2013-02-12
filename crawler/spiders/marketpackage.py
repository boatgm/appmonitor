#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import urlparse
import os
import socket
import subprocess

from os import path
from md5 import md5

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from scrapy.http import Request
from crawler.settings import AAPT_PATH,STORE_PATH
from crawler.items import ApkItem
from crawler.urls import packages
from crawler.spiders import itunes,zhushou,waptw,anzhi,hiapk,google

class Spider(CrawlSpider):
    name = 'marketpackage'
    start_urls =[
            'http://zhushou.360.cn/',
            ]
    is_start = True

    def parse(self,response):

        if self.is_start :
            self.is_start = False
            for pkg in packages():
                self.download(pkg)

    def download(self,pkg):
        url = pkg['package_url']
        md5 = pkg['md5']
        market = pkg['market']
        category = pkg['category_general']

        store_path = STORE_PATH + '/marketcrawler/' + market + "/" + category + "/"
        store_name = str(pkg['app_id']) +"_"+ str(pkg['app_version'])+"_"+pkg['market']+'.apk'
        store_host = self.get_ip_address("eth0")
        apk_store_path = store_host+":"+store_path+store_name
        if not path.exists(store_path):
            os.makedirs(store_path)
        if not path.exists(store_path + store_name):
            if True:
            #try:
                command_wget = "wget "+url+" -O "+store_path+store_name
                print command_wget
                pkg_res = subprocess.Popen(command_wget,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                if path.exists(store_path + store_name):
                    item = ApkItem()
                    item['md5'] = md5
                    item['package_name'] = self.get_apk_pkg_name(store_path+store_name)
                    item['apk_store_path'] = apk_store_path
                    print item['package_name']
                    #return item

            #except Exception as E:
                #query={"app_id":item["app_id"],"app_version":item["app_version"],"market":item['market']}
                #self.appcontroller_dbutil.set_item_property(query,"status","")
                pass
        else:
            item = ApkItem()
            item['md5'] = md5
            item['package_name'] = self.get_apk_pkg_name(store_path+store_name)
            item['apk_store_path'] = apk_store_path
            print item['package_name']
            #return item

    def get_apk_pkg_name(self,apk_store_path):
        pkg_command = AAPT_PATH+'aapt dump badging '+ apk_store_path +" | sed -n \"s/.*package: name='\\([^']*\\).*/\\1/p\""
        print pkg_command
        pkg_res = subprocess.Popen(pkg_command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        pkg_name = pkg_res.stdout.read().strip()
        return pkg_name

    @staticmethod
    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("baidu.com", 80))
        res = s.getsockname()[0]
        s.close()
        return res
