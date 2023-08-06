#!/usr/bin/env python
# coding: utf-8

import pymongo
import time
import argparse


# mongo连接
def mongo_connect(host, port, username, password, authsource='admin'):
    if not username and not password:
        client = pymongo.MongoClient(host, port)
    else:
        client = pymongo.MongoClient(host, port, username=username, password=password, authSource=authsource)

    return client

def mongo_replica_connect(hosts, username, password, authsource='admin', replicaset=''):
    if not username and not password:
        if replicaset:
            client = pymongo.MongoClient(hosts, replicaset=replicaset)
        else:
            client = pymongo.MongoClient(hosts)
    else:
        if replicaset:
            client = pymongo.MongoClient(hosts, username=username, password=password, authSource=authsource, replicaset=replicaset)
        else:
            client = pymongo.MongoClient(hosts, username=username, password=password, authSource=authsource)

    return client

# 获取一条记录
def get_one(client, database, collection, filters={}):
    db = client[database]
    collection_obj = db[collection]

    return collection_obj.find_one(filters)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="get mongodb one document time.")
    parser.add_argument("-D", dest="database", default=None, help="mongodb database")
    parser.add_argument("-C", dest="collection", default=None, help="mongodb database collection")
    parser.add_argument("-u", dest="username", default="", help="mongodb username,default is none.")
    parser.add_argument("-p", dest="password", default="", help="mongodb password,default is none.")
    args = parser.parse_args()

    hosts = ['192.168.1.106:27017', '192.168.1.107:27017', '192.168.1.108:27017']

    try:
        t1 = time.time()
        client = mongo_replica_connect(hosts, args.username, args.password, args.database, '')
        get_one(client, args.database, args.collection, {})
        client.close()
        t2 = time.time()
        print (t2 - t1) * 1000
    except Exception as e:
        #print e
        print 1000

