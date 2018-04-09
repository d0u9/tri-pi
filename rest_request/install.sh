#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "Permission denied"
    exit 1
fi

target_dir=/opt/app
run_dir=/run/rest_request
proj_name=rest_request

id app > /dev/null || useradd -s /sbin/nologin -M -u 5001 -U app
id pyenv > /dev/null || useradd -s /bin/bash -m -G 5001 -u 6001 -U pyenv
id pyenv | grep gpio > /dev/null || usermod -a -G gpio pyenv

test -d $target_dir || mkdir -p $target_dir
chown app:app $target_dir

pwd=$(pwd)
rm -fr $target_dir/$proj_name

cp -r $pwd $target_dir/$proj_name
chown -R pyenv:app $target_dir/$proj_name

cp -f $pwd/rest-request.service /etc/systemd/system/

test -d $run_dir || mkdir -p $run_dir
chown -R pyenv:app $run_dir

systemctl daemon-reload
systemctl restart rest-request
