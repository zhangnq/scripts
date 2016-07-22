#coding:utf-8

import json
import sys
from config import access_id,access_key_secret,ecs_vpc_id
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest

clt = client.AcsClient(access_id,access_key_secret,'cn-hongkong')

def instance_info(instanceid,fmt='json'):
    request=DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format(fmt)
    request.set_InstanceIds([instanceid])
    
    try:
        result=clt.do_action(request)
        r_dict=json.loads(result)
    except:
        print("Get Instance Info Failed.")
        sys.exit()
        
    if r_dict.has_key('TotalCount') and r_dict['TotalCount'] != 0:
        instance=r_dict['Instances']['Instance'][0]
        return instance
    else:
        print("Instance id %s is not exist.") % instanceid
        sys.exit()

if __name__ == "__main__":
    print instance_info(ecs_vpc_id)['EipAddress']

