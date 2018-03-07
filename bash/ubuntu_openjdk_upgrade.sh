#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

email="admin@nbhao.org"

#send email
sendEmail(){
  curl -X POST \
  --data-urlencode "token=mytoken" \
  --data-urlencode "subject=$1" \
  --data-urlencode "content=$2" \
  --data-urlencode "email=$3" \
  http://www.nbhao.org/api/email/send
}

#first check
version=`/usr/bin/java -version 2>&1`
res=$?
if [ $res -ne 0 ];then
  sub="get java version error."
  ip=`/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`
  msg="IP: $ip"
  sendEmail "$sub" "$msg" "$email"
  exit 1
fi

count=`echo $version|grep '1.8.0_'|grep -v grep|wc -l`
if [ $res -eq 0 -a $count -eq 1 ];then
  echo "jdk 1.8 is installed,exit."
  exit 0
fi

#start to upgrade
apt-get update
apt-get install curl -y
apt-get install software-properties-common -y

add-apt-repository ppa:openjdk-r/ppa -y
apt-get update
apt-get install openjdk-8-jdk -y --force-yes
update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
update-alternatives --set javac /usr/lib/jvm/java-8-openjdk-amd64/bin/javac
update-alternatives --set jps /usr/lib/jvm/java-8-openjdk-amd64/bin/jps
update-alternatives --set jstack /usr/lib/jvm/java-8-openjdk-amd64/bin/jstack

#last check
ip=`/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`
version=`/usr/bin/java -version 2>&1`
res=$?
if [ $res -ne 0 ];then
  sub="get java version error."
  msg="IP: $ip"
  sendEmail "$sub" "$msg" "$email"
  exit 1
fi
count=`echo $version|grep '1.8.0_'|grep -v grep|wc -l`
if [ $res -eq 0 -a $count -ne 1 ];then
  sub="upgrade java error."
  msg="IP: $ip"
  sendEmail "$sub" "$msg" "$email"
  exit 1
fi
