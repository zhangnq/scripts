#coding:utf-8
#/usr/bin/env python

import cymysql
import Config
import os
import sys
import datetime

def addPort():
    cur=conn.cursor()
    sql="select id,port from user"
    #sql="select 12812,10009 from user"
    cur.execute(sql)
    rows = []
    for r in cur.fetchall():
        rows.append(list(r))
    for row in rows:
        #add iptable rules
        cmd1="/sbin/iptables -L -n|grep dpt:%s|grep -v grep" % row[1]
        rc1=os.popen(cmd1).read()
        if not rc1:
            cmd2="/sbin/iptables -I INPUT -p tcp --dport %s -j ACCEPT;service iptables save;service iptables restart" % row[1]
            os.system(cmd2)

        #add port to haproxy.cfg
        content='''
#ss %s start
frontend ss-in-%s
        bind *:%s
        default_backend ss-out-%s
backend ss-out-%s
        balance source
        server server1 %s:%s maxconn 20480
        server server2 %s:%s maxconn 20480
#ss %s end
        ''' % (row[1],row[1],row[1],row[1],row[1],Config.S1,row[1],Config.S2,row[1],row[1])

        cmd3="/bin/grep %s /etc/haproxy/haproxy.cfg" % row[1]
        rc3=os.popen(cmd3).read()
        if not rc3:
            cmd4='''
/bin/cat >> /etc/haproxy/haproxy.cfg << "EOF"
%s
EOF
/etc/init.d/haproxy restart
            ''' % content
            os.system(cmd4)

    cur.close()

def checkPort():
    dport_list=[]
    cmd="/bin/grep '#ss.*start' /etc/haproxy/haproxy.cfg|awk '{print $2}'"
    rc=os.popen(cmd).read()
    if rc:
        l=rc.split()
        for v in l:
            dport_list.append(v)

    cur=conn.cursor()
    for dport in dport_list:
        sql="select id,port from user where port=%s" % dport
        cur.execute(sql)
        rows=[]
        for r in cur.fetchall():
            rows.append(list(r))
        if len(rows) != 0:
            print "%s: Port %s is ok." % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),rows[0][1])
        else:
            print "Delete haproxy port %s ..." % dport
            #delete port
            cmd="/sbin/iptables -L -n --line-number|grep 'dpt:%s'|grep -v grep|awk '{print $1}'" % dport
            rc=os.popen(cmd).read()
            if rc:
                cmd="/sbin/iptables -D INPUT %s;service iptables save;service iptables restart" % rc.strip()
                os.system(cmd)
            cmd="/bin/sed -i '/^#ss %s start/,/^#ss %s end/d' /etc/haproxy/haproxy.cfg;/etc/init.d/haproxy restart" % (dport,dport)
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
    addPort()
    checkPort()

    conn.close()
