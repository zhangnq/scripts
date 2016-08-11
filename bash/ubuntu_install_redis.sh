#!/bin/bash

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script."
    exit 1
fi

apt-get update
apt-get autoremove -y
apt-get install -y build-essential gcc g++ make zlibc zlib1g zlib1g-dev

cd /root
#download
wget http://download.redis.io/releases/redis-3.2.3.tar.gz
tar zxvf redis-3.2.3.tar.gz
cd redis-3.2.3/
make
if [ $? -ne 0 ];then
    echo "Make redis source error."
    exit 1
fi

#add redis user group
groupadd redis
useradd -g redis redis
#make dirs
mkdir -pv /usr/local/redis
mkdir -pv /usr/local/redis/bin
mkdir -pv /usr/local/redis/conf
mkdir -pv /usr/local/redis/logs
chown -R redis:redis /usr/local/redis
#copy files
cd src
cp redis-benchmark redis-check-aof redis-cli redis-server /usr/local/redis/bin
cd ..
cp redis.conf /usr/local/redis/conf

cat >>/etc/profile<<eof
export PATH=/usr/local/redis/bin:\$PATH
eof
source /etc/profile
#modify redis.conf
sed -i "s@bind 127.0.0.1@bind 0.0.0.0@g" /usr/local/redis/conf/redis.conf
sed -i "s@daemonize no@daemonize yes@g" /usr/local/redis/conf/redis.conf
sed -i "s@redis_6379.pid@redis.pid@g" /usr/local/redis/conf/redis.conf
sed -i "s@logfile \"\"@logfile \"/usr/local/redis/logs/redis.log\"@g" /usr/local/redis/conf/redis.conf
sed -i "s@dir ./@dir /usr/local/redis@g" /usr/local/redis/conf/redis.conf
#
echo "vm.overcommit_memory=1" >> /etc/sysctl.conf
sysctl -p
echo never > /sys/kernel/mm/transparent_hugepage/enabled
sed -i '/.*exit 0.*/i\echo never > /sys/kernel/mm/transparent_hugepage/enabled' /etc/rc.local
#init scripts
wget https://raw.githubusercontent.com/zhangnq/scripts/master/bash/service/redis-server -O /etc/init.d/redis-server
chmod +x /etc/init.d/redis-server
update-rc.d redis-server defaults

#end
/etc/init.d/redis-server start
ps -ef|grep redis
