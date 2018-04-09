# -*- coding: utf-8 -*-
'''
author: zhangnq
website: http://www.sijitao.net/
'''

import requests
import cookielib
import re
import random
import time
import datetime


#http代理配置，有用户名和密码。
proxie = { 
    'http' : 'http://username:password@www.sijitao.net:1080'
}
#配置hostloc论坛的用户名密码
users=[
    {'username':'user1','password':'password1'},
    {'username':'user2','password':'password2'},
]


agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
headers = {
    "Host": "www.hostloc.com",
    "Referer": "http://www.hostloc.com/forum.php",
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")

def is_login():
    url='http://www.hostloc.com/home.php?mod=spacecp'
    html=session.get(url, headers=headers, allow_redirects=False,proxies = proxie).text
    pattern=r'<div id="messagelogin"></div>'
    result=re.search(pattern, html)
    if result:
        return False
    else:
        return True
    
def login(username,password):
    print("start to login...")
    post_url = 'http://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes'
    postdata = {
        'username': username,
        'password': password,
        'checkbox':'on',
    }
    
    login_page = session.post(post_url, data=postdata, headers=headers,proxies = proxie)
    
    if login_page.status_code == 200:
        session.cookies.save()
        if is_login():
            print("login successfully...")
            return True
        else:
            return False
    else:
        return False

def visit_space(username,password):
    print("start to visit space...")
    urls=[]
    for i in range(10):
        url='http://www.hostloc.com/space-uid-%s.html' % random.randint(4000,25000)
        urls.append(url)
    if not is_login():
        login(username,password)
    
    for url in urls:
        code=session.get(url,headers=headers,proxies = proxie).status_code
        print("%s --> %s" % (url,code))
        time.sleep(5)

def logout():
    print("start to logout...")
    url='http://www.hostloc.com/forum.php'
    html=session.get(url,headers=headers,proxies = proxie).text
    pattern=r'name="formhash" value="(.*)"'
    result=re.findall(pattern,html)
    
    logout_url='http://www.hostloc.com/member.php?mod=logging&action=logout&formhash=%s' % result[0]
    logout_code=session.get(logout_url, headers=headers,proxies = proxie).status_code
    if logout_code == 200:
        print("logout successfully.")
    else:
        print("logout failed.")

def main():
    print(datetime.datetime.now())
    
    for user_dict in users:
        #login
        login(user_dict['username'],user_dict['password'])
        #visit space
        visit_space(user_dict['username'],user_dict['password'])
        #logout
        logout()

if __name__ == "__main__":
    main()

