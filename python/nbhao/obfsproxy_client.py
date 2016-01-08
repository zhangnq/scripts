#coding:utf-8
#/usr/bin/env python

import cymysql
import Config
import os
import sys
import datetime

def start_obfsproxy_client():
    cur=conn.cursor()
    sql="select id,passwd,dport,sport from obfsproxy"
    cur.execute(sql)
    rows = []
    for r in cur.fetchall():
        rows.append(list(r))
    for row in rows:
        #add iptable rules
        cmd1="/sbin/iptables -L -n|grep dpt:%s|grep -v grep" % row[3]
        rc1=os.popen(cmd1).read()
        if not rc1:
            cmd2="/sbin/iptables -I INPUT -p tcp --dport %s -j ACCEPT;service iptables save;service iptables restart" % row[3]
            os.system(cmd2)

        #start obfsproxy client
        cmd="ps -ef|grep 'dest %s:%s'|grep -v grep" % (Config.S1,row[2])
        rc=os.popen(cmd).read()
        if rc:
            #pass
            print "%s: Sport %s is start" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),row[3])
        else:
            print "start the %s obfsproxy client process" % row[3]
            cmd="su - py27 -c 'nohup /home/py27/obfsproxy/obfsproxy.bin scramblesuit --dest %s:%s --password=%s client 0.0.0.0:%s >/dev/null 2>&1 &';" % (Config.S1,row[2],row[1],row[3])
            os.system(cmd)
    cur.close()

def check_obfsproxy_client():
    dport_list=[]
    cmd="ps -ef|grep python|grep '%s'|grep -v grep|awk '{print $12}'|cut -d: -f2" % Config.S1
    rc=os.popen(cmd).read()
    if rc:
        l=rc.split()
        for v in l:
            dport_list.append(v)

    cur=conn.cursor()
    for dport in dport_list:
        sql="select id,passwd,sport,dport from obfsproxy where dport=%s" % dport
        cur.execute(sql)
        rows=[]
        for r in cur.fetchall():
            rows.append(list(r))
        if len(rows) != 0:
            print "%s: Sport %s is ok." % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),rows[0][2])
        else:
            print "Kill obfsproxy client dport %s ..." % dport
            #kill process
            cmd="ps -ef|grep python|grep '%s:%s'|grep -v grep|awk '{print $2}'" % (Config.S1,dport)
            rc=os.popen(cmd).read()
            if rc:
                cmd="kill -9 %s" % rc.strip()
                os.system(cmd)

    cur.close()

if __name__ == "__main__":
    try:
        conn = cymysql.connect(host=Config.MYSQL_HOST, port=Config.MYSQL_PORT, user=Config.MYSQL_USER,
                               passwd=Config.MYSQL_PASS, db=Config.MYSQL_DB, charset='utf8', connect_timeout=60)
    except cymysql.err.OperationalError,e:
        print "Error: %s" % e
        sys.exit()
    except:
        print "Error: mysql connect error."
        sys.exit()

    #some functions
    start_obfsproxy_client()
    check_obfsproxy_client()

    conn.close()