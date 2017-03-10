#!/bin/bash

#ubuntu apache一键安装脚本
#作者：章郎虫
#博客：http://www.sijitao.net/

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

host='http://download.chekiang.info'
wwwroot='/home/wwwroot'
www_default='/home/wwwroot/default'
log_dir='/var/log/apache2'

rm -rf /usr/local/apache2

echo "============================install dependency=================================="
sleep 5

apt-get install -y build-essential gcc g++ make zlibc zlib1g zlib1g-dev

cur_dir=$(pwd)
cd $cur_dir

echo "============================check files=================================="

sleep 5

if [ -s apr-1.5.0.tar.gz ]; then
  echo "apr [found]"
  else
  wget -c $host/apache/apr-1.5.0.tar.gz
fi

if [ -s apr-util-1.5.3.tar.gz ]; then
  echo "apr-util [found]"
  else
  wget -c $host/apache/apr-util-1.5.3.tar.gz
fi

if [ -s httpd-2.2.26.tar.bz2 ]; then
  echo "apache-httpd [found]"
  else
  wget -c $host/apache/httpd-2.2.26.tar.bz2
fi

echo "============================apache + apr + apr-util install================================="

sleep 5

tar zxvf apr-1.5.0.tar.gz
cd apr-1.5.0
./configure --prefix=/usr/local/apr-httpd
make && make install
cd ../

tar zxvf apr-util-1.5.3.tar.gz
cd apr-util-1.5.3
./configure --prefix=/usr/local/apr-util-httpd --with-apr=/usr/local/apr-httpd
make && make install
cd ../

tar jxvf httpd-2.2.26.tar.bz2
cd httpd-2.2.26
./configure --prefix=/usr/local/apache2 --with-apr=/usr/local/apr-httpd --with-apr-util=/usr/local/apr-util-httpd --enable-so --enable-mods-shared=most --enable-rewrite=shared --enable-proxy=shared --enable-proxy-ajp=shared --enable-proxy-balancer=shared --enable-speling=shared --enable-deflate --enable-headers
make && make install
cd ../

echo "============================config apache================================="

sleep 5

groupadd www
useradd -s /bin/bash -g www www

mkdir -pv $www_default
mkdir -pv $log_dir
chown www:www $wwwroot
chown www:www $log_dir

cp -a /usr/local/apache2/bin/apachectl /etc/init.d/
mv /etc/init.d/apachectl /etc/init.d/apache2
sed -i '2i# chkconfig: 35 70 30\n# description: Apache2' /etc/init.d/apache2
update-rc.d apache2 defaults

cp /usr/local/apache2/conf/httpd.conf /usr/local/apache2/conf/httpd.conf.bak
sed -i 's/#Include conf\/extra\/httpd-vhosts\.conf/Include conf\/extra\/httpd-vhosts\.conf/g' /usr/local/apache2/conf/httpd.conf
sed -i 's/User .*/User www/g' /usr/local/apache2/conf/httpd.conf
sed -i 's/Group .*/Group www/g' /usr/local/apache2/conf/httpd.conf

mv /usr/local/apache2/conf/extra/httpd-vhosts.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf.bak

