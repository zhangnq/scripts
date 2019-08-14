# -*- coding: UTF-8 -*-

#author: zhangnq
#url: https://zhangnq.com
#description: 使用aliyun的api实现ddns动态域名解析
#安装必须的模块
#pip install aliyun-python-sdk-domain
#pip install requests


import os
import datetime
import time
import urllib
import subprocess
import pickle
import socket
from json import loads
from requests import post
# email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
# aliyun sdk
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

rc_rr = "home"                  # 指代二级域名（子域名，空则使用 @ 代替）
rc_domain = "zhangnq.com"       # 指代完整域名，若未配置阿里云 NameServer 解析修改也无效
rc_format = "json"              # 指定返回数据格式，目前本例使用 JSON 数据
rc_type = "A"                   # 指定修改记录类型，目前本例使用 A 记录
rc_ttl = "600"                  # 指定修改 TTL 值，目前本例使用 600 秒
rc_format = "json"              # 使用 JSON 返回数据，也可以填写为 XML

data_pkl='/tmp/ddns_ip.pkl'     # 保存ip临时文件

# 定义邮箱参数
smtp_server = "smtp.zhangnq.com"
smtp_port = 465
smtp_username = "noreply@zhangnq.com"
smtp_password = "123456"
smtp_ssl = True
to_emails = "admin@zhangnq.com"
email_error_log = "/tmp/mail_error.log"

access_key_id = "xxxxxxxxxxxxxxxx"                          # 这里为 Aliyun AccessKey 信息
access_key_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"        # 这里为 Aliyun AccessKey 信息

clt = AcsClient(access_key_id, access_key_secret, 'default')

class sendMail(object):
    def __init__(self, smtp_server, smtp_port, from_mail, mail_pass, error_file, is_ssl=False, is_tls=False):
        self.smtp_server = smtp_server
        self.smtp_port = int(smtp_port)
        self.from_mail = from_mail
        self.mail_pass = mail_pass
        self.is_ssl = is_ssl
        self.is_tls = is_tls
        self.error_file = error_file

    def __writeError(self, errinfo):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(self.error_file, 'a') as f:
            f.write(now_time)
            f.write('     ' + str(errinfo))
            f.write('\n')

    def send(self, subject, body, to_mails, files, mail_type='plain'):
        """
            subject: 邮件主题
            body: 邮件内容
            to_mail: 收件人，英文逗号,分隔
            files: 附件路径，list列表
        """
        to_mails = str(to_mails).split(',')
        to_mails = [item.strip() for item in to_mails]

        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header(self.from_mail, 'utf-8')
        message['To'] = ', '.join(to_mails)
        message['Subject'] = Header(subject, 'utf-8')

        # 邮件正文内容
        message.attach(MIMEText(body, mail_type, 'utf-8'))

        # 构造附件，传送当前目录下的 test.txt 文件
        for myfile in files:
            att1 = MIMEText(open(myfile, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'

            basename = u'%s' % os.path.basename(myfile)
            att1["Content-Disposition"] = "attachment; filename=%s" % basename.encode('utf-8')
            message.attach(att1)

        try:
            if self.is_ssl:
                s = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=30)
            else:
                s = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30)
            if self.is_tls and not self.is_ssl:
                s.starttls()
            #s.set_debuglevel(1)
            s.login(self.from_mail, self.mail_pass)
            s.sendmail(self.from_mail, to_mails, message.as_string())
            s.quit()
        except smtplib.SMTPException as e:
            self.__writeError(e)


def check_record_id(dns_rr, dns_domain):
    times = 0            # 用于检查对应子域名的记录信息
    check = 0            # 用于确认对应子域名的记录信息
    request = CommonRequest()
    request.set_accept_format('json')                   # 设置返回格式
    request.set_domain('alidns.aliyuncs.com')           # 阿里云服务
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2015-01-09')
    request.set_action_name('DescribeDomainRecords')

    request.add_query_param('DomainName', rc_domain)    # 设置请求域名
    request.add_query_param('RRKeyWord', rc_rr)
    request.add_query_param('TypeKeyWord', rc_type)
    response = loads(clt.do_action(request))            # 接受返回数据
    result = response['DomainRecords']['Record']        # 缩小数据范围
    for record_info in result:                            # 遍历返回数据
        if record_info['RR'] == dns_rr:                    # 检查是否匹配
            check = 1; break;                            # 确认完成结束
        else:
            times += 1                                    # 进入下个匹配
    if check:
        result = result[times]['RecordId']                # 返回记录数值
    else:
        result = -1                                        # 返回失败数值
    return result

