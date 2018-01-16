#!/usr/bin/env python
#coding:utf-8

'''
说明：
1、PostgreSQL日志格式：
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,host=%h '
    %t = timestamp without milliseconds
    %p = process ID
    %l = session line number
    %u = user name
    %d = database name
    %h = remote host
2、host默认指定内网ip 192.168.0.0/16 ;
3、Blog：http://www.sijitao.net/ ;
'''

import sys
import re
import difflib
import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header

#if debug
debug=True
#pg log path
PGLOG='/data/pgsql/pg_log'
#email
EMAIL_POST = 25
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_HOST_USER = 'aa@qq.com'
EMAIL_HOST_PASSWORD = '123456'
SENDMAIL_FROM = '运维通知 <aa@qq.com>'
#脚本环境
ENV="正式"

if debug:
    pg_log_path=sys.argv[1]
    EMAIL_RECEIVERS=['admin@nbhao.org',]
else:
    import os
    cmd="ls -ltr %s/|tail -n 1|awk '{print $NF}'" % PGLOG
    filename=os.popen(cmd).read().strip()
    pg_log_path="%s/%s" % (PGLOG,filename)
    EMAIL_RECEIVERS=['admin@nbhao.org',]

def get_slow_query(pg_log):
    pg_log_file=file(pg_log,'rb')
    pattern=re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*user=(\w+).*db=(\w+).*host=(192\.168\.\d+\.\d+).*duration: (\d+\.\d+) ms.*: (.*)')
    #results=[]
    results_dict={}
    for line in pg_log_file:
        #result_dict={}
        l_str = line.strip()
        lists = pattern.findall(l_str)
        if len(lists) != 0:
            if results_dict.has_key(lists[0][2]):
                results_dict[lists[0][2]].append(lists[0][5])
            else:
                results_dict[lists[0][2]]=[]
                results_dict[lists[0][2]].append(lists[0][5])
            '''
            result_dict['datetime']=lists[0][0]
            result_dict['username']=lists[0][1]
            result_dict['database']=lists[0][2]
            result_dict['host']=lists[0][3]
            result_dict['time']=lists[0][4]
            result_dict['sql']=lists[0][5]
            results.append(lists[0][5])
            '''
    return results_dict

def remove_similar(lists,similarity=0.9):
    i=0
    l=len(lists)
    while i<l:
        j=i+1
        while j<l:
            seq=difflib.SequenceMatcher(None,lists[i],lists[j])
            ratio=seq.ratio()
            if ratio>=similarity:
                del lists[j]
                l=l-1
            else:
                j+=1
        i+=1
    return lists

def send_email(receiver,subject,msg):
    smtp = smtplib.SMTP()
    smtp.connect(EMAIL_HOST)
    smtp.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
    msg = MIMEText(msg,'html','utf-8')
    msg['Subject'] = Header(subject,'utf-8')
    msg['From'] = SENDMAIL_FROM
    if type(receiver) == type(""):
        msg['To']=receiver
    elif type(receiver) == type(u''):
        msg['To']=str(receiver)
    elif type(receiver) == type([]):
        msg['To']=', '.join(receiver)
    else:
        msg['To']=''
    smtp.sendmail(EMAIL_HOST_USER,receiver,msg.as_string())
    smtp.quit()

def main():
    results=get_slow_query(pg_log_path)
    for key,val in results.items():
        remove_similar(val, similarity=0.9)
        try:
            val.remove('COMMIT')
        except:
            pass
    msg=''
    for key,val in results.items():
        if len(val) != 0:
            msg=msg + '<b>DATABASE:</b> %s <br/>\n' % key
            i=1
            for r in val:
                msg=msg + str(i) + '、 ' + r + ' ; <br/>\n'
                i+=1
            msg=msg + '<br/>\n'

    #send email
    if len(msg) != 0:
        subject="%s PostgreSQL慢查询语句【 %s 】" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),ENV)
        send_email(EMAIL_RECEIVERS,subject,msg)
    else:
        print "Great,no slow query!"
    
if __name__ == "__main__":
    main()
