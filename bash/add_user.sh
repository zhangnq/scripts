#!/bin/bash

USERNAMES="zhangnq"


for USERNAME in $USERNAMES
do
    if id $USERNAME &>/dev/null ;then
        echo "Username $USERNAME exists"
        echo "$USERNAME:$USERNAME"|chpasswd
    else
        mkdir -pv /home/$USERNAME &>/dev/null
        cp /etc/skel/.bash_logout /home/$USERNAME
        cp /etc/skel/.bashrc /home/$USERNAME
        cp /etc/skel/.profile /home/$USERNAME
        useradd -s /bin/bash -d /home/$USERNAME $USERNAME
        chown -R $USERNAME:$USERNAME /home/$USERNAME
        chmod go-rwx /home/$USERNAME
        echo "$USERNAME:$USERNAME"|chpasswd
        echo "User $USERNAME is added."
    fi

    if [ "$USERNAME" == "zhangnq" ] || [ "$USERNAME" == "admin" ];then
        adduser $USERNAME admin &>/dev/null
        adduser $USERNAME sudo &>/dev/null
    fi
done
