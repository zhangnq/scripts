hostloc赚金币脚本

修改，设置http代理。
proxie = { 
    'http' : 'http://username:password@www.sijitao.net:1080'
}

修改用户名密码，可以配置多个。
users=[
    {'username':'user1','password':'password1'},
    {'username':'user2','password':'password2'},
]

直接运行 python hostloc.py 即可

配合crontab，每天运行一次。