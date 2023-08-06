# coding: utf-8

import sys
import re
import json
from optparse import OptionParser

from qiueer.python.cmds import cmds

def get_tomcat_list():
    cmdstr = "ps -ef|grep java|grep -v grep|grep \"Dcatalina.home\"|awk '{print $2 ,$(NF-3)}'|sed 's/-Dcatalina.home=//g'"
    c2 = cmds(cmdstr, timeout=3)
    stdo = c2.stdo()
    stde = c2.stde()
    # retcode = c2.code()
    
    (stdo_list, stde_list) = (re.split("\n", stdo), re.split("\n", stde))
    
    data = list()
    for tomcat in stdo_list:
        if not tomcat:continue
        data.append({
                     "{#TOMCAT_PID}":tomcat.split()[0],
                     "{#TOMCAT_PATH}": tomcat.split()[1],
                     "{#TOMCAT_NAME}":tomcat.split()[1].split('/')[-1],
                     })
    return json.dumps({'data': data}, sort_keys=True, indent=7, separators=(",",":"))

def main():
    try:
        usage = "usage: %prog [options]\ngGet Tomcat Stat"
        parser = OptionParser(usage)
        
        parser.add_option("-l", "--list",  
                          action="store_true", dest="is_list", default=False,  help="if list all tomcat")
        
        (options, args) = parser.parse_args()
        if 1 >= len(sys.argv):
            parser.print_help()
            return

        if options.is_list == True:
            print get_tomcat_list()
            return

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print tb

if __name__ == "__main__":
    main()

