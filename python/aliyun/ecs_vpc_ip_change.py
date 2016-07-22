#!/usr/bin/env python
#coding:utf-8

import sys
import time
from config import ecs_vpc_id,eip_bandwidth
from eip import create_eip_address,delete_eip_address,associate_eip_address,unassociate_eip_address
from instance import instance_info

def main():
    #获取当前vpc下ecs主机的eip
    instance=instance_info(ecs_vpc_id)
    eip_id=instance['EipAddress']['AllocationId']
    eip_ip=instance['EipAddress']['IpAddress']
    if not instance:
        print("Get instance info error.")
        sys.exit()
    else:
        if not eip_id:
            print("Instance %s has not associate eip address.") % ecs_vpc_id
        else:
            print("Instance: %s ,Eip id: %s .") % (ecs_vpc_id,eip_id)
    
            #解绑eip
            result_unassociate=unassociate_eip_address(eip_id, ecs_vpc_id)
            if not result_unassociate:
                print("Unassociate eip address from %s error.") % ecs_vpc_id
                sys.exit()
            
            #判断真正解绑后开始删除老的eip
            while True:
                eip_id_tmp=instance_info(ecs_vpc_id)['EipAddress']['AllocationId']
                if not eip_id_tmp:
                    #删除老的eip
                    result_release=delete_eip_address(eip_id)
                    if not result_release:
                        print("Release eip %s error.") % eip_id
                        sys.exit()
                    break
                else:
                    continue
                time.sleep(1)
    
    #申请新eip
    result_allocate=create_eip_address(bandwidth=eip_bandwidth)
    if not result_allocate:
        print("Allocate new eip address error.")
        sys.exit()
    
    #time.sleep(10)
    
    #绑定eip
    result_associate=associate_eip_address(result_allocate['id'], instanceid=ecs_vpc_id)
    if not result_associate:
        print("Associate eip %s to instance %s error.") % (result_allocate,ecs_vpc_id)
        sys.exit()
    else:
        print("Associate eip %s to instance %s successfully.") % (result_allocate['ip'],ecs_vpc_id)
        ip_dict={
            'oip':eip_ip,
            'nip':result_allocate['ip']
        }
        return ip_dict
    

if __name__ == "__main__":
    print main()

