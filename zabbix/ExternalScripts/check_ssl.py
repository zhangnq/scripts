#!/usr/bin/env python
#coding: utf-8
#Author: zhangnq
#Blog: https://zhangnq.com/

import requests
import argparse
import time

url = 'https://api.nbhao.org/v1/ssl/cert'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="check ssl expire time.")
    parser.add_argument("-H", dest="host", help="https hostname")
    parser.add_argument("-P", dest="port", default=443, help="https port ,default 443")
    args = parser.parse_args()
    
    try:
        resp = requests.get(url = url, params={"host":args.host,"port":args.port})
        result = resp.json()
    except:
        result = dict()
    
    if result:
        if result['code'] == 200:
            tm_end = result['message']['te']
            # 返回剩余的天数
            print (tm_end - int(time.time()))/86400
        else:
            print "error"
    else:
        print "error"
