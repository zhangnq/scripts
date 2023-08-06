#!/usr/bin/env python
#coding: utf-8

import redis
import time
import argparse


def connect(host, port, password=None):
    try:
        if password:
            r = redis.StrictRedis(host=host, port=port, password=password)
        else:
            r = redis.StrictRedis(host=host, port=port)
        return r
    except Exception as e:
        #print e
        return False


def get_random_key(r):
    return r.randomkey()


def get_value_timecost(r, key):
    t1 = time.time()
    value = r.get(key)
    t2 = time.time()
    return (t2 - t1) * 1000


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="get redis key time.")
    parser.add_argument("-H", dest="host", help="redis hostname or ip")
    parser.add_argument("-P", dest="port", default=6379, help="redis port default 6379")
    parser.add_argument("-p", dest="password", default=None, help="redis password default None")
    args = parser.parse_args()

    try:
        r = connect(args.host, args.port, args.password)
        t1 = time.time()
        key = get_random_key(r)
        t2 = time.time()
        key_type = r.type(key)
        if key_type == 'string':
            print get_value_timecost(r, key)
        else:
            print (t2 - t1) * 1000
    except Exception as e:
        print 1000

