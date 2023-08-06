# coding: utf-8

import requests
import sys
from optparse import OptionParser


def main():
    script_name = sys.argv[0]
    usage = "usage: python {0} [options]".format(script_name)
    parser = OptionParser(usage)

    parser.add_option("-i", "--iphost", action="store", dest="iphost", type="string", default='localhost',
                      help="iphost")
    parser.add_option("-p", "--port", action="store", dest="port", type="string", default=80, help="port")
    parser.add_option("-k", "--key", action="store", dest="key", type="string", default='taskmanagers',
                      help="which key to fetch")

    (options, args) = parser.parse_args()

    iphost = options.iphost
    port = options.port
    key = options.key

    url = "http://{0}:{1}/overview".format(iphost, port)

    try:
        resp = requests.get(url)
        res = resp.json()

        if not key or not iphost or not port:
            parser.print_help()
            return

        value = res[key]
        print value
    except Exception as expt:
        import traceback
        tb = traceback.format_exc()
        print tb

if __name__ == '__main__':
    main()
