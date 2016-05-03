#!/bin/bash

#ubuntu apache一键安装脚本
#作者：章郎虫
#博客：http://www.sijitao.net/

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

host='http://download.chekiang.info'

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
    ServerAdmin webmaster@dummy-host.example.com
    DocumentRoot "/usr/local/apache2/htdocs/"
    ServerName www.domain.com
    <IfModule dir_module>
	DirectoryIndex index.html index.php
    </IfModule>

    <Directory "/usr/local/apache2/htdocs/">
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

    #ProxyPass /upload !
    #ProxyPass / ajp://localhost:8009/
    #ProxyPassReverse / ajp://localhost:8009/

    ErrorLog "/tmp/www.domain.com-error_log"
    CustomLog "/tmp/www.domain.com-access_log" common
</VirtualHost>
EOF
ln -s /usr/local/apache2/conf /etc/httpd
mkdir -p /etc/httpd/conf.d
cat >>/usr/local/apache2/conf/httpd.conf <<EOF
Include conf/conf.d/
EOF

echo "============================start================================="

sleep 5

/etc/init.d/apache2 start

sleep 5

ps -ef|grep apache