#!/bin/bash

# run as root
if [ $(id -u) != "0" ]; then
    printf "Error: You must be root to run this tool!\n"
    exit 1
fi
clear

# config
obkey='helloworld@nbhao'
echo "Please input secret key share between server and client:"
read -p "(Default : helloworld@nbhao):" obkey
if [ "$obkey" = "" ]; then
	obkey="helloworld@nbhao"
fi
echo "obkey set to: ${obkey}"

# install
yum -y install unzip
wget http://download.chekiang.info/gongju/obfuscated-openssh.zip
unzip obfuscated-openssh.zip
cd obfuscated-openssh-master
yum -y install gcc make zlib zlib-devel openssl-devel openssl
./configure; make

# configure
obpath=`pwd`

rm -f sshd_config
touch sshd_config
cat >sshd_config <<EOF
ObfuscatedPort 2200
ObfuscateKeyword ${obkey}

Port 2201
Protocol 2

PermitRootLogin no

HostKey ${obpath}/ssh_host_rsa_key

RSAAuthentication yes
PubkeyAuthentication yes

Subsystem       sftp    /usr/libexec/sftp-server
EOF

# keygen
ssh-keygen -f ssh_host_rsa_key
mkdir -p /var/temp
mkdir -p /var/empty

# as service
rm -f /etc/init.d/obsshd
touch /etc/init.d/obsshd
chmod u+x /etc/init.d/obsshd
cat >/etc/init.d/obsshd <<EOF
#!/bin/bash

# chkconfig: 2345 85 25
# Description:       SSH is a protocol for secure remote shell access.
#                     This service starts up the OpenSSH server daemon.
#
# processname: obsshd

### BEGIN INIT INFO
# Provides: obsshd
# Required-Start: $local_fs $network $syslog
# Required-Stop: $local_fs $syslog
# Should-Start: $syslog
# Should-Stop: $network $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Start up the obfuscated OpenSSH server daemon
# Description:       SSH is a protocol for secure remote shell access.
#                    This service starts up the OpenSSH server daemon.
### END INIT INFO

export SSH_HOME=${obpath}

case "\$1" in

start)

echo "Starting obfuscated ssh..."
\$SSH_HOME/sshd -f \$SSH_HOME/sshd_config
;;

stop)

echo "Stopping obfuscated ssh..."
PID=\`ps aux|grep \$SSH_HOME/sshd | grep -v grep | awk ' { print ( \$(2) ) }'\`
kill \$PID
;;

restart)
\$0 stop
\$0 start
;;

*)

echo "Usage: \$0 {start|stop|restart}"
exit 1
esac

exit 0
EOF

#update-rc.d obsshd defaults
service obsshd start
