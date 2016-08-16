#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

apt-get update
apt-get -y install python-pip
apt-get install python-setuptools
pip install shadowsocks
mkdir -pv /etc/shadowsocks

cat > /etc/shadowsocks/config.json<<EOF
{
    "server":"0.0.0.0",
    "server_port":443,
    "local_address": "127.0.0.1",
    "local_port":7070,
    "password":"passw0rd",
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":false,
    "workers":3
}
EOF

cat >> /etc/sysctl.conf << EOF
#
#shadowsocks
# max open files
fs.file-max = 51200
# max read buffer
net.core.rmem_max = 67108864
# max write buffer
net.core.wmem_max = 67108864
# default read buffer
net.core.rmem_default = 65536
# default write buffer
net.core.wmem_default = 65536
# max processor input queue
net.core.netdev_max_backlog = 4096
# max backlog
net.core.somaxconn = 4096

# resist SYN flood attacks
net.ipv4.tcp_syncookies = 1
# reuse timewait sockets when safe
net.ipv4.tcp_tw_reuse = 1
# turn off fast timewait sockets recycling
net.ipv4.tcp_tw_recycle = 0
# short FIN timeout
net.ipv4.tcp_fin_timeout = 30
# short keepalive time
net.ipv4.tcp_keepalive_time = 1200
# outbound port range
net.ipv4.ip_local_port_range = 10000 65000
# max SYN backlog
net.ipv4.tcp_max_syn_backlog = 4096
# max timewait sockets held by system simultaneously
net.ipv4.tcp_max_tw_buckets = 5000
# turn on TCP Fast Open on both client and server side
net.ipv4.tcp_fastopen = 3
# TCP receive buffer
net.ipv4.tcp_rmem = 4096 87380 67108864
# TCP write buffer
net.ipv4.tcp_wmem = 4096 65536 67108864
# turn on path MTU discovery
net.ipv4.tcp_mtu_probing = 1

# for high-latency network
net.ipv4.tcp_congestion_control = hybla

# for low-latency network, use cubic instead
# net.ipv4.tcp_congestion_control = cubic
EOF

sysctl -p

cnt=`grep -c "/usr/local/bin/ssserver -c /etc/shadowsocks/config.json -d start" /etc/rc.local`
if [ $cnt -eq 0 ];then
	sed -i '/.*exit 0.*/i\/usr/local/bin/ssserver -c /etc/shadowsocks/config.json -d start' /etc/rc.local
fi

#start
/usr/local/bin/ssserver -c /etc/shadowsocks/config.json -d start
