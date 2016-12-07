#!/bin/bash

export PATH="$PATH:/sbin"

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

#nagios nrpe port
iptables -A INPUT -p tcp --dport 5666 -j ACCEPT

#http https server
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

iptables -P INPUT DROP

mkdir -pv /etc/iptables
iptables-save >/etc/iptables/rules
echo "pre-up /sbin/iptables-restore < /etc/iptables/rules" >>/etc/network/interfaces
iptables -t filter -L -n

