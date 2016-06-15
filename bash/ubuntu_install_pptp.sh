#!/bin/bash

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

clear
CUR_DIR=$(pwd)

if [ $(id -u) != "0" ]; then
    printf "Error: You must be root to run this script!"
    exit 1
fi

echo "#############################################################"
echo "# PPTP VPN Auto Install"
echo "# Env: Debian/Ubuntu"
echo "# Version: 1.0"
echo "# Author: zhangnq"
echo "# Blog: http://www.sijitao.net/"
echo "#############################################################"
echo ""

apt-get -y update
apt-get -y install pptpd

cat >>/etc/pptpd.conf<<EOF
localip 10.10.10.1
remoteip 10.10.10.2-254
EOF

cp /etc/ppp/pptpd-options /etc/ppp/pptpd-options.old

cat >/etc/ppp/pptpd-options<<EOF
name pptpd
refuse-pap
refuse-chap
refuse-mschap
require-mschap-v2
require-mppe-128
ms-dns 223.5.5.5
ms-dns 114.114.114.114
proxyarp
debug
dump
lock
nobsdcomp
novj
novjccomp
logfile /var/log/pptpd.log
EOF

cat >>/etc/ppp/chap-secrets<<EOF
test pptpd 123456 *
EOF

sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g' /etc/sysctl.conf
sysctl -p

iptables-save > /etc/iptables.down.rules

iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 1723 -j ACCEPT
iptables -A INPUT -p gre -j ACCEPT
iptables -t nat -A POSTROUTING -s 10.0.0.0/8 -j MASQUERADE
iptables -A FORWARD -s 10.0.0.0/8 -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --set-mss 1200
#iptables -I FORWARD -p tcp --syn -i ppp+ -j TCPMSS --set-mss 1300

iptables-save > /etc/iptables.up.rules

cat >>/etc/network/interfaces<<EOF
pre-up iptables-restore < /etc/iptables.up.rules
post-down iptables-restore < /etc/iptables.down.rules
EOF

/etc/init.d/pptpd restart