def my_ip_direct():
    opener = urllib.urlopen('http://tool.sijitao.net/network/ip/myip?type=html')
    strg = opener.read()
    return strg

def my_ip_json():
    opener = urllib.urlopen('http://tool.sijitao.net/network/ip/myip?type=json')
    strt = opener.read().decode('utf-8')
    strg = loads(strt)
    return strg['ip']

def my_ip():
    ip1 = str(my_ip_direct()).replace('\n', '')
    return ip1

def old_ip(dns_record_id):
    request = CommonRequest()
    request.set_accept_format('json')                           # 设置返回格式
    request.set_domain('alidns.aliyuncs.com')
    request.set_method('POST')                                  # 设置记录值
    request.set_protocol_type('https')
    request.set_version('2015-01-09')
    request.set_action_name('DescribeDomainRecordInfo')

    request.add_query_param('RecordId', dns_record_id)

    result = loads(clt.do_action(request))                      # 接受返回数据
    return result['Value']                                      # 返回记录数值

def add_dns(dns_rr, dns_domain, dns_type, dns_value, dns_ttl):
    request = CommonRequest()
    request.set_accept_format('json')                           # 设置返回格式
    request.set_domain('alidns.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2015-01-09')
    request.set_action_name('AddDomainRecord')

    request.add_query_param('DomainName', dns_domain)           # 设置请求域名
    request.add_query_param('RR', dns_rr)                       # 设置子域名信息
    request.add_query_param('Type', dns_type)                   # 设置 DNS 类型
    request.add_query_param('Value', dns_value)                 # 设置解析 IP

    response = loads(clt.do_action(request))                    # 发送请求内容
    return response

def update_dns(dns_rr, dns_type, dns_value, dns_record_id, dns_ttl):
    request = CommonRequest()
    request.set_accept_format('json')                           # 设置返回格式
    request.set_domain('alidns.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2015-01-09')
    request.set_action_name('UpdateDomainRecord')

    request.add_query_param('RecordId', dns_record_id)          # 设置记录值
    request.add_query_param('RR', dns_rr)                       # 设置子域名信息
    request.add_query_param('Type', dns_type)                   # 设置 DNS 类型
    request.add_query_param('Value', dns_value)                  # 设置解析 IP

    response = loads(clt.do_action(request))                    # 发送请求内容
    return response

def send_mail(content):
    email = sendMail(smtp_server, smtp_port, smtp_username, smtp_password, email_error_log, smtp_ssl)
    subject = "DDNS IP Update From ISP."
    email.send(subject, content, to_emails, [])

def get_time():
    return "[" + time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())) + "]"


def save_local_ip(ip):
    val = {"ip":ip}
    f=file(data_pkl,'wb')
    pickle.dump(val,f)
    f.close()
    return True

def get_local_ip():
    try:
        f=file(data_pkl,'rb')
        data_dict=pickle.load(f)
        f.close()
    except:
        data_dict={"ip":""}
    return data_dict["ip"]

def host2ip(hostname):
    ip =socket.gethostbyname(hostname)
    return ip


if __name__ == "__main__":
    rc_value = my_ip()
    tips = get_time()
    o_ip = get_local_ip()

    # get record from dns
    dom = "{}.{}".format(rc_rr, rc_domain)
    try:
        o_ip2 = host2ip(dom)
    except:
        o_ip2 = o_ip

    # get record from aliyun sdk
    if not o_ip or o_ip != o_ip2:
        rc_record_id = check_record_id(rc_rr, rc_domain)
        o_ip = old_ip(rc_record_id)
        save_local_ip(o_ip)
        print tips + " Save old IP to file..."

    # start
    if rc_value == o_ip:
        tips += " Same DNS Record..."
    else:
        rc_record_id = check_record_id(rc_rr, rc_domain)
        resp = update_dns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl)
        # print resp
        if resp.has_key("RecordId"):
            tips += " DNS Record was updated from [" + o_ip + "] to [" + rc_value + "]."
            # save new ip to local
            save_local_ip(rc_value)
        else:
            tips += " " + resp["Message"]

        #send email
        send_mail(tips)

    print tips

