## All In One目录结构及说明：
```  
├── confs                       放置所有zabbix key的配置  
├── install_zabbix_extend.sh    安装脚本  
├── readme.txt                  本文件  
├── readme.md                   本文件(md)  
├── src                         源码文件  
├── effects                     运行效果图    
└── templates                   所有相关的zabbix模板  
```

## 使用说明：
```  
《一》确定zabbix agent扩展功能需要包括的配置文件路径，例如/usr/local/zabbix_agent_extend/conf  
修改zabbix agent的主配置文件zabbix_agentd.conf，加入如下内容：  
Include=/usr/local/zabbix_agent_extend/conf/*.conf  
《二》在root用户下执行zabbix_extend_init.sh脚本，脚本第一个参数为配置文件存放目录，第二个参数为源码脚本存放路径。  
例如执行如下命令，其中/usr/local/zabbix_agent_extend/conf是步骤《一》中确定的文件路径：  
bash zabbix_extend_init.sh /usr/local/zabbix_agent_extend/conf /usr/local/zabbix_agent_extend/scripts  
其作用是：  
1）将confs目录下的文件拷贝到/usr/local/zabbix_agent_extend/conf目录  
2）将src目录下的文件拷贝到/usr/local/zabbix_agent_extend/scripts目录  
注：  
1）步骤1）中拷贝之前脚本会对这些配置文件先进行处理；  
2）脚本执行到最后会尝试执行"/etc/init.d/zabbix-agent restart"命令重启zabbix agent，如果执行失败，请根据agent安装的实际情况进行重启，使配置生效  
《三》将templates目录下的模板文件导入到zabbix系统；  
《四》将主机link到相关的模板；  
《五》大功告成；  
```

## 更新说明：
```
=========  
20170618  
=========  
关于JVM监控，前一个版本，对适用于JVM大部分的GC算法，都集中在同一个模板中，这样会导致有些key不支持， 
因为一个JVM实例同时只能支持一个GC算法，而一个GC算法通常有两个垃圾收集器，而不同垃圾收集器对内存管理方式又各不相同。  
此次更新，主要解决上述问题，同时增加了对G1 GC算法的支持，另外同步调整了代码，为新的可能出现的GC算法预留可扩展性。  
具体来说，JVM监控，使用模板文件“Qiueer-Template JVM.xml”中“Qiueer-Template JVM”模块即可,此模板包含了以下五个子模板：  
Qiueer-Template JVM Generic Basic    
Qiueer-Template JVM Generic With GC Is G1  
Qiueer-Template JVM Generic With GC Is ConcMarkSweep  
Qiueer-Template JVM Generic With GC Is Parallel  
Qiueer-Template JVM Generic With GC Is Serial  
  
=========  
20170716   
=========  
增加对nginx的监控，使用方法见nginx.conf或python nginx.py -h或直接阅读代码，偷懒:) 

========
20180102
======== 
更新代码，解决由root用户手动执行脚本后导致日志文件、缓存文件的权限问题
```

## 注意事项：
```  
以下的日志路径、缓存文件路径有变，变更后的目录不变，文件名类似。
1）jvm监控   
日志存储位置：/tmp/zabbix_jvm_info.log   
2）tomcat监控   
日志存储位置：/tmp/zabbix_tomcat_info.log   
需打开jmxport监控端口及tomcat的配置文件server.xml对启动zabbix agent的用户可读（通常是zabbix），具体参考上层目录Tomcat   
3）mongodb监控   
日志存储位置：/tmp/zabbix_mongodb.log   
cache存储位置：/tmp/.zabbix_mongodb_cache*.txt   
如果mongodb做了权限，那么需要将账号密码写到/usr/local/public-ops/zabbix/.mongodb.passwd，且该文件对启动zabbix agent的用户可读（通常是zabbix）   
格式是： 端口  用户名  密码   
4）memcache监控   
日志存储位置：/tmp/zabbix_memcached.log   
cache存储位置：/tmp/zabbix_memcached_cache*.txt   
4）redis监控   
日志存储位置：/tmp/zabbix_redis_info.log   
cache存储位置：/tmp/.zabbix_redis_*.txt   
如果redis设置了密码，那么需要将账号密码写到/usr/local/public-ops/zabbix/.redis.passwd，且该文件对启动zabbix agent的用户可读（通常是zabbix）   
5）mysql监控   
日志存储位置： /tmp/zabbix_mysql_variables_slave_status.log  /tmp/zabbix_mysql_perf.log /tmp/zabbix_mysql_status.log   
cache存储位置：/tmp/.zabbix_mysql_variables_slave_status*.txt  /tmp/.zabbix_mysql_status*.txt   
需创建监控用户dbmonitor，创建命令如下，供参考：   
create user 'dbmonitor'@'localhost'  identified by 'monitor_md5_666';   
grant REPLICATION CLIENT on *.* to 'dbmonitor'@'localhost';   
flush privileges;   
关于mysql监控共有6个模板，如果对zabbix不是很熟练，使用下面两个即可：   
MySQL-Master-For-Business   
MySQL-Slave-For-Business   
``` 

## 其他：
```   
1）对所有脚本，如果命令行执行成功，但让zabbix执行取不到数据，大多数是权限的问题，检查一下/tmp目录各个日志文件、或cache文件、或密码文件的权限，或者执行如下：
chmod 777 /tmp/.zabbix_*.{log,txt}
chmod 777 /tmp/zabbix_*.{txt,log}
```
