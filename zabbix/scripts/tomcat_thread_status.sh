#!/bin/bash

#### 添加sudo权限 ####
#zabbix ALL=(root) NOPASSWD:/etc/zabbix/custom/scripts/tomcat_thread_status.sh
#Defaults:zabbix   !requiretty
####

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin

tomcat_path=$1
user=$2

STATS=(NEW:0 RUNNABLE:0 BLOCKED:0 WAITING:0 TIMED_WAITING:0 TERMINATED:0 TOTAL:0)

pid=`ps -ef|grep "java .*$tomcat_path"|grep -v grep|awk '{print $2}'`
if [ $pid ];then
  STATUS=`su - $user -c "jstack $pid|grep -i \"java.lang.Thread.State:\""|awk '{print $2}'|sort|uniq -c|awk '{print $2":"$1}'`
fi

if [ ! -z "$STATUS" ];then
  total=0
  for s in $STATUS;do
    key=`echo $s|cut -d: -f1`
    val=`echo $s|cut -d: -f2`

    i=0
    for t in ${STATS[@]};do
      if [ `echo $t|grep -c $key` -eq 1 ];then
        idx=$i
        break
      fi
      let i=$i+1

    done

    STATS[$i]=${key}":"${val}

    let total=$total+${val}
  done
  STATS[6]="TOTAL:"${total}
fi

echo ${STATS[@]} | sed -e s/' '/',"'/g -e s/':'/'":'/g -e s/^/'{"thread_status":{"'/g -e s/'$'/'}}'/g
