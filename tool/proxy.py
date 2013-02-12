import os
import sys
import re
import requests
import time

proxy_file_name = 'proxys.txt'
lock = 'Checking'

class Proxy(object):
    current = 0
    proxy_dict = {}
    
    @classmethod
    def today(cls):
        return time.strftime("%Y-%m-%d", time.gmtime())
    
    @classmethod
    def crawl_proxy(cls):
        if os.path.exists(cls.today()):
            with open(cls.today()) as a_file:
                proxy_str = a_file.read().strip()
                if proxy_str:
                    proxy_list = proxy_str.split('\n')

                    cls.proxy_dict[cls.today()] = proxy_list
                    return

        cls.proxy_dict[cls.today()] = lock
        url = 'http://proxy.ipcn.org/proxylist.html'
        userAgent = 'iTunes/10.6.3 (Macintosh; Intel Mac OS X 10.8.1) AppleWebKit/536.25'
        headers = {"User-Agent": userAgent}
        try:
            r = requests.get(url, headers = headers)
            html = r.text
            result = re.findall(r'CN Proxy List, Powered by proxy.ipcn.org(.*?)</pre>', r.text, re.S)
            result= result[0].split('\n')[4:]
            print "crawled %d proxies" % len(result)
            
            ava_list = []
            for proxy in result:
                if cls.check_proxy(proxy):
                    ava_list.append(proxy)

            if len(ava_list) == 0:
                raise Exception('available proxy is empty')
            print "%d proxies is available" % len(ava_list)

            with open(cls.today(), 'w') as a_file:
                a_file.write('\n'.join(ava_list))

            cls.proxy_dict[cls.today()] = ava_list
            cls.current = 0
        except Exception, e:
            print 'update proxy list error'
            del cls.proxy_dict[cls.today()]

    @classmethod
    def check_proxy(cls, ip_port):
        try:
            print 'check: %s' % ip_port
            proxy = {'http': "http://%s/" % ip_port}

            res = requests.get('http://www.appchina.com/', timeout=5, proxies = proxy)
            print "%s available" % ip_port
            return True
        except Exception, e:

            print ("%s is not available" % ip_port)
            return False

    @classmethod
    def _get_available_proxy(cls):
        available_proxy_list = []
        with open(proxy_file_name) as a_file:
            for line in a_file:
                line = line.strip()
                if line.startswith('#'):
                    continue
                available_proxy_list.append(line)
        return available_proxy_list

    @classmethod
    def get_next_proxy(cls):
        if not cls.today() in cls.proxy_dict:
            cls.crawl_proxy()

        while cls.proxy_dict.get(cls.today()) == lock:
            time.sleep(3)

        proxy_list = cls.proxy_dict.get(cls.today())

        list_len = len(proxy_list)
        if list_len == 0:
            return None

        if cls.current >= list_len:
            cls.current %= list_len
        proxy = proxy_list[cls.current]
        cls.current += 1

        return proxy

if __name__ == '__main__':
    for i in range(10):
        print Proxy.get_next_proxy()
