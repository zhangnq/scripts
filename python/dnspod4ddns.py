#coding:utf-8
#author:zhangnq
#url:http://www.sijitao.net
#description:使用dnspod的api实现ddns的目的

import urllib2
import urllib
import json
import os
import datetime
 
username='xxx'
password='xxx'
type1='json'
domain_id='xxx'
record_id='xxx'

def MonitorRecordChange():
    #获取本地ip
    os.system('export PATH=$PATH;curl -o /tmp/ipinfo.txt http://ipinfo.io/ >/dev/null 2>&1')
    f=file('/tmp/ipinfo.txt','rb')
    localip=json.loads(f.read())['ip']
    f.close()

    #获取dnspod记录
    url='https://dnsapi.cn/Record.Info'
    values={
        'login_email':username,
        'login_password':password,
        'format':type1,
        'domain_id':domain_id,
        'record_id':record_id,
    }
    data=urllib.urlencode(values)
    req=urllib2.Request(url,data)
    req.add_header('User-Agent', 'NBHAO DDNS Client/1.0.0 (admin@nbhao.org) www.sijitao.net')
    response = urllib2.urlopen(req)
    recordip=json.loads(response.read())['record']['value']
    
    #修改记录
    if localip != recordip:
        url='https://dnsapi.cn/Record.Modify'
        values={
                'login_email':username,
                'login_password':password,
                'format':type1,
                'domain_id':domain_id,
                'record_id':record_id,
                'sub_domain':'sijitao.net',
                'value':localip,
                'record_type':'A',
                'record_line':'默认',
        }
        data=urllib.urlencode(values)
        req=urllib2.Request(url,data)
        req.add_header('User-Agent', 'NBHAO DDNS Client/1.0.0 (admin@nbhao.org) www.sijitao.net')
        try:
            response = urllib2.urlopen(req)
            print "Domain Record Change Successfully!%s --> %s" % (recordip,localip)
        except:
            print "Domain Record Change Failed!%s --> %s" % (recordip,localip)
    else:
        print "%s Domain Record Is Not Need To Change." % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
if __name__ == '__main__':
    MonitorRecordChange()
