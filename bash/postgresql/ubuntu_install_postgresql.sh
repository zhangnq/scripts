#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

host='http://nb.cyyun.com:18104'

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script."
    exit 1
fi

echo "You can find the postgresql version from http://nb.cyyun.com:18104/software/PostgreSQL/."
read -p "Please input the postgresql version that you want to install(eg:9.3.5):" version
if [ "$version" = "" ];then
	echo "You must input postgresql version."
	exit 1
fi

echo "============================install dependency=================================="
sleep 5
issue=$(cat /etc/issue |awk '{print $2}' |awk -F "." '{print $1$2$3}')

if [ -s dependency_12.04.2.tar.gz ];then
	if [ "$issue" -eq "12042" ];then
		echo "Ok,start to install dependency."
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

apt-get install -y libreadline-dev language-pack-zh-hans

mv /etc/default/locale /etc/default/locale.bak
echo "LANG=\"en_US.UTF-8\"" >/etc/default/locale
echo "LANGUAGE=\"en_US:en\"" >>/etc/default/locale

cur_dir=$(pwd)
cd $cur_dir

echo "============================check files=================================="

sleep 5

if [ "$version" = "9.3.5" ];then
	if [ -s postgresql-9.3.5.tar.gz ]; then
	  echo "postgresql-9.3.5 [found]"
	  else
	  wget -c $host/software/PostgreSQL/postgresql-9.3.5.tar.gz
	fi
elif [ "$version" = "9.2.9" ];then
	if [ -s postgresql-9.2.9.tar.gz ]; then
          echo "postgresql-9.2.9 [found]"
          else
          wget -c $host/software/PostgreSQL/postgresql-9.2.9.tar.gz
        fi
else
	echo "Please input the valid postgresql version."
	exit 1
fi

echo "============================postgresql install================================="

sleep 5

cd $cur_dir

PGHOME=/opt/PostgreSQL/`echo $version |awk -F "." '{print $1$2}'`
PGPATH=$PGHOME/bin
PGDATA=/data/pgsql

tar zxvf postgresql-$version.tar.gz
cd postgresql-$version
./configure --prefix=$PGHOME
make
make install

groupadd postgres
useradd -s /bin/bash -g postgres postgres
mkdir -p /home/postgres
chown postgres:postgres /home/postgres
mkdir -p $PGDATA
chown -R postgres.postgres $PGDATA
chmod -R go-rwx $PGDATA

cat >>/etc/profile<<eof
export PATH=$PGPATH:\$PATH
export PGDATA=$PGDATA
export PGHOME=$PGHOME
export PGPORT=5432
eof

source /etc/profile

wget $host/zhangnq/jiaoben/init.d/postgresql
mv postgresql /etc/init.d/
chmod +x /etc/init.d/postgresql
update-rc.d postgresql defaults

su - postgres -c "$PGHOME/bin/initdb -D $PGDATA --locale=zh_CN.UTF8"

mkdir -p $PGDATA/pg_log
chown postgres:postgres $PGDATA/pg_log
chmod go-rwx $PGDATA/pg_log

sed -i "s/#listen_addresses = .*/listen_addresses = '\*'/g" $PGDATA/postgresql.conf
sed -i "s/#port = 5432/port = 5432/g" $PGDATA/postgresql.conf
sed -i "s/#log_destination = 'stderr'/log_destination = 'stderr'/g" $PGDATA/postgresql.conf
sed -i "s/#logging_collector = off/logging_collector = on/g" $PGDATA/postgresql.conf
sed -i "s/#log_filename = 'postgresql-%Y-%m-%d_%H%M%S\.log'/log_filename = 'postgresql-%Y-%m-%d\.log'/g" $PGDATA/postgresql.conf
sed -i "s/#log_rotation_age = 1d/log_rotation_age = 1d/g" $PGDATA/postgresql.conf
sed -i "s/#log_rotation_size = 10MB/log_rotation_size = 10MB/g" $PGDATA/postgresql.conf
sed -i "s/#log_min_messages = warning/log_min_messages = warning/g" $PGDATA/postgresql.conf
sed -i "s/#log_min_error_statement = error/log_min_error_statement = error/g" $PGDATA/postgresql.conf
sed -i "s/#log_min_duration_statement = -1/log_min_duration_statement = 1000/g" $PGDATA/postgresql.conf
sed -i "s/#log_line_prefix = ''/log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,host=%h '/g" $PGDATA/postgresql.conf
sed -i "s/#log_statement = 'none'/log_statement = 'ddl'/g" $PGDATA/postgresql.conf

su - postgres -c "$PGHOME/bin/pg_ctl start"

if [ $? -eq 0 ];
then
	sleep 15
	echo "Postgresql is installed  successfully."
	ps -ef|grep postgres
	#echo "Start to reboot!"
	#sleep 3
	#reboot
else
	echo "Start Postgresql failed,Please check!"
	exit 1
fi