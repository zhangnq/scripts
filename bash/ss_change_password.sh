#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

newpass=$1

if [ ! $newpass ];then
  echo "Please input new password."
  exit 2
fi

sed -i "s@\"password\":\".*\"@\"password\":\"`echo $newpass`\"@g" /etc/shadowsocks/config.json

/etc/init.d/shadowsocks restart

