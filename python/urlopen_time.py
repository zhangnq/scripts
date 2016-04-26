#coding:utf-8

import socks
import socket
socket.socket = socks.socksocket
socket.setdefaulttimeout(30)
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "192.168.0.199", 7070)

import urllib2
import httplib
import time
import datetime
from threading import Thread
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='urlopen_time.log',
                    filemode='w')
logger = logging.getLogger()

def url_open(url,open_timeout=30):
    start_time = datetime.datetime.now()
    request_headers={
        'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        #'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        #'Accept-Encoding':"gzip, deflate, sdch",
        #'Accept-Language':"zh-CN,zh;q=0.8",
        #'Connection':'keep-alive',
        #'Referer':None,
    }
    req=urllib2.Request(url,None,request_headers)
    #req.add_header('User-Agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
    
    try:
        response=urllib2.urlopen(req,timeout=open_timeout)
        end_time = datetime.datetime.now()
        return_code=response.getcode()
    except urllib2.URLError as e:
        if hasattr(e, 'code'):
            return_code=e.code
        elif hasattr(e, 'reason'):
            return_code=500
        end_time = datetime.datetime.now()
    except httplib.BadStatusLine:
        return_code="unknown"
        end_time = datetime.datetime.now()
    except:
        return_code="timeout"
        end_time = datetime.datetime.now()
    
    interval = (end_time-start_time).microseconds / 1000 + (end_time-start_time).seconds * 1000
    msg = "%s\t%s\t%s\t%s\t%s" % (url,return_code,start_time,end_time,interval)
    print msg
    logger.info(msg)

def start_thread(url,thread_count=10,sleep_time=10):
    #print "Start: %s" % datetime.datetime.now()
    threads=[]
    i=0
    while i<thread_count:
        t=Thread(target=url_open,args=(url,))
        threads.append(t)
        i+=1
    for t in threads:
        t.setDaemon(True)
        t.start()
        time.sleep(sleep_time)

    for t in threads:
        t.join()

    #print "End: %s" % datetime.datetime.now()

if __name__ == "__main__":
    #url="http://www.voachinese.com/"
    url="http://download.chekiang.info/voachinese.html"
    
    while True:
        start_thread(url,thread_count=10,sleep_time=10)
