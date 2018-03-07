#!/bin/bash

mkdir /swapfile
cd /swapfile
if [ ! -e /swapfile/swap ];then
  dd if=/dev/zero of=swap bs=1024 count=2000000
  mkswap -f swap
  echo "/swapfile/swap none swap defaults 0 0" >>/etc/fstab
fi

mount -a
swapon -a

free -m

