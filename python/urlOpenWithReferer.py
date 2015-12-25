#coding:utf-8
#伪装referer访问指定网站

import urllib2

def visitWebsite(url,timeout=60):
    req=urllib2.Request(url)
    req.add_header('Referer', 'http://www.sijitao.net/')
    req.add_header('User-Agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
    
    try:
        response=urllib2.urlopen(req,timeout=timeout)
        print "Url: %s\t%s" % (url,response.getcode())
    except urllib2.URLError as e:
        if hasattr(e, 'code'):
            print "Url: %s\t%s" % (url,e.code)
        elif hasattr(e, 'reason'):
            print "Url: %s\t%s" % (url,'error')
    except:
        pass
    finally:
        if response:
            response.close()

if __name__ == '__main__':
    urls=[
        'http://zgboke.com/',
        'http://114.vprol.com/',
    ]
    for url in urls:
        visitWebsite(url)
