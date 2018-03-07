#!/bin/bash
#upgrade oracle jdk to 1.8

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
if [ ! -d /usr/lib/jvm ];then mkdir -pv /usr/lib/jvm/ ;fi
wget http://nb.cyyun.com:18104/software/Java/jdk-8u121-linux-x64.tar.gz -O /tmp/jdk-8u121-linux-x64.tar.gz
tar zxf /tmp/jdk-8u121-linux-x64.tar.gz -C /usr/lib/jvm/

update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.8.0_121/bin/java" 1
update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk1.8.0_121/bin/javac" 1
update-alternatives --install "/usr/bin/jps" "jps" "/usr/lib/jvm/jdk1.8.0_121/bin/jps" 1
update-alternatives --install "/usr/bin/jstack" "jstack" "/usr/lib/jvm/jdk1.8.0_121/bin/jstack" 1
update-alternatives --set java /usr/lib/jvm/jdk1.8.0_121/bin/java
update-alternatives --set javac /usr/lib/jvm/jdk1.8.0_121/bin/javac
update-alternatives --set jps /usr/lib/jvm/jdk1.8.0_121/bin/jps
update-alternatives --set jstack /usr/lib/jvm/jdk1.8.0_121/bin/jstack

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
