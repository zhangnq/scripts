#!/bin/bash

#set localtime
cat >/etc/cron.daily/ntpdate <<EOF
#!/bin/bash
ntpdate ntp.ubuntu.com >>/var/log/ntpdate.log 2>&1
EOF
chmod +x /etc/cron.daily/ntpdate

#set default language
mv /etc/default/locale /etc/default/locale.`date "+%Y%m%d%H%M%S"`
cat >/etc/default/locale <<EOF
LANG="en_US.UTF-8"
LANGUAGE="en_US:en"
EOF
echo "en_US.UTF-8 UTF-8" >/var/lib/locales/supported.d/local

#Synchronization time
mv /etc/localtime /etc/localtime.bak
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

#iptables rules

iptables -F
iptables -X
iptables -Z
#允许本地回环
iptables -A INPUT -i lo -p all -j ACCEPT
#允许状态正常的数据包进入
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
#允许PING测试的数据包进出
iptables -A INPUT -p icmp -j ACCEPT
#允许22端口的数据进出
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
#add nrpe port
iptables -A INPUT -p tcp --dport 5666 -j ACCEPT
#add http https port
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT


iptables -P INPUT DROP
service iptables save
service iptables restart
iptables -t filter -L -n

#denyhost
wget https://raw.githubusercontent.com/zhangnq/scripts/master/bash/denyhost/setup.sh
bash setup.sh
