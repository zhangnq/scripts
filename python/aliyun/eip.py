#!/usr/bin/env python
#coding:utf-8

import json
import sys
from config import access_id,access_key_secret
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import AllocateEipAddressRequest,ReleaseEipAddressRequest,AssociateEipAddressRequest, \
UnassociateEipAddressRequest,DescribeEipAddressesRequest

clt = client.AcsClient(access_id,access_key_secret,'cn-hongkong')

def create_eip_address(regionid='cn-hongkong',chargetype='PayByBandwidth',bandwidth=1,fmt='json'):
    request=AllocateEipAddressRequest.AllocateEipAddressRequest()
    request.set_accept_format(fmt)
    request.set_Bandwidth(bandwidth)
    request.add_query_param('RegionId',regionid)
    request.add_query_param('InternetChargeType',chargetype)
    
    try:
        result=clt.do_action(request)
        r_dict=json.loads(result)
    except:
        print("Create EIP Address Failed.")
        sys.exit()
    
    if r_dict.has_key('EipAddress'):
        res={}
        res['ip']=r_dict['EipAddress']
        res['id']=r_dict['AllocationId']
        return res
    else:
        print(r_dict['Message'])
        sys.exit()

def delete_eip_address(eipid,fmt='json'):
    request=ReleaseEipAddressRequest.ReleaseEipAddressRequest()
    request.set_accept_format(fmt)
    request.set_AllocationId(eipid)
    try:
        result=clt.do_action(request)
        r_dict=json.loads(result)
    except:
        print("Delete EIP Address Failed.")
        sys.exit()
    
    if r_dict.has_key('Code'):
        print(r_dict['Message'])
        sys.exit()
    else:
        return r_dict
    
def associate_eip_address(allocationid,instanceid,instancetype='EcsInstance',fmt='json'):
    request=AssociateEipAddressRequest.AssociateEipAddressRequest()
    request.set_accept_format(fmt)
    request.set_AllocationId(allocationid)
    request.add_query_param('InstanceType',instancetype)
    request.set_InstanceId(instanceid)
    try:
        result=clt.do_action(request)
        r_dict=json.loads(result)
    except:
        print("Associate EIP Address Failed.")
        sys.exit()
        
    if r_dict.has_key('Code'):
        print(r_dict['Message'])
        sys.exit()
    else:
        return r_dict
    
def unassociate_eip_address(allocationid,instanceid,instancetype='EcsInstance',fmt='json'):
    request=UnassociateEipAddressRequest.UnassociateEipAddressRequest()
    request.set_accept_format(fmt)
    request.set_AllocationId(allocationid)
    request.add_query_param('InstanceType',instancetype)
    request.set_InstanceId(instanceid)
    try:
        result=clt.do_action(request)
        r_dict=json.loads(result)
    except:
        print("Unassociate EIP Address Failed.")
        sys.exit()
        
    if r_dict.has_key('Code'):
        print(r_dict['Message'])
        sys.exit()
    else:
        return r_dict
    
def delete_unassociate_eip_address():
    request=DescribeEipAddressesRequest.DescribeEipAddressesRequest()
    request.set_accept_format('json')
    request.set_Status('Available')
    request.set_PageSize(50)
    try:
        result =json.loads(clt.do_action(request))
    except:
        print("Get Eip address list error.")
        sys.exit()
    eip_list=[]
    if result:
        eip_list=result['EipAddresses']['EipAddress']
        
    for eip in eip_list:
        #print eip['IpAddress'],eip['AllocationId']
        result=delete_eip_address(eip['AllocationId'])
        if result:
            print("EIP %s is deleted.") % eip['IpAddress']
        

if __name__ == "__main__":
    delete_unassociate_eip_address()
