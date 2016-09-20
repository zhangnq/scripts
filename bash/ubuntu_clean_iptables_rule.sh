#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
export LANG=en_US.UTF-8

echo `date` "Starting..."

ips=`iptables -L INPUT -n --line-number|grep ACCEPT|grep -v "dpt:22"|awk '{print $5}'`
ips2=`netstat -nt|grep tcp|grep -v grep |awk '{print $5}'|cut -d: -f1|sort|uniq`

#计算在线ip数
declare -i m=0

for ip2 in $ips2
do
  m=m+1
done

#比较iptables规则和在线ip
for ip in $ips
do
  declare -i i=0
  for ip2 in $ips2
  do
    if [ "$ip" == "$ip2" ];then
      break
    else
      i=i+1
    fi
  done

  #结果
  if [ $i -eq $m ];then
    echo -n "$ip is not online,start to delete iptables rules..."
    id=`iptables -L -n --line-number|grep "$ip"|awk '{print $1}'|head -n 1`;iptables -D INPUT $id;iptables-save >/etc/iptables/rules
    if [ $? -eq 0 ];then
      echo "successfully"
    fi
  else
    echo "$ip is online..."
  fi

done

echo `date` "end."