#!/usr/bin/python2.7
#_*_coding:utf-8 _*_
# 源地址：https://github.com/X-Mars/Zabbix-Alert-WeChat

import requests,sys,json

reload(sys)
sys.setdefaultencoding('utf-8')

def GetTokenFromServer(Corpid,Secret):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid":Corpid,
        "corpsecret":Secret
    }
    r = requests.get(url=Url,params=Data,verify=False)
    print(r.json())
    if r.json()['errcode'] != 0:
        return False
    else:
        Token = r.json()['access_token']
        file = open('/usr/lib/zabbix/var/zabbix_wechat_config.json', 'w')
        file.write(r.text)
        file.close()
        return Token

def SendMessage(User,Agentid,Subject,Content):
    try:
        file = open('/usr/lib/zabbix/var/zabbix_wechat_config.json', 'r')
        Token = json.load(file)['access_token']
        file.close()
    except:
        Token = GetTokenFromServer(Corpid, Secret)

    n = 0
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                                 # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
        #"totag": Tagid,                                # 企业号中的标签id，群发使用（推荐）
        #"toparty": Partyid,                             # 企业号中的部门id，群发时使用。
        "msgtype": "text",                              # 消息类型。
        "agentid": Agentid,                             # 企业号中的应用id。
        "text": {
            "content": Subject + '\n' + Content
        },
        "safe": "0"
    }
    r = requests.post(url=Url,data=json.dumps(Data),verify=False)
    while r.json()['errcode'] != 0 and n < 4:
        n+=1
        Token = GetTokenFromServer(Corpid, Secret)
        if Token:
            Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
            r = requests.post(url=Url,data=json.dumps(Data),verify=False)
            print(r.json())

    return r.json()


if __name__ == '__main__':
    # zabbix传过来的第一个参数
    User = sys.argv[1]
    # zabbix传过来的第二个参数
    Subject = str(sys.argv[2])
    # zabbix传过来的第三个参数
    Content = str(sys.argv[3])

    # CorpID是企业号的标识
    Corpid = ""
    # Secret是管理组凭证密钥 
    Secret = ""
    # 通讯录标签ID
    #Tagid = "1"
    # 应用ID
    Agentid = ""
    # 部门ID
    #Partyid = "1"

    Status = SendMessage(User,Agentid,Subject,Content)
    print Status
