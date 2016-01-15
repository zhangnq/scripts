#!/bin/sh

export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

URL=http://www.chekiang.info/scan/html/zhangnq_sshbl_deny.tar.gz
HOSTSDENY=/etc/hosts.deny
TMP_DIR=/dev/shm
FILE=hosts.deny

cd $TMP_DIR

curl $URL 2> /dev/null | tar zx
cat zhangnq_sshbl_deny.txt >$FILE

LINES=`grep "^sshd:" $FILE | wc -l`

if [ $LINES -gt 10 ]
then
sed -i '/^####SSH BlackList START BY Zhangnq####/,/^####SSH BlackList END BY Zhangnq####/d' $HOSTSDENY
echo "####SSH BlackList START BY Zhangnq####" >> $HOSTSDENY
cat $FILE >> $HOSTSDENY
echo "####SSH BlackList END BY Zhangnq####" >> $HOSTSDENY
fi