#!/bin/bash

cd /root/
wget -c http://download.chekiang.info/gongju/DenyHosts-2.6.tar.gz
tar zxvf DenyHosts-2.6.tar.gz

cd DenyHosts-2.6
python setup.py install

cd /usr/share/denyhosts/
wget -c https://raw.githubusercontent.com/zhangnq/scripts/master/bash/denyhost/denyhosts.cfg
cp daemon-control-dist daemon-control
chown root daemon-control
chmod 700 daemon-control

echo "/usr/share/denyhosts/daemon-control start" >> /etc/rc.local

./daemon-control start
