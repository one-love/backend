#!/bin/sh


BIN_DIR=`dirname $0`
WSGI_MODULE=wsgi
FLASK_ENV="development"

. ${BIN_DIR}/common.sh
setup $1
sed -e "s;PROJECT_ROOT;${PROJECT_ROOT};" ansible_cfg >cfg/ansible.cfg
export ANSIBLE_CONFIG="${PROJECT_ROOT}/cfg/ansible.cfg"


flask celery start
