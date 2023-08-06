#!/bin/bash

STATS=(UNKNOWN:0 ESTABLISHED:0 SYN_SENT:0 SYN_RECV:0 FIN_WAIT1:0 FIN_WAIT2:0 TIME_WAIT:0 CLOSED:0 CLOSE_WAIT:0 LAST_ACK:0 LISTEN:0 CLOSING:0)
CONN="$(awk '{print $4}' /proc/net/tcp /proc/net/tcp6 | grep -v st | sort | uniq -c | sed -e s/' 0'/' '/g -e s/'A'/'10'/g -e s/'B'/'11'/g | awk '{print $2":"$1}')"

if [ ! -z "$CONN" ];then
    for s in $CONN
    do
        STATS[${s%%:*}]=${STATS[${s%%:*}]%%:*}":"${s#*:}
    done
fi
echo ${STATS[@]} | sed -e s/' '/',"'/g -e s/':'/'":'/g -e s/^/'{"tcp_conn":{"'/g -e s/'WAIT_'/'WAIT'/g -e s/'$'/'}}'/g
