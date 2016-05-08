#!/bin/bash

export C_FORCE_ROOT=yes

if [ -s /tmp/gunicorn.pid ]; then
    kill -SIGHUP $(cat /tmp/gunicorn.pid)
else
    cd /usr/src/app
    gunicorn --config gunicorn.conf manage:app
    cd -
fi
