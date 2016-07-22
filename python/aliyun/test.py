#coding:utf-8

import json
from config import access_id,access_key_secret

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest,CreateInstanceRequest,DescribeImagesRequest, \
AllocatePublicIpAddressRequest,StartInstanceRequest,ModifyInstanceNetworkSpecRequest,DeleteInstanceRequest,StopInstanceRequest, \
AllocateEipAddressRequest,AssociateEipAddressRequest,CreateVpcRequest,CreateVSwitchRequest




clt = client.AcsClient(access_id,access_key_secret,'cn-hongkong')

print "##########DescribeRegions###########"
request = DescribeRegionsRequest.DescribeRegionsRequest()
request.set_accept_format('json')

result = clt.do_action(request)

'''
status, headers, body = clt.get_response(request)
print status
result = json.loads(body)
for key,value in result.items():
    print key,value 
'''

print result
#print json.loads(result)['RequestId']
for i in json.loads(result)['Regions']['Region']:
    print i['LocalName'],i['RegionId']

print "#########DescribeImages############"

request=DescribeImagesRequest.DescribeImagesRequest()
request.set_accept_format('json')
request.set_PageSize(100)

result=clt.do_action(request)
result=json.loads(result)

for i in result['Images']['Image']:
    #print i['ImageId'], i['Description'], i['OSType'], i['OSName']
    if i['OSName'].strip() == u'Ubuntu  14.04 64位':
        image_id=i['ImageId']

print u"Ubuntu  14.04 64位 : %s" % image_id

print "###########CreateInstance##########"

request=CreateInstanceRequest.CreateInstanceRequest()
request.set_accept_format('json')
request.set_ImageId('ubuntu1404_64_40G_cloudinit_20160427.raw')
request.set_InstanceType('ecs.t1.small')
request.set_Password('123456')

#result = clt.do_action(request)
#print json.loads(result)
##  {u'InstanceId': u'i-62pepv5ke', u'RequestId': u'0CF4B16A-EEE3-4C6A-A6AC-352630688D58'}

print "##########AllocatePublicIpAddress###########"

request=AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
request.set_accept_format('json')
request.set_InstanceId('i-62wpk9e7e')

#print clt.do_action(request)
## {"RequestId":"3993EC47-222B-48EE-ABA1-246CEB40B2FC","IpAddress":"49.213.8.1"}

print "##########StartInstance###########"

request=StartInstanceRequest.StartInstanceRequest()
request.set_accept_format('json')
request.set_InstanceId('i-62wpk9e7e')

#print clt.do_action(request)

print "##########ModifyInstanceNetworkSpec###########"
request=ModifyInstanceNetworkSpecRequest.ModifyInstanceNetworkSpecRequest()
request.set_accept_format('json')
request.set_InstanceId('i-62wpk9e7e')
request.set_InternetMaxBandwidthOut(1)

#print clt.do_action(request)

print "##########StopInstance###########"
request=StopInstanceRequest.StopInstanceRequest()
request.set_accept_format('json')
request.set_InstanceId('i-62wpk9e7e')
request.set_ForceStop('true')

#print clt.do_action(request)

print "##########DeleteInstance###########"
request=DeleteInstanceRequest.DeleteInstanceRequest()
request.set_accept_format('json')
request.set_InstanceId('i-62wpk9e7e')

#print clt.do_action(request)

print "##########AllocateEipAddress###########"
request=AllocateEipAddressRequest.AllocateEipAddressRequest()
request.set_accept_format('json')
request.set_Bandwidth(1)
request.add_query_param('RegionId','cn-hongkong')
request.add_query_param('InternetChargeType','PayByBandwidth')

#print clt.do_action(request)
#{"RequestId":"A3EA6988-AABE-4E2D-B4B0-D1C0BF812D15","EipAddress":"47.89.13.75","AllocationId":"eip-gky75i1p5"}

print "##########AssociateEipAddress###########"
request=AssociateEipAddressRequest.AssociateEipAddressRequest()
request.set_accept_format('json')
request.set_AllocationId('eip-gky75i1p5')
request.add_query_param('InstanceType','EcsInstance')
request.set_InstanceId('i-62bh3lg5y')

print clt.do_action(request)

print "##########CreateVpc###########"
request=CreateVpcRequest.CreateVpcRequest()
request.set_accept_format('json')
request.add_query_param('RegionId', 'cn-hongkong')
#print clt.do_action(request)
#{"RequestId":"52B694B2-C337-49B5-A50C-A8511E5FCEB8","RouteTableId":"vtb-1i2b5k2xo","VRouterId":"vrt-k46tudsez","VpcId":"vpc-paxw4rrw3"}

print "##########CreateVSwitch###########"
request=CreateVSwitchRequest.CreateVSwitchRequest()
request.set_accept_format('json')
request.set_ZoneId('cn-hongkong-b')
request.set_CidrBlock('172.16.1.0/24')
request.set_VpcId('vpc-paxw4rrw3')

#print clt.do_action(request)
#{"RequestId":"66903EE4-E307-46FA-8ED4-1A262E7EB4EA","VSwitchId":"vsw-x6wzk2af2"}
