#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

left=`crontab -l 2>/dev/null|grep check_nbhao_org`

if [ ! "$left" ];then
    (crontab -l 2>/dev/null;echo "10 * * * * /bin/bash /opt/apps/check_nbhao_org")|crontab -
fi
