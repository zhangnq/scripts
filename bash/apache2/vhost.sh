#!/bin/bash

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, use sudo sh $0"
    exit 1
fi

domain="www.cyyun.com"
echo "Please input domain:"
read -p "(Default domain: www.cyyun.com):" domain
if [ "$domain" = "" ]; then
    domain="www.cyyun.com"
fi

if [ ! -f "/usr/local/apache2/conf/vhost/$domain.conf" ]; then
    echo "domain=$domain"
else
    echo "$domain is exist!"
    exit 1
fi

vhostdir="/home/wwwroot/$domain"

echo "Create Virtul Host directory......"
mkdir -p $vhostdir
echo "set permissions of Virtual Host directory......"
chmod -R 755 $vhostdir
chown -R www:www $vhostdir

cat >/usr/local/apache2/conf/vhost/$domain.conf<<eof
<VirtualHost *:10080>
    ServerAdmin admin@cyyun.com
    DocumentRoot "$vhostdir"
    ServerName $domain

    <Directory "$vhostdir">
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
        #不需要压缩
        BrowserMatch ^Mozilla/4 gzip-only-text/html
        BrowserMatch ^Mozilla/4\.0[678] no-gzip
        BrowserMatch \bMSIE !no-gzip !gzip-only-text/html
        #SetEnvIfNoCase Request_URI .(?:html|htm)$ no-gzip dont-varySetEnvIfNoCase
        #SetEnvIfNoCase Request_URI .(?:gif|jpe?g|png)$ no-gzip dont-vary
        SetEnvIfNoCase Request_URI .(?:exe|t?gz|zip|bz2|sit|rar)$ no-gzip dont-vary
        SetEnvIfNoCase Request_URI .(?:pdf|doc)$ no-gzip dont-vary
    </ifmodule>

    ProxyPass /upload !
    RedirectMatch 404 ^/upload/$

    #RewriteEngine on
    #RewriteCond %{REQUEST_URI} ^/$
    #RewriteRule ^/$ /sso/ [R=permanent,L]

    ProxyPass / ajp://localhost:8009/
    ProxyPassReverse / ajp://localhost:8009/

    ErrorLog "/var/log/apache2/$domain-error_log"
    CustomLog "/var/log/apache2/$domain-access_log" common

</VirtualHost>
eof

/etc/init.d/apache2 restart 