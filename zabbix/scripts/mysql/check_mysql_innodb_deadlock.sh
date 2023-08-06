#!/bin/bash
# 通过show engine innodb status监测死锁deadlock

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin:/usr/local/ruby/bin

# mysql zabbix密码
# password='123456'
source /etc/zabbix/custom/public/zabbix/.mysql_zabbix.passwd

host='192.168.1.21'
user='zabbix'

# check 3 hours
offset=10800

mysql -u${user} -p${password} -h${host} -e "show engine innodb status\G" >/tmp/mysql_master_innodb_status.txt

t=`grep -A 2 -i "LATEST DETECTED DEADLOCK" /tmp/mysql_master_innodb_status.txt|tail -n 1|awk '{print $1,$2}'`
rm -f /tmp/mysql_master_innodb_status.txt

if [ "$t"x = ""x ];then 
  echo 0
  exit 0
fi

ts1=`date +"%s"`
ts2=`date -d "$t" +"%s"`

i=0
let i=ts1-ts2
if [ $i -lt $offset ];then
  echo 1
  exit 1
fi

echo 0
exit 0