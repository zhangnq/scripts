import json
from erl_terms import decode
from os import getuid
from re import sub
from subprocess import check_output

'''
zabbix 增加sudo权限
例如：
zabbix ALL=(root) NOPASSWD:/usr/sbin/rabbitmqctl
Defaults:zabbix   !requiretty
'''

check_command = ['/usr/sbin/rabbitmqctl', '-q', 'status']

if getuid() != 0:
    check_command.insert(0, '/usr/bin/sudo')
status = check_output(check_command)

status = ''.join(status.splitlines()) + '.'
status = sub('(?:\\\\n)+', '',  status)

status = decode(status)

#print status


status_dict = dict()
for item in status[0]:
    key = item[0]
    val = item[1]

    if key == 'running_applications':
        continue

    #print key, val
    if type(val) == type(list()):
        d_tmp = dict()
        for v in val:
            d_tmp[v[0]] = v[1]

        status_dict[key] = d_tmp
    else:
        status_dict[key] = val

print json.dumps(status_dict)
