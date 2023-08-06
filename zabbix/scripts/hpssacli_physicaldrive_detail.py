# coding: utf-8

import sys
import re
import json
from optparse import OptionParser

from qiueer.python.cmds import cmds

#### 添加sudo权限 ####
#zabbix ALL=(root) NOPASSWD:/usr/sbin/hpssacli
#Defaults:zabbix   !requiretty
####
# hpssacli安装：https://zhangnq.com/3267.html

def get_pd_list(slot):
    cmdstr = "sudo /usr/sbin/hpssacli controller slot={} physicaldrive all show detail|grep physicaldrive".format(slot)
    c2 = cmds(cmdstr, timeout=5)
    stdo = c2.stdo()
    stde = c2.stde()
    # retcode = c2.code()
    
    (stdo_list, stde_list) = (re.split("\n", stdo), re.split("\n", stde))
    
    data = list()
    for pd in stdo_list:
        if not pd:continue
        data.append({
                     "{#DRIVE}": pd.split()[1],
                     })
    return json.dumps({'data': data}, sort_keys=True, indent=7, separators=(",",":"))

def get_pd_detail(slot, drive, parameter):
    cmdstr = "sudo /usr/sbin/hpssacli controller slot={} physicaldrive all show detail|grep -i -A 21 'physicaldrive {}'|grep -i '{}'".format(slot, drive, parameter)
    c2 = cmds(cmdstr, timeout=5)
    stdo = c2.stdo()
    stde = c2.stde()
    (stdo_list, stde_list) = (re.split("\n", stdo), re.split("\n", stde))

    return stdo_list[0].split(':')[-1].strip()

def main():
    try:
        usage = "usage: %prog [options]\ngHP Smart Array PhysicalDrive Show"
        parser = OptionParser(usage)
        
        parser.add_option("-l", "--list",  
                          action="store_true", dest="is_list", default=False,  help="if list all physical drive")
        parser.add_option("-S", "--slot", action="store", type="string", dest="slot", default=0)
        parser.add_option("-P", "--physical", action="store", type="string", dest="physical", default=None)
        parser.add_option("-p", "--parameter", action="store", type="string", dest="parameter", default=None)
        
        (options, args) = parser.parse_args()
        if 1 >= len(sys.argv):
            parser.print_help()
            return

        if options.is_list == True:
            print get_pd_list(options.slot)
            return

        if options.physical and options.parameter:
            print get_pd_detail(options.slot, options.physical, options.parameter) 
            return

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print tb

if __name__ == "__main__":
    main()
