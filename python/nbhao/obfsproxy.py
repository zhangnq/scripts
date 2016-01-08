#!/usr/bin/python
#coding:utf-8

import cymysql
import Config
import string
import random
import sys
import os


def pull_db_all_user():
    cur = conn.cursor()
    cur.execute("SELECT port, u, d, transfer_enable, passwd, switch, enable FROM user")
    rows = []
    for r in cur.fetchall():
        rows.append(list(r))
    cur.close()
    return rows

def create_obfsproxy_port():
    users=pull_db_all_user()
    cur=conn.cursor()
    for user in users:
        #s=''.join(random.choice(string.ascii_uppercase) for x in range(25))+''.join(random.choice(string.digits) for x in range(7))
        s=''.join(random.choice(string.ascii_uppercase) for x in range(25))+'4343431'
        #l=list(s)
        #random.shuffle(l)
        #passwd=''
        #for r in l:
        #    passwd=passwd+r
        passwd=s
        dport=random.randint(3000,5000)
        sport=user[0]
        sql="select id from obfsproxy where sport=%s" %sport
        cur.execute(sql)
        r=cur.fetchone()
        if not r:
            sql="insert into obfsproxy(passwd,dport,sport) values('%s','%s','%s')" % (passwd,dport,sport)
            try:
                cur.execute(sql)
            except:
                print "dport %s may exist." % dport
                sys.exit()
    cur.close()

def start_obfsproxy():
    cur=conn.cursor()
    sql="select id,passwd,dport,sport from obfsproxy"
    cur.execute(sql)
    rows = []
    for r in cur.fetchall():
        rows.append(list(r))
    for row in rows:
        #add iptable rules
        cmd1="iptables -L -n|grep '%s.*dpt:%s'|grep -v grep" % (Config.S,row[2])
        rc1=os.popen(cmd1).read()
        if not rc1:
            cmd2="/sbin/iptables -I INPUT -p tcp -s %s --dport %s -j ACCEPT;service iptables save;service iptables restart" % (Config.S,row[2])
            os.system(cmd2)

        #start process
        cmd="ps -ef|grep 'dest=.*%s'|grep -v grep" % row[3]
        rc=os.popen(cmd).read()
        if rc:
            #pass
            print "sport %s is start" % row[3]
        else:
            print "start the %s obfsproxy process" % row[3]
            cmd="su - py27 -c 'obfsproxy --data-dir=/tmp/scramblesuit-server scramblesuit --password=%s --dest=127.0.0.1:%s server 0.0.0.0:%s >/dev/null 2>&1 &';" % (row[1],row[3],row[2])
            os.system(cmd)
    cur.close()

def check_obfsproxy():
    users=pull_db_all_user()
    sport_list=[]
    for user in users:
        sport_list.append(user[0])

    cur=conn.cursor()
    sql="select id,passwd,sport,dport from obfsproxy"
    cur.execute(sql)
    rows=[]
    for r in cur.fetchall():
        rows.append(list(r))

    for row in rows:
        if row[2] in sport_list:
            pass
            #print "sport %s is ok." % row[2]
        else:
            print "Delete sport %s ..." % row[2]
            #kill process
            cmd="ps -ef|grep python|grep 'dest=127.0.0.1:%s'|grep -v grep|awk '{print $2}'" % row[2]
            rc=os.popen(cmd).read()
            if rc:
                cmd="kill -9 %s" % rc.strip()
                os.system(cmd)

            #delete iptables rule
            cmd="/sbin/iptables -L -n --line-number|grep '%s.*dpt:%s'|grep -v grep|awk '{print $1}'" % (Config.S,row[3])
            rc=os.popen(cmd).read().strip()
            if rc:
                cmd="/sbin/iptables -D INPUT %s;service iptables save;service iptables restart" % rc
                os.system(cmd)

            #delete obfsproxy record from db
            sql="delete from obfsproxy where id=%s" % row[0]
            cur.execute(sql)

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
    create_obfsproxy_port()
    start_obfsproxy()
    check_obfsproxy()

    conn.close()
