#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

host='http://nb.cyyun.com:18104'

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script."
    exit 1
fi

echo "============================install dependency=================================="

cur_dir=$(pwd)
cd $cur_dir

echo "============================check files=================================="

sleep 5

if [ -s jdk-7u45-linux-x64.tar.gz ]; then
  echo "jdk [found]"
  else
  wget -c $host/software/Java/jdk-7u45-linux-x64.tar.gz
fi

echo "============================jdk install================================="

sleep 5

cd $cur_dir

tar zxvf jdk-7u45-linux-x64.tar.gz
if [ $(grep -c jvm /usr/lib/) -eq 0 ];then
        mkdir -p /usr/lib/jvm
fi

mv jdk1.7.0_45 /usr/lib/jvm/

cat >>/etc/profile<<"eof"
JAVA_HOME=/usr/lib/jvm/jdk1.7.0_45
export PATH="$PATH:$JAVA_HOME/bin"
eof

source /etc/profile

java -version

