#!/usr/bin/env python
# @Author: zhangnq
# @Blog: https://zhangnq.com/
# @Tool: http://tool.sijitao.net/software/tcping

import socket,sys
import time
import argparse
from argparse import RawTextHelpFormatter

VERSION = '1.0.1'

ping_cnt = 0
ping_success_cnt = 0
ping_fail_cnt = 0
ping_resp_min = 0
ping_resp_max = 0
ping_resp_avg = 0
ping_resp_total = 0

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

# get ip from hostname
def host2ip(host):
    try:
        return socket.gethostbyname(host)
    except Exception:
        return False

# probing tcp port
def tcp(ip, port, timeout=2):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(timeout)
    try:
        t1 = time.time()
        sk.connect((ip, port))
        t2 = time.time()
        sk.close()
        return True, int(round((t2-t1)*1000))
    except Exception:
        sk.close()
        return False, timeout*1000

def format_tcp_result(results):
    if results[0]:
        return "Probing {}:{}/tcp - Port is open - time={}ms".format(ip, port, results[1])
    else:
        return "Probing {}:{}/tcp - No response - time={}ms".format(ip, port, results[1])

def statistic_tcp_result(results):
    global ping_cnt
    global ping_success_cnt
    global ping_fail_cnt
    global ping_resp_min
    global ping_resp_max
    global ping_resp_avg
    global ping_resp_total
    # total count
    ping_cnt += 1
    if results[0]:
        # success count
        ping_success_cnt += 1
        # min ping response time
        if ping_resp_min == 0:
            ping_resp_min = results[1]
        elif results[1] < ping_resp_min:
            ping_resp_min = results[1]
        # max ping respose time
        if results[1] > ping_resp_max:
            ping_resp_max = results[1]
        # average ping response time
        ping_resp_avg = round((ping_resp_total + results[1]) / float(ping_success_cnt), 3)
        ping_resp_total += results[1]
    else:
        # fail count
        ping_fail_cnt += 1
    
    return ping_cnt, ping_success_cnt, ping_fail_cnt, ping_resp_min, ping_resp_max, ping_resp_avg

if __name__ == "__main__":
    desc = '''--------------------------------------------------------------------------
tcping for linux by zhangnq
Please see http://tool.sijitao.net/software/tcping for more introductions.
--------------------------------------------------------------------------'''
    
    example_text = '''examples:
    tcping zhangnq.com
    tcping 114.114.114.114 -t -p 53
    tcping zhangnq.com -n 10 -p 443 -i 5 -w 1
    \n
'''
    
    parser=MyParser(description=desc, formatter_class=RawTextHelpFormatter, epilog=example_text)
    parser.add_argument("destination", type=str, help="a DNS name, an IP address")
    parser.add_argument("-p", dest="port", type=int, default=80, help="a numeric TCP port, 1-65535. If not specified, defaults to 80.")
    parser.add_argument("-t", dest="is_continuously", action='store_true', help="ping continuously until stopped via control-c.")
    parser.add_argument("-n", dest="number", type=int, default=4, help="send count pings and then stop, default 4.")
    parser.add_argument("-i", dest="interval", type=int, default=1, help="wait seconds between pings, default 1.")
    parser.add_argument("-w", dest="wait", type=int, default=2, help="wait seconds for a response, default 2.")
    parser.add_argument("-v", "--version", action='version', version=VERSION,  help="print version and exit.")
    args=parser.parse_args()
    
    ip = host2ip(args.destination)
    port = args.port
    if not ip:
        print("ERROR: Could not find host - %s, aborting" % args.destination)
        sys.exit(1)
    
    try:
        # continuously
        if args.is_continuously:
            print("")
            print("** Pinging continuously.  Press control-c to stop **")
            print("")
            while True:
                results = tcp(ip, port, args.wait)
                # print format result
                print(format_tcp_result(results))
                # start statistic
                statistic_tcp_result(results)
                
                time.sleep(args.interval)
        else:
            print("")
            for i in range(args.number):
                results = tcp(ip, port, args.wait)
                # print format result
                print(format_tcp_result(results))
                # start statistic
                statistic_tcp_result(results)
                
                time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Control-C")
    finally:
        format_statistic_results = '''
Ping statistics for {}, port {}:
    Probes: send = {}, success = {}, fail = {} ({}% fail)
Approximate trip times:
    Minimum = {}ms, Maximum = {}ms, Average = {}ms
'''.format(ip, port, ping_cnt, ping_success_cnt, ping_fail_cnt,round(ping_fail_cnt/float(ping_cnt)*100,2), ping_resp_min, ping_resp_max, ping_resp_avg)
        print(format_statistic_results)