cat > /usr/local/apache2/conf/extra/httpd-vhosts.conf<<EOF
NameVirtualHost *:80
<VirtualHost *:80>
    ServerAdmin admin@domain.com
    DocumentRoot "$www_default"
    ServerName www.domain.com
    <IfModule dir_module>
        DirectoryIndex index.html index.php
    </IfModule>

    #首页重定向规则
    #RewriteEngine on
    #RewriteCond %{REQUEST_URI} ^/$
    #RewriteRule ^/$ /login/ [R=permanent,L]

    <Directory "$www_default">
        Options FollowSymLinks
        AllowOverride None
        Order allow,deny
        Allow from all
    </Directory>

    <ifmodule mod_expires.c>
        ExpiresActive on
        ExpiresBytype text/css                  "access plus 1 days"
        ExpiresByType text/javascript           "access plus 1 days"
        ExpiresByType application/x-javascript  "access plus 1 days"
        ExpiresByType image/*                   "access plus 1 days"
    </ifmodule>

    <ifmodule mod_deflate.c>
        DeflateCompressionLevel 6
        AddOutputFilterByType DEFLATE text/html
        AddOutputFilterByType DEFLATE text/css
        AddOutputFilterByType DEFLATE text/javascript
        AddOutputFilterByType DEFLATE application/javascript
        AddOutputFilterByType DEFLATE application/x-javascript
        BrowserMatch ^Mozilla/4 gzip-only-text/html
        BrowserMatch ^Mozilla/4\.0[678] no-gzip
        BrowserMatch \bMSIE !no-gzip !gzip-only-text/html
        #SetEnvIfNoCase Request_URI .(?:html|htm)$ no-gzip dont-varySetEnvIfNoCase
        #SetEnvIfNoCase Request_URI .(?:gif|jpe?g|png)$ no-gzip dont-vary
        SetEnvIfNoCase Request_URI .(?:exe|t?gz|zip|bz2|sit|rar)$ no-gzip dont-vary
        SetEnvIfNoCase Request_URI .(?:pdf|doc)$ no-gzip dont-vary
    </ifmodule>

    #不代理upload路径
    #ProxyPass /upload !
    #访问/upload路径不提示403禁止错误，提示404不存在。
    #RedirectMatch 404 ^/upload/$
    
    #反向代理ajp 8009的应用，一般是tomcat。
    #ProxyPass / ajp://localhost:8009/
    #ProxyPassReverse / ajp://localhost:8009/
    
    #tomcat主备、负载均衡配置例子 开始
    #ProxyRequests off
    #Header add Set-Cookie "ROUTEID=.%{BALANCER_WORKER_ROUTE}e; path=/" env=BALANCER_ROUTE_CHANGED
    #<Proxy balancer://www.sijitao.net>
    #    BalancerMember ajp://192.168.0.10:8009 route=node1
    #    BalancerMember ajp://192.168.0.11:8009 route=node2 status=+H
    #    ProxySet stickysession=JSESSIONID
    #    ProxySet stickysession=ROUTEID
    #    byrequests(default),bytraffic,bybusyness
    #    ProxySet lbmethod=bytraffic
    #    ProxySet nofailover=On
    #</Proxy>
    #不代理balancer目录
    #ProxyPass /balancer !
    #ProxyPass / balancer://www.sijitao.net/
    #ProxyPassReverse / balancer://www.sijitao.net/
    #balancer目录，查看节点状态
    #<Location /balancer>
    #    SetHandler balancer-manager
    #    Proxypass !
    #    Order allow,deny
    #    Allow from all
    #</Location>
    #<Proxy *>
    #    Order allow,deny
    #    Allow from all
    #</Proxy>
    #tomcat主备、负载均衡配置例子 结束

    ErrorLog "$log_dir/www.domain.com-error_log"
    CustomLog "$log_dir/www.domain.com-access_log" common
</VirtualHost>
EOF

rm -rf /etc/httpd
ln -s /usr/local/apache2/conf /etc/httpd
mkdir -p /etc/httpd/conf.d
cat >>/usr/local/apache2/conf/httpd.conf <<EOF
Include conf/conf.d/
EOF

echo "============================logrotate================================="
sleep 5
rm -rf /etc/logrotate.d/apache2
cat >>/etc/logrotate.d/apache2 <<EOF
/var/log/apache2/*_log {
        daily
        rotate 12
        compress
        delaycompress
        missingok
        notifempty
        create 644 www www
        sharedscripts
        postrotate
                /etc/init.d/apache2 restart >/dev/null
        endscript
}
EOF

echo "============================start================================="
sleep 5
/etc/init.d/apache2 start

echo "============================end================================="
sleep 5
ps -ef|grep apache