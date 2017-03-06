#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

project=$1
if [ ! $project ];then
    echo "Please input project."
    exit 1
fi

host='http://nb.cyyun.com:18104'

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script."
    exit 1
fi

echo "============================jdk==============================="
source /etc/profile
java -version
if [ $? -ne 0 ];then
	echo "Start to install jdk."
	sleep 3
	wget $host/zhangnq/jiaoben/jdk.sh
	bash jdk.sh
fi

echo "============================install dependency=================================="
sleep 5
issue=$(cat /etc/issue |awk '{print $2}' |awk -F "." '{print $1$2$3}')

if [ -s dependency_12.04.2.tar.gz ];then
	if [ "$issue" -eq "12042" ];then
		echo "ok,start to install dependency."
		tar zxvf dependency_12.04.2.tar.gz
		cd dependency
		dpkg -i *.deb
		cd ../
	else
		apt-get update
		apt-get autoremove -y
		apt-get install -y build-essential gcc g++ make zlibc zlib1g zlib1g-dev
	fi
else
	apt-get update
        apt-get autoremove -y
        apt-get install -y build-essential gcc g++ make zlibc zlib1g zlib1g-dev
fi

cur_dir=$(pwd)
cd $cur_dir

echo "============================check files=================================="

sleep 5

if [ -s apache-tomcat-7.0.52.tar.gz ]; then
  echo "apache-tomcat [found]"
  else
  wget -c $host/software/Tomcat/apache-tomcat-7.0.52.tar.gz
fi

echo "============================tomcat install================================="

sleep 5

if grep -q "^tomcat" /etc/group
  then
    echo "group tomcat exists"
  else
    groupadd tomcat -g 8000
fi
if grep -q "^tomcat" /etc/passwd
  then
    echo "user tomcat exists"
  else
    useradd -s /bin/bash -u 8000 -g tomcat tomcat
fi
cd $cur_dir

tar zxvf apache-tomcat-7.0.52.tar.gz
mv apache-tomcat-7.0.52 $project
mv $project /usr/local/

chown -R tomcat:tomcat /usr/local/$project

echo "============================config tomcat================================="

sleep 5

sed -i '/# OS specific support.*/a\JAVA_HOME="/usr/lib/jvm/jdk1.7.0_45"\nJAVA_OPTS="-server -Xms800M -Xmx1024M -XX:MaxPermSize=512M -Dfile.encoding=utf-8"' /usr/local/$project/bin/catalina.sh
sed -i '/<Connector port="8080" protocol=.*/a\\t\tURIEncoding="UTF-8"' /usr/local/$project/conf/server.xml
sed -i 's/<Connector port="8009" protocol="AJP\/1\.3"/& URIEncoding="UTF-8"/' /usr/local/$project/conf/server.xml
sed -i 's/<Server port="8005" shutdown="SHUTDOWN">/<Server port="-1" shutdown="SHUTDOWN">/g' /usr/local/$project/conf/server.xml
mv /usr/local/$project/conf/tomcat-users.xml /usr/local/$project/conf/tomcat-users.xml.bak
cat > /usr/local/$project/conf/tomcat-users.xml<<EOF
<?xml version='1.0' encoding='utf-8'?>
<tomcat-users>
 <role rolename="tomcat"/>
  <role rolename="manager-gui"/>
  <role rolename="manager-script"/>
  <role rolename="manager-status"/>
  <role rolename="manager-jmx"/>
  <user username="tomcat" password="tomcat" roles="tomcat,manager-gui,manager-script,manager-status,manager-jmx"/>
</tomcat-users>
EOF

rm -rf /usr/local/$project/webapps/*

wget https://raw.githubusercontent.com/zhangnq/scripts/master/bash/service/tomcat7 -O /etc/init.d/$project

sed -i "s/tomcat7/$project/" /etc/init.d/$project

chmod +x /etc/init.d/$project
update-rc.d $project defaults

wget https://raw.githubusercontent.com/zhangnq/scripts/master/bash/tomcat/cut_tomcat_logs -O /etc/cron.daily/cut_tomcat_logs
chmod +x /etc/cron.daily/cut_tomcat_logs

echo "============================start================================="

sleep 5

source /etc/profile
/etc/init.d/$project start

sleep 3
ps -ef|grep $project